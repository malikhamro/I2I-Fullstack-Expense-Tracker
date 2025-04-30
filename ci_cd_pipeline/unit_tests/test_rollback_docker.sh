#!/bin/bash

# Unit test script for rollback_docker.sh script

# Include the script to be tested
source ../deployment_scripts/rollback_docker.sh

# Function to mock docker commands
mock_docker_command() {
    echo "Mock docker command executed: $*"
}

# Replace 'docker' command with the mock function during testing
alias docker=mock_docker_command

# Test function for successful rollback
test_successful_rollback() {
    echo "Testing successful rollback..."

    # Mock environment variables
    export PREVIOUS_VERSION="mock_previous_version"
    export CURRENT_VERSION="mock_current_version"
    export ROLLBACK_SUCCESS=true

    # Call the rollback function
    rollback_docker

    # Expected result
    expected="Mock docker command executed: run --rm -e PREVIOUS_VERSION=mock_previous_version -e CURRENT_VERSION=mock_current_version rollback_docker_container"

    if [[ $output == $expected ]]; then
        echo "Success: Rollback executed as expected"
        return 0
    else
        echo "Failure: Rollback did not execute as expected"
        return 1
    fi
}

# Test function for unsuccessful rollback due to missing environment variables
test_rollback_missing_env_vars() {
    echo "Testing rollback with missing environment variables..."

    # Unset the necessary environment variables
    unset PREVIOUS_VERSION
    unset CURRENT_VERSION

    # Capture the output
    output=$(rollback_docker 2>&1)

    # Expected result
    expected="Error: Missing environment variables"

    if [[ $output == *$expected* ]]; then
        echo "Success: Proper error message displayed"
        return 0
    else
        echo "Failure: Error message not displayed as expected"
        return 1
    fi
}

# Test function for unsuccessful rollback due to docker command failure
test_rollback_docker_failure() {
    echo "Testing rollback with docker command failure..."

    # Mock environment variables
    export PREVIOUS_VERSION="mock_previous_version"
    export CURRENT_VERSION="mock_current_version"
    export ROLLBACK_SUCCESS=false

    # Capture the output
    output=$(rollback_docker 2>&1)

    # Expected result
    expected="Error: Docker command failed"

    if [[ $output == *$expected* ]]; then
        echo "Success: Correct error message for docker command failure"
        return 0
    else
        echo "Failure: Error message not displayed for docker command failure"
        return 1
    fi
}

# Run all tests
run_all_tests() {
    test_successful_rollback
    test_rollback_missing_env_vars
    test_rollback_docker_failure
}

# Execute the tests
run_all_tests
