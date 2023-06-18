provider "google" {
  credentials = file("C:/Users/Krishna/Desktop/K8/cloudsummer23-08f57c1337e1.json")
  project     = "cloudsummer23"
  region      = "us-central1-a"
}

resource "google_container_cluster" "cluster" {
  name               = "assignmentkrishnak8"
  location           = "us-central1-a"
  initial_node_count = 1

  node_config {
    machine_type  ="e2-medium"
    disk_size_gb  = 10
    image_type    = "COS_CONTAINERD"
    disk_type     = "pd-standard"
  }
}
