provider "aws" {
  region = "eu-north-1"
}

resource "aws_vpc" "analytics_vpc" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name        = "AnalyticsVPC"
    Environment = var.environment
  }
}

resource "aws_subnet" "analytics_subnet" {
  vpc_id            = aws_vpc.analytics_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "eu-north-1a"

  tags = {
    Name        = "AnalyticsSubnet"
    Environment = var.environment
  }
}

resource "aws_security_group" "analytics_sg" {
  name        = "analytics_sg_${var.environment}"
  description = "Allow traffic for analytics infrastructure"
  vpc_id      = aws_vpc.analytics_vpc.id

  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_dynamodb_table" "time_series_data" {
  name         = "FiilisData_${var.environment}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "partition_key"
  range_key    = "timestamp"

  attribute {
    name = "partition_key"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "N"
  }

}

resource "aws_dynamodb_table" "per_guild_data" {
  name         = "FiilisData_PerGuild_${var.environment}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "partition_key"
  range_key    = "timestamp"

  attribute {
    name = "partition_key"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "N"
  }

}

resource "aws_dynamodb_table" "per_year_data" {
  name         = "FiilisData_PerYear_${var.environment}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "partition_key"
  range_key    = "timestamp"

  attribute {
    name = "partition_key"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "N"
  }

}
