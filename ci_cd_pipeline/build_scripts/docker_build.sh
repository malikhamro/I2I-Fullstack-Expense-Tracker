#!/bin/bash

# Script to build Docker images for the microservices

# Function to log error messages
log_error() {
  echo "[ERROR] $1"
  exit 1
}

# Function to log informational messages
log_info() {
  echo "[INFO] $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
  log_error "Docker is not installed. Please install Docker and try again."
fi

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
  log_error "Docker daemon is not running. Please start Docker and try again."
fi

# Function to build Docker images
build_docker_image() {
  local service_name=$1
  local dockerfile_path=$2
  local tag_name=$3

  # Validate input parameters
  if [[ -z "$service_name" ]] || [[ -z "$dockerfile_path" ]] || [[ -z "$tag_name" ]]; then
    log_error "Invalid input parameters. Usage: build_docker_image <service_name> <dockerfile_path> <tag_name>"
  fi

  # Build Docker image
  log_info "Building Docker image for $service_name..."
  docker build -t "$tag_name" -f "$dockerfile_path" . || log_error "Failed to build Docker image for $service_name"
  log_info "Successfully built Docker image for $service_name with tag $tag_name"
}

# Example usage
# Define services and their respective Dockerfiles and tags
services=(
  "service1:./services/service1/Dockerfile:service1:latest"
  "service2:./services/service2/Dockerfile:service2:latest"
)

# Loop through each service and build the Docker image
for service in "${services[@]}"; do
  IFS=':' read -r -a service_info <<< "$service"
  build_docker_image "${service_info[0]}" "${service_info[1]}" "${service_info[2]}"
done

log_info "All Docker images built successfully."
