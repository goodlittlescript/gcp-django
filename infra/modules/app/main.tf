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

  rate_limits {
    max_concurrent_dispatches = 3
    max_dispatches_per_second = 2
  }

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
      audience              = data.google_cloud_run_service.service.status[0].url
    }
  }
}

//
// Dataset
//

resource "google_bigquery_table" "service" {
  for_each = toset([
    "requests"
  ])
  project    = local.project
  dataset_id = replace(local.service, "/\\W/", "_")
  table_id   = each.value

  time_partitioning {
    type  = "DAY"
    field = "extracted_at"
  }

  schema = <<EOF
[
   {
    "name": "uuid",
    "type": "STRING",
    "mode": "REQUIRED",
    "description": "A uuid assigned to each record"
  },
  {
    "name": "extracted_at",
    "type": "TIMESTAMP",
    "mode": "REQUIRED",
    "description": "The extraction time (partitioning field)"
  },
  {
    "name": "metadata",
    "type": "JSON",
    "mode": "NULLABLE",
    "description": "Metadata blob"
  },
  {
    "name": "data",
    "type": "JSON",
    "mode": "REQUIRED",
    "description": "Data blob"
  }
]
EOF
}