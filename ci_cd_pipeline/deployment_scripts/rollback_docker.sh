#!/bin/bash

# rollback_docker.sh
# Script to rollback Docker containers to the previous stable version in case of deployment failure

# Exit immediately if any command exits with a non-zero status
set -e

# Constants
CONTAINER_NAME="my-app"  # Change to the appropriate container name
PRIOR_IMAGE_TAG=":previous"  # Tag used for previous stable image
DOCKER_REGISTRY_URL="yourdockerregistry.io"  # Change to your Docker registry URL if necessary
DOCKER_NETWORK="my-app-network"  # Change to the appropriate Docker network if necessary
ROLLBACK_LOG_FILE="rollback.log"

# Function to log rollback actions
log() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') - $1" | tee -a "$ROLLBACK_LOG_FILE"
}

# Function to check if a container is running
is_container_running() {
    docker ps --filter "name=$CONTAINER_NAME" --filter "status=running" --format "{{.ID}}" | grep -q .
}

# Function to pull the previous stable image
pull_previous_image() {
    local image="${DOCKER_REGISTRY_URL}/${CONTAINER_NAME}${PRIOR_IMAGE_TAG}"
    log "Pulling previous stable image: $image"
    docker pull "$image"
}

# Function to stop the current container
stop_current_container() {
    if is_container_running; then
        log "Stopping running container: $CONTAINER_NAME"
        docker stop "$CONTAINER_NAME"
        docker rm "$CONTAINER_NAME"
    else
        log "No running container found to stop."
    fi
}

# Function to start the container with the previous image
start_previous_container() {
    local image="${DOCKER_REGISTRY_URL}/${CONTAINER_NAME}${PRIOR_IMAGE_TAG}"
    log "Starting container with previous stable image: $image"
    docker run -d --name "$CONTAINER_NAME" --network "$DOCKER_NETWORK" "$image"
}

# Main rollback process
main() {
    log "Starting rollback process..."
    pull_previous_image
    stop_current_container
    start_previous_container
    log "Rollback process completed successfully."
}

# Error handling
trap 'log "An error occurred. Check previous log statements for details."; exit 1' ERR

# Execute the main function
main
