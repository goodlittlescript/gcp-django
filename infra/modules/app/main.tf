variable "project" {
  type = string
}

variable "appname" {
  type = string
}

locals {
  service                 = var.appname
  project                 = var.project
  location                = "us-central1"
  timezone                = "America/Denver"
  runtime_service_account = "rt-${local.service}@${local.project}.iam.gserviceaccount.com"
}

data "google_cloud_run_service" "service" {
  name     = local.service
  project  = local.project
  location = local.location
}

//
// Task
//

resource "google_cloud_tasks_queue" "service" {
  name     = data.google_cloud_run_service.service.name
  project  = data.google_cloud_run_service.service.project
  location = data.google_cloud_run_service.service.location
  retry_config {
    min_backoff = "600s"
  }
}

//
// Schedule
//

resource "google_cloud_scheduler_job" "service" {
  name             = data.google_cloud_run_service.service.name
  project          = data.google_cloud_run_service.service.project
  region           = data.google_cloud_run_service.service.location
  description      = "${local.service} scheduler"
  schedule         = "0 */8 * * *"
  time_zone        = local.timezone
  attempt_deadline = "60s"

  retry_config {
    retry_count = 1
  }

  http_target {
    http_method = "POST"
    uri         = "${data.google_cloud_run_service.service.status[0].url}/task"
    headers = {
      "Content-Type" = "application/json"
    }
    oidc_token {
      service_account_email = local.runtime_service_account
      audience = data.google_cloud_run_service.service.status[0].url
    }
  }
}
