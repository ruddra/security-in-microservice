build:
	docker build . -t akshilt/grpcserver

create-network:
	docker network create simc-net 

run-server:
	docker run --rm --net simc-net  --name grpc_server grpcserver greeter_server.py 

run-client:
	docker run --rm --net simc-net  --name grpc_client grpcserver greeter_client.py

dump-docker:
	docker save grpcserver > grpc.tar

nomad-agent:
	nomad agent -dev -config="./client.hcl"

consul-agent:
	consul agent -dev

nomad-job:
	nomad job run -var-file=config.var config.nomad.hcl

                                                                                                                                                                     