terraform {
  backend "gcs" {
    bucket = ""
  }
}

locals {
  project = "goodlittlescript-io-prd"
  appname = "gcp-django"
}


module "app" {
  source  = "../../modules/app"
  appname = local.appname
  project = local.project
}
