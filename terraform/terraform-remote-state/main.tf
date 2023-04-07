terraform {
  backend "s3" {
    bucket = "tf-remote-state20230406220833131500000002"
    key            = "this-remote-state-bucket/terraform.tfstate"
    region         = "eu-north-1"
    encrypt        = true
    kms_key_id     = "dca8ba1b-a9cb-4f06-be83-4ce544268760"
    dynamodb_table = "tf-remote-state-lock"
  }
}

provider "aws" {
  region = "eu-north-1"
}

provider "aws" {
  alias  = "replica"
  region = "eu-west-1"
}

module "remote_state" {
  source = "nozaq/remote-state-s3-backend/aws"

  providers = {
    aws         = aws
    aws.replica = aws.replica
  }
}

resource "aws_iam_user" "terraform" {
  name = "TerraformUser"
}

resource "aws_iam_user_policy_attachment" "remote_state_access" {
  user       = aws_iam_user.terraform.name
  policy_arn = module.remote_state.terraform_iam_policy.arn
}