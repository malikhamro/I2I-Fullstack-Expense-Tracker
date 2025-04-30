#!/bin/bash
# deploy_docker.sh
# Script to deploy Docker containers to the specified environment

set -e

# Function to log messages
log_message() {
    local MESSAGE=$1
    echo "$(date +"%Y-%m-%d %T") : ${MESSAGE}"
}

# Function to validate environment variables
validate_environment() {
    if [ -z "$DOCKER_IMAGE" ]; then
        log_message "ERROR: DOCKER_IMAGE environment variable not set."
        exit 1
    fi
    
    if [ -z "$DEPLOY_ENV" ]; then
        log_message "ERROR: DEPLOY_ENV environment variable not set."
        exit 1
    fi
}

# Function to deploy the Docker container
deploy_container() {
    log_message "Starting deployment of Docker container..."

    # Pull the Docker image from the registry
    log_message "Pulling Docker image: ${DOCKER_IMAGE}"
    docker pull ${DOCKER_IMAGE}

    # Stop and remove existing container if it exists
    if [ "$(docker ps -q -f name=my_application)" ]; then
        log_message "Stopping and removing existing Docker container..."
        docker stop my_application && docker rm my_application
    fi

    # Run the new container
    log_message "Running new Docker container..."
    docker run -d --name my_application -e "ENVIRONMENT=${DEPLOY_ENV}" ${DOCKER_IMAGE}

    log_message "Deployment successful!"
}

# Main script execution
log_message "Deploy Docker script started..."
validate_environment
deploy_container
log_message "Deploy Docker script completed."
