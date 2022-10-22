locals {
  project = "goodlittlescript-io-dev"
  appname = "gcp-django"
}


module "app" {
  source  = "../../modules/app"
  appname = local.appname
  project = local.project
}
