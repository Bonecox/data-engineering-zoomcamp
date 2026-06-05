terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.6.0"
    }
  }
}

provider "google" {
    credentials = "./keys/my-creds.json"
  project = "terraform-demo-498400"
  region  = "us-west1"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "terraform-demo-498400"
  location      = "US"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 3
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}