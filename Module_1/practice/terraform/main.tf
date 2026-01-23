terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.16.0"
    }
  }
}

provider "google" {
  project     = "de-zoomcamp-485104"
  region      = "us-central1"
} 

resource "google_storage_bucket" "demo-bucket" {
  name          = "de-zoomcamp-485104-bucket"
  location      = "US"

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}