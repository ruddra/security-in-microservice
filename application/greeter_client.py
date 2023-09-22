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

import logging
import time
import consul
import grpc
from grpc_generated import helloworld_pb2
from grpc_generated import helloworld_pb2_grpc

CONSUL_HOST = "consul"
CONSUL_PORT = 8500
GRPC_HOST = "grpc-server"
GRPC_PORT = 50051


def resolve_service():
    c = consul.Consul(host=CONSUL_HOST, port=CONSUL_PORT)
    service = c.agent.services().get(f'{GRPC_HOST}-{GRPC_PORT}')
    if service:
        return service["Address"], service["Port"]
    print("Consul failed")
    return GRPC_HOST, GRPC_PORT
    # index = None
    # while True:
    #     data = c.kv.get(, index=index)
    #     print(data)


def run():
    print("Will try to call internal service")
    server, port = resolve_service()
    with grpc.insecure_channel(f"{server}:{port}/grpc_server") as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        while True:
            response = stub.SayHello(helloworld_pb2.HelloRequest(name="you"))
            print("Greeter client received: " + response.message)
            time.sleep(30)


if __name__ == "__main__":
    logging.basicConfig()
    run()
