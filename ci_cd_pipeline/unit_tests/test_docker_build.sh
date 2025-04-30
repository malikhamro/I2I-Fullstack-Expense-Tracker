#!/bin/bash

# Filename: test_docker_build.sh
# Description: Unit tests for docker_build.sh script

# Exit on any error
set -e

# Path to the docker_build.sh script
DOCKER_BUILD_SCRIPT="../build_scripts/docker_build.sh"

# Function to assert the expected output and exit code of docker_build.sh
function assert_output_and_exit_code() {
    expected_output="$1"
    expected_exit_code="$2"

    output=$(./$DOCKER_BUILD_SCRIPT 2>&1)
    exit_code=$?

    if [[ "$output" != *"$expected_output"* ]]; then
        echo "FAILED: Expected output '$expected_output', but got '$output'"
        exit 1
    fi

    if [[ "$exit_code" -ne "$expected_exit_code" ]]; then
        echo "FAILED: Expected exit code '$expected_exit_code', but got '$exit_code'"
        exit 1
    fi

    echo "PASSED: $3"
}

# Test cases
function run_tests() {

    echo "Running unit tests for docker_build.sh..."

    # Test 1: Ensure the script executes without errors
    assert_output_and_exit_code "Docker build successful" 0 "Script executes without errors"

    # Additional test cases can be added here
    # e.g., simulate errors, check for specific output, etc.

    echo "All tests passed successfully"
}

# Invoke the tests
run_tests

# End of test_docker_build.sh
