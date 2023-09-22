from concurrent import futures
import logging

import consul
import grpc
from grpc_reflection.v1alpha import reflection
from grpc_generated import helloworld_pb2
from grpc_generated import helloworld_pb2_grpc

CONSUL_HOST = "consul"
CONSUL_PORT = 8500
GRPC_HOST = "grpc-server"
GRPC_PORT = 50051


class Greeter(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        print("Received hello from client. Saying hi back!")
        return helloworld_pb2.HelloReply(message="Hello, %s!" % request.name)


def register():
    print("register started...")
    c = consul.Consul(host=CONSUL_HOST, port=CONSUL_PORT)
    check = consul.Check.tcp(CONSUL_HOST, CONSUL_PORT, "30s")

    c.agent.service.register(
        GRPC_HOST,
        f"{GRPC_HOST}-{GRPC_PORT}",
        address=GRPC_HOST,
        port=GRPC_PORT,
        check=check
    )
    print("services: " + str(c.agent.services()))


def serve():
    port = GRPC_PORT
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    # the reflection service will be aware of "Greeter" and "ServerReflection" services.
    SERVICE_NAMES = (
        helloworld_pb2.DESCRIPTOR.services_by_name['Greeter'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Server started, listening on {port}")
    try:
        register()
        print("Registered on consul")
    except Exception as e:
        print(f"Failed for reason {str(e)}")
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
