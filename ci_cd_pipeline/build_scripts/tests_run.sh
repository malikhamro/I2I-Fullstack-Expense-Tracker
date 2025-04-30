#!/bin/bash

# Script: tests_run.sh
# Purpose: Script to execute unit tests for the microservices
# Author: Your Name
# Created Date: YYYY-MM-DD
# Description: This script is designed to execute all unit tests for the microservices.
# It ensures that any issues with the code are identified before deployment.

# Function to execute tests and handle errors
execute_tests() {
  echo "Starting the execution of unit tests..."

  # Run all unit tests
  if ! ./gradlew test; then
    echo "Unit tests failed! Please check the test results."
    exit 1
  fi

  echo "Unit tests completed successfully."
}

# Main script execution
{
  execute_tests
} || {
  echo "An unexpected error occurred during the execution of the tests."
  exit 1
}

echo "Unit test script execution completed."
