FROM python:3.10-slim
ARG HITFACTORPY_VERSION=latest

RUN pip install "hitfactorpy==$HITFACTORPY_VERSION"

ENTRYPOINT [ "python", "-m", "hitfactorpy" ]
