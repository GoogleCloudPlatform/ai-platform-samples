resource "random_id" "instance_id" {
  byte_length = 8
}

resource "google_compute_instance" "default" {
  name         = "vm-${random_id.instance_id.hex}"
  machine_type = "n1-standard-4"
  zone         = "us-central1-b"

  boot_disk {
    initialize_params {
      image = "deeplearning-platform-release/tf-ent-latest-gpu"
      size = 50 // 50 GB Storage
    }
  }

  network_interface {
    network = "default"
    access_config {
      // Include this section to give the VM an external ip address
    }
  }

  guest_accelerator {
    type = "nvidia-tesla-t4"
    count = 1

  }

  scheduling {
    automatic_restart = true
    on_host_maintenance = "TERMINATE"
  }


  metadata = {
    install-nvidia-driver = true
    proxy-mode = "project_editors"
  }

  // Apply the firewall rule to allow external IPs to access this instance
  tags = ["deeplearning-vm"]

  service_account {
    scopes = ["https://www.googleapis.com/auth/cloud-platform"]
  }
}


resource "google_compute_firewall" "jupyterlab" {
  name    = "default-allow-jupyterlab"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["8080"]
  }

  // Allow traffic from everywhere to instances with an jupyterlab tag
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["jupyterlab"]
}

output "ip" {
  value = "${google_compute_instance.default.network_interface.0.access_config.0.nat_ip}"
}
