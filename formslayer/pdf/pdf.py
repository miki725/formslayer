# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import os
import tempfile
from subprocess import PIPE, Popen, SubprocessError, check_output

import structlog

from .exceptions import PDFNotFilled


PDFTK_PATH = (
    os.environ.get('PDFTK_PATH')
    or check_output('which pdftk', shell=True).decode('utf-8').rstrip('\n')
)
log = structlog.get_logger()


class PDFFiller(object):
    def __init__(self, pdf, data, flatten=False):
        self.pdf = pdf
        self.data = data
        self.flatten = flatten

        log.bind(pdf=pdf, pdf_name=self.pdf.name)

    def generate_fdf(self):
        fields = []
        for key, value in self.data.items():
            fields.append('<field name="{}"><value>{}</value></field>'.format(key, value))

        xfdf = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<xfdf xmlns="http://ns.adobe.com/xfdf/" xml:space="preserve">'
            '<fields>'
            '{}'
            '</fields>'
            '</xfdf>'
            ''.format(''.join(fields))
        )

        log.debug('Generated xfdf')

        return xfdf.encode('utf-8')

    def __call__(self):
        fdf = self.generate_fdf()

        fdf_fid, fdf_path = tempfile.mkstemp(suffix='.xfdf')
        os.write(fdf_fid, fdf)
        os.close(fdf_fid)

        pdf_fid, pdf_path = tempfile.mkstemp(suffix='.pdf')
        os.write(pdf_fid, self.pdf.read())
        os.close(pdf_fid)

        cmd = (
            '{pdftk} {pdf} fill_form {fdf} output {output} {flatten}'
            ''.format(pdftk=PDFTK_PATH,
                      pdf=pdf_path,
                      fdf=fdf_path,
                      output='-',
                      flatten=self.flatten and 'flatten' or '')
        )

        log.debug('Filling in pdf', cmd=cmd)

        try:
            p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
            stdout, stderr = p.communicate(fdf, 10)

        except SubprocessError as e:
            log.error('Error filling in pdf', error=e)
            raise PDFNotFilled()

        else:
            if p.returncode != 0:
                log.error('Error filling in pdf', returncode=p.returncode, stderr=stderr)
                raise PDFNotFilled()

            log.info('Successfully filled in pdf')

            return stdout

        finally:
            os.unlink(fdf_path)
            os.unlink(pdf_path)
