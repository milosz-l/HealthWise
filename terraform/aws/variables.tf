variable "region" {
  description = "AWS region"
  default     = "eu-central-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  default     = "t4g.micro" # Choose an appropriate instance type
}

variable "ami_id" {
  description = "AMI ID for the EC2 instance"
  default = "ami-02d9d83052ced9fdd" # Canonical, Ubuntu, 24.04, amd64 noble image
}

variable "key_name" {
  description = "Name of the SSH key pair to use for the instance"
  default = "healthwise-key-name" 
}

variable "openai_api_key" {
  description = "OpenAI API Key"
  type        = string
  sensitive   = true
}

variable "tavily_api_key" {
  description = "Tavily API Key"
  type        = string
  sensitive   = true
}

variable "mongo_uri" {
  description = "MongoDB Atlas Connection String"
  type        = string
  sensitive   = true
}

variable "mongodb_database" {
  description = "MongoDB Database Name"
  type        = string
}

variable "chatbot_password" {
  description = "Password for Chatbot access"
  type        = string
  sensitive   = true
}

variable "hotspots_password" {
  description = "Password for Disease Hotspots access"
  type        = string
  sensitive   = true
}