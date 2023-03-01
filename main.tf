resource "aws_iam_role" "app_role" {
  name               = "app_role"
  assume_role_policy = data.aws_iam_policy_document.lambda_trust.json
}

resource "aws_iam_role_policy_attachment" "app_role" {
  role       = aws_iam_role.app_role.id
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

data "aws_iam_policy_document" "lambda_trust" {
  statement {
    actions = [
      "sts:AssumeRole"
    ]

    principals {
      type = "Service"
      identifiers = [
        "lambda.amazonaws.com"
      ]
    }
  }
}

module "lambda" {
  source      = "./modules/lambda"
  runtime     = "python3.9"
  name        = var.name
  source_file = "${path.module}/main.py"
  lambda_role = aws_iam_role.app_role.arn
  tags        = {}
  environment_variables = {
    FOO = "bar"
  }
}
