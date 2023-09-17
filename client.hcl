plugin "raw_exec" {
  config {
    enabled = true
  }
}

bind_addr = "0.0.0.0"
datacenter = "local"

// acl {
//   enabled = true
//   token_ttl = "30s"
//   policy_ttl = "60s"
// }

// ports {
//   grpc = 50051
// }

// connect {
//   enabled = true
// }

server {
  # license_path is required as of Nomad v1.1.1+
  # license_path = "/etc/nomad.d/nomad.hcl"
  enabled = true
  bootstrap_expect = 1
}

client {
  enabled = true
  servers = ["127.0.0.1"]
}

consul {
  address = "127.0.0.1:8500"
  server_service_name = "nomad-server"
  client_service_name = "nomad-client"
  auto_advertise      = true
  server_auto_join    = true
  client_auto_join    = true
  token   = "redacted"
}