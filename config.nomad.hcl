
variable "service_root_dir" {
    type = string
}

job "simc" {
  datacenters = ["local"]
  group "server" {
    // network {
    //   mode = "bridge"
    // }

    service {
      name = "grpcserver"
      tags = [
        "gprc_server"
      ]
    //   port = "50051"
    }
    task "grpcserver" {   
        driver = "raw_exec"
        config {
            command = "powershell"
            // ports = ["rpc"]
            args = ["local/prestart.ps1"]
        }

        template {
            data = <<EOF
cd {{ env  "service_root_dir" }}
. ./.venv/Scripts/Activate.ps1
python ./application/greeter_server.py
EOF

            destination = "local/prestart.ps1"
        }

        env {
            service_root_dir = var.service_root_dir
        }

        resources {
            cpu    = 2000
            memory = 2000
        }

    }
  }

  group "client" {
    // network {
    //   mode = "bridge"
    // }
    
    service {
      name = "grpcclient"
      tags = [
        "gprc_client"
      ]
    }
    task "grpcclient" {   
        driver = "raw_exec"
        config {
            command = "powershell"
            // ports = ["rpc"]
            args = ["local/start.ps1"]
        }

        template {
            data = <<EOF
cd {{ env  "service_root_dir" }}
. ./.venv/Scripts/Activate.ps1
python ./application/greeter_client.py
EOF

            destination = "local/start.ps1"
        }

        env {
            service_root_dir = var.service_root_dir
        }

        resources {
            cpu    = 2000
            memory = 2000
        }
    }
  }


}