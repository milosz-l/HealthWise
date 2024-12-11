resource "aws_iam_role" "ec2_role" {
  name = "healthwise-ec2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecr_access" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "healthwise-ec2-profile"
  role = aws_iam_role.ec2_role.name
}

resource "aws_security_group" "healthwise_sg" {
  name        = "healthwise-sg"
  description = "Allow traffic to backend and frontend"

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # TODO: Be more restrictive in production
  }

  ingress {
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # TODO: Be more restrictive in production
  }

  # Add SSH rule for EC2 Instance Connect (less secure)
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Allows SSH from anywhere - not recommended for production
  }

  # # TODO: Add SSH rule for EC2 Instance Connect (more secure - using prefix list)
  # ingress {
  #   from_port       = 22
  #   to_port         = 22
  #   protocol        = "tcp"
  #   prefix_list_ids = [data.aws_vpc_prefix_list.ec2_instance_connect.id]
  # }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# # TODO: Data source to get the EC2 Instance Connect prefix list ID (for more secure SSH rule)
# data "aws_vpc_prefix_list" "ec2_instance_connect" {
#   filter {
#     name   = "prefix-list-name"
#     values = ["com.amazonaws.${var.region}.ec2-instance-connect"]
#   }
# }

resource "aws_instance" "healthwise_instance" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  key_name               = var.key_name
  vpc_security_group_ids = [aws_security_group.healthwise_sg.id]
  iam_instance_profile   = aws_iam_instance_profile.ec2_profile.name

  user_data = <<-EOF
              #!/bin/bash
              sudo apt update
              sudo apt install -y docker.io
              sudo apt install -y docker-compose

              # Install AWS CLI
              curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip"
              sudo apt install unzip
              unzip -o awscliv2.zip
              sudo ./aws/install

              sudo systemctl start docker
              sudo systemctl enable docker

              # Login to ECR
              aws ecr get-login-password --region ${var.region} | sudo docker login --username AWS --password-stdin ${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.region}.amazonaws.com

              # Create docker-compose.yml file
              cat <<-'DOCKERCOMPOSE' > docker-compose.yml
              version: "3.8"
              services:
                backend:
                  image: ${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.region}.amazonaws.com/healthwise-backend:latest
                  ports:
                    - "8000:8000"
                  environment:
                    - OPENAI_API_KEY=${var.openai_api_key}
                    - TAVILY_API_KEY=${var.tavily_api_key}
                    - MONGO_URI=${var.mongo_uri}
                    - MONGODB_DATABASE=${var.mongodb_database}
                frontend:
                  image: ${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.region}.amazonaws.com/healthwise-frontend:latest
                  ports:
                    - "8501:8501"
                  environment:
                    - CHATBOT_PASSWORD=${var.chatbot_password}
                    - HOTSPOTS_PASSWORD=${var.hotspots_password}
                  depends_on:
                    - backend
              DOCKERCOMPOSE

              # Run docker-compose
              sudo docker-compose up -d
              EOF

  tags = {
    Name = "HealthWise-Instance"
  }
}

data "aws_caller_identity" "current" {}