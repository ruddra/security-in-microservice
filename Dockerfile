FROM python:3.7-alpine as base

# install gcc and grpc dependencies
FROM base as builder
RUN apk add --update --no-cache \
    gcc \
    linux-headers \
    make \
    musl-dev \
    python3-dev \
    g++
ENV GRPC_PYTHON_VERSION 1.54.2
ENV PIP_TARGET=/install
RUN python -m pip install --upgrade pip
RUN pip install grpcio==${GRPC_PYTHON_VERSION} grpcio-tools==${GRPC_PYTHON_VERSION}

FROM base
ENV GRPC_PYTHON_VERSION 1.54.2
COPY --from=builder /install /usr/local
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

