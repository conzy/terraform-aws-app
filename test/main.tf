module "test" {
  source = "../"
  name   = "terraform_test"
}

output "function_arn" {
  value = module.test.lambda_arn
}
