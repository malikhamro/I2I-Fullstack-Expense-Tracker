#!/bin/bash

# Unit tests for deploy_docker.sh script

# Include error handling
set -euo pipefail

# Testing if the deploy_docker.sh script exists
if [[ ! -f ../deployment_scripts/deploy_docker.sh ]]; then
  echo "deploy_docker.sh script not found!"
  exit 1
fi

# Mocking environment variables commonly used in deploy_docker.sh
export DOCKER_IMAGE_TAG="latest"
export DEPLOY_ENV="staging"
export DOCKER_NETWORK="app_network"
export CONTAINER_NAME="app_container"

# Helper function to assert expected output
assert_equals() {
  local expected=$1
  local actual=$2
  if [[ "$expected" != "$actual" ]]; then
    echo "Assertion failed: Expected '$expected' but got '$actual'"
    exit 1
  fi
}

# Test function for successful deployment
test_successful_deployment() {
  echo "Running test for successful deployment..."

  # Mocking docker run command 
  function docker() {
    if [[ "$1" == "run" ]]; then
      echo "Docker container deployed"
    fi
  }

  # Run the script and capture the output
  output=$(../deployment_scripts/deploy_docker.sh 2>&1)
  expected_output="Docker container deployed"

  # Validate output
  assert_equals "$expected_output" "$output"

  echo "Test for successful deployment passed."
}

# Test function for missing environment variables
test_missing_env_variables() {
  echo "Running test for missing environment variables..."

  # Unset one of the environment variables
  unset DOCKER_IMAGE_TAG
  
  # Run the script and capture the output
  if output=$(../deployment_scripts/deploy_docker.sh 2>&1); then
    echo "Test failed: Expected error for missing environment variable, but script executed successfully."
    exit 1
  else
    expected_error="DOCKER_IMAGE_TAG not set"
    # Check if expected error message is in output
    if [[ "$output" != *"$expected_error"* ]]; then
      echo "Test failed: Expected '$expected_error' but got '$output'"
      exit 1
    fi
  fi

  echo "Test for missing environment variables passed."
}

# Reset environment variables for other tests
export DOCKER_IMAGE_TAG="latest"

# Run all tests
test_successful_deployment
test_missing_env_variables

echo "All tests passed."
