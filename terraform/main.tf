terraform {
  backend "s3" {
    bucket = "tf-remote-state20230406220833131500000002"
    # key            = "production/terraform.tfstate" - PROVIDED AS A TF_CLI_ARGS_init VARIABLE
    region         = "eu-north-1"
    encrypt        = true
    kms_key_id     = "dca8ba1b-a9cb-4f06-be83-4ce544268760"
    dynamodb_table = "tf-remote-state-lock"
  }
}

provider "aws" {
  region = "eu-north-1"
}

resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_lambda_function" "lambda" {
  filename      = "lambda_function_payload.zip"
  function_name = "wappufiilis_bot_lambda"
  role          = "${aws_iam_role.iam_for_lambda.arn}"
  handler       = "bot.lambda_handler"

  runtime = "python3.9"

  # The filebase64sha256() function is available in Terraform 0.11.12 and later
  # For Terraform 0.11.11 and earlier, use the base64sha256() function and the file() function:
  # source_code_hash = "${base64sha256(file("lambda_function_payload.zip"))}"
  source_code_hash = "${filebase64sha256("lambda_function_payload.zip")}"

  environment {
    variables = {
      TOKEN = var.telegram_token
      TIMEZONE = "Europe/Helsinki"
      DATABASE_URL="postgres://a@b:c/d"
    }
  }
  depends_on = [aws_iam_role_policy_attachment.lambda_logs, aws_cloudwatch_log_group.example]
}

# This is to optionally manage the CloudWatch Log Group for the Lambda Function.
# If skipping this resource configuration, also add "logs:CreateLogGroup" to the IAM policy below.
resource "aws_cloudwatch_log_group" "example" {
  name              = "/aws/lambda/wappufiilis_bot_lambda"
  retention_in_days = 14
}

# See also the following AWS managed policy: AWSLambdaBasicExecutionRole
resource "aws_iam_policy" "lambda_logging" {
  name        = "lambda_logging"
  path        = "/"
  description = "IAM policy for logging from a lambda"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*",
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = "${aws_iam_role.iam_for_lambda.name}"
  policy_arn = "${aws_iam_policy.lambda_logging.arn}"
}

resource "random_id" "random_path" {
  byte_length = 16
}

resource "random_id" "id" {
  byte_length = 16
}

resource "aws_apigatewayv2_api" "api" {
  name          = "api-${random_id.id.hex}"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "api" {
  api_id           = aws_apigatewayv2_api.api.id
  integration_type = "AWS_PROXY"

  integration_method     = "POST"
  integration_uri        = aws_lambda_function.lambda.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "api" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "ANY /${random_id.random_path.hex}/{proxy+}"

  target = "integrations/${aws_apigatewayv2_integration.api.id}"
}

resource "aws_apigatewayv2_stage" "api" {
  api_id      = aws_apigatewayv2_api.api.id
  name        = "$default"
  auto_deploy = true
}

# give permission to call the lambda
resource "aws_lambda_permission" "apigw" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda.arn
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.api.execution_arn}/*/*"
}

data "httpclient_request" "webhook_register" {
  url = "https://api.telegram.org/bot${var.telegram_token}/setWebhook?url=${aws_apigatewayv2_api.api.api_endpoint}/${random_id.random_path.hex}/"
}