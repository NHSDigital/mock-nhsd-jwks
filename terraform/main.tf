provider "apigee" {
  org          = var.apigee_organization
  access_token = var.apigee_token
}

terraform {
  backend "azurerm" {}

  required_providers {
    apigee = "~> 0.0"
    archive = "~> 1.3"
  }
}


module "{{ config.meta.service_name }}" {
  source                   = "github.com/NHSDigital/api-platform-service-module"
  name                     = "{{ config.meta.service_name }}"
  path                     = "{{ config.meta.service_base_path }}"
  apigee_environment       = var.apigee_environment
  proxy_type               = (var.force_sandbox || length(regexall("sandbox", var.apigee_environment)) > 0) ? "sandbox" : "live"
  namespace                = var.namespace
  make_api_product         = !(length(regexall("sandbox", var.apigee_environment)) > 0)
  api_product_display_name = length(var.namespace) > 0 ? "{{ config.meta.service_name }}${var.namespace}" : "{{ config.meta.product_display_name }}"
  api_product_description  = "{{ config.meta.product_description}}"
}
