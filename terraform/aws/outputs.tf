output "instance_public_ip" {
  description = "Public IP address of the HealthWise instance"
  value       = aws_instance.healthwise_instance.public_ip
}