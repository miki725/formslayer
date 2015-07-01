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
    def __init__(self, pdf_path, data, flatten=False):
        self.pdf_path = pdf_path
        self.data = data
        self.flatten = flatten

        log.bind(pdf_path=self.pdf_path)

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

        cmd = (
            '{pdftk} {pdf} fill_form {fdf} output {output} {flatten}'
            ''.format(pdftk=PDFTK_PATH,
                      pdf=self.pdf_path,
                      fdf=fdf_path,
                      output='-',
                      flatten=self.flatten and 'flatten' or '')
        )

        log.debug(cmd)

        try:
            p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
            stdout, stderr = p.communicate(fdf, 10)

        except SubprocessError:
            raise PDFNotFilled()

        else:
            if p.returncode != 0:
                raise PDFNotFilled()

            log.info('Successfully filled in pdf')

            return stdout

        finally:
            os.unlink(fdf_path)
