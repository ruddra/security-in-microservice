# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function
import sys
import os
import logging
import time
import consul
import grpc
from grpc_generated import helloworld_pb2
from grpc_generated import helloworld_pb2_grpc

CONSUL_HOST = "consul"
CONSUL_PORT = 8500
# GRPC_HOST = "172.22.48.1"
GRPC_HOST = "localhost"
GRPC_PORT = 50051
GRPC_PATH = "/"
PRIVATE_CERT = "./ssl/server.crt"


def resolve_service():
    try:
        c = consul.Consul(host=CONSUL_HOST, port=CONSUL_PORT)
        service = c.agent.services().get(f'{GRPC_HOST}-{GRPC_PORT}')
        if service and not "external" in sys.argv:
            return service["Address"], service["Port"]
    except Exception as e:
        print(f"Consul failed or calling external: {str(e)}")
    return GRPC_HOST, GRPC_PORT


def get_credentials():
    with open(PRIVATE_CERT, 'rb') as f:
        return grpc.ssl_channel_credentials(f.read())


def get_channel(server, port):
    if "secured" in sys.argv:
        return grpc.secure_channel(f"{server}:{port}", get_credentials())
    return grpc.insecure_channel(f"{server}:{port}")


def get_response(stub):
    return stub.SayHello(helloworld_pb2.HelloRequest(name="you"))


def time_grpc_response(*args):
    import timeit
    for i in range(10):
        start_time = timeit.default_timer()
        counter = 0
        while counter < 100000:
            get_response(*args)
            counter += 1
        print(f"Attempt {i}: Time took {timeit.default_timer() - start_time}")


def run():
    print("Will try to call internal service")

    with get_channel(*resolve_service()) as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        if "timeit" in sys.argv:
            time_grpc_response(stub)
        else:
            while True:
                response = get_response(stub)
                print("Greeter client received: " + response.message)
                time.sleep(30)


if __name__ == "__main__":
    logging.basicConfig()
    run()
