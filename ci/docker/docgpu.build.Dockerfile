ARG DOCKER_IMAGE_BASE_BUILD=cr.ray.io/rayproject/oss-ci-base_gpu
FROM $DOCKER_IMAGE_BASE_BUILD

# Unset dind settings; we are using the host's docker daemon.
ENV DOCKER_TLS_CERTDIR=
ENV DOCKER_HOST=
ENV DOCKER_TLS_VERIFY=
ENV DOCKER_CERT_PATH=

SHELL ["/bin/bash", "-ice"]

COPY . .

RUN <<EOF
#!/bin/bash

DOC_TESTING=1 TRAIN_TESTING=1 TUNE_TESTING=1 ./ci/env/install-dependencies.sh

# TODO(amogkam): Remove when https://github.com/ray-project/ray/issues/36011 
# is resolved.
#
# TODO(scottjlee): Move datasets to train/data-test-requirements.txt 
# (see https://github.com/ray-project/ray/pull/38432/)
pip install transformers==4.30.2 datasets==2.14.0

pip install -Ur ./python/requirements/ml/dl-gpu-requirements.txt

EOF
