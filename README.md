# FormSlayer

[![Build Status](https://travis-ci.org/miki725/formslayer.svg?branch=master)](https://travis-ci.org/miki725/formslayer)

FormSlayer is a Django application which implements RESTful API for working with PDFs.

PDF files/forms handling can be tedious. FormSlayer eventual goal is to fix that by providing a stand-along (aka microservice) solution for managing pdf files/forms via simple RESTful API. In order to make FormSlayer super easy to run as a microservice, FormSlayer is packaged as a Docker image on [dockerhub](https://registry.hub.docker.com/u/miki725/formslayer/). That allows FormSlayer to be easily deployed either as standalone container or as part of a larger docker application with separate db, load balancer, etc containers.

## API

Currently the feature-set is rather small however if you would like to add new features, please feel free to file a feature request at [GitHub](https://github.com/miki725/formslayer/issues).

### Fill forms

This service allows to fill in previously uploaded PDF forms:

```
❯❯❯ curl -s -X POST \
    -H 'Accept: application/json' \
    -H 'Authorization: token f9f00121c4f6b53db96faff75f5b95f2bef0bbe7' \
    --data '{"fields":[{"name":"foo","value":"bar"}}' \
    http://localhost:8000/api/pdf/forms/2267128b-3e4a-4f29-b430-7c8f2f1e458d/filled/
{
    "url": "http://localhost:8000/api/pdf/forms/2267128b-3e4a-4f29-b430-7c8f2f1e458d/filled/a46ca86d-8726-46a0-b4c6-66b999856dd6/",
    "form": "http://localhost:8000/api/pdf/forms/2267128b-3e4a-4f29-b430-7c8f2f1e458d/",
    "id": "a46ca86d872646a0b4c666b999856dd6",
    "created": "2015-07-12T12:00:00.000000Z",
    "filled_pdf": "http://localhost:8000/media/pdf/filled_forms/db88c1fc18a54b62836bd04a25ae93b8.pdf"
}
```

First thing to notice in the above request is the request URI. You can see filled in pdf is a child resource of a PDF form resource. The call itself then does the following:

* Creates a new filled in PDF form resource by filling in existing parent pdf form resource
* Stores the resulted PDF file

## Storage

For simplicity and scalability, FormSlayer uses [`django-storages`](https://django-storages.readthedocs.org/en/latest/) with AWS [S3](http://aws.amazon.com/s3/) backend to store both static and media (e.g. uploaded PDF) files. In additional, FormSlayer uses different S3 buckets for static and media files.

## Docker

As mentioned earlier, FormSlayer is meant to be used as a micro-service which makes Docker an ideal platform to use. FormSlayer can be used right out of the box via [`miki725/formslayer` dockerhub](https://registry.hub.docker.com/u/miki725/formslayer/) container. You can find the [`Dockerfile`](https://github.com/miki725/formslayer/blob/master/Dockerfile) used to build image within the [repo](https://github.com/miki725/formslayer/blob/master/Dockerfile).

FormSlayer uses environment for configuring it at run-time. Here is a blank sample docker environment variables file:

```
DJANGO_SETTINGS_MODULE=formslayer.settings.prod
ALLOWED_HOSTS=*
SECRET_KEY=

AWS_S3_ACCESS_KEY_ID=
AWS_S3_SECRET_ACCESS_KEY=
AWS_S3_STATIC_STORAGE_BUCKET_NAME=
AWS_S3_MEDIA_STORAGE_BUCKET_NAME=

DATABASE_HOST=postgres
DATABASE_PORT=5432
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=

EMAIL_HOST=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

NEW_RELIC_LICENSE_KEY=
NEW_RELIC_APP_NAME=

OPBEAT_ORGANIZATION_ID=
OPBEAT_APP_ID=
OPBEAT_SECRET_TOKEN=
```
