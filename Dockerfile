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
COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install -t /install -r requirements.txt

FROM base
COPY --from=builder /install /usr/local
RUN python -c 'import site; print(site.getsitepackages())'

