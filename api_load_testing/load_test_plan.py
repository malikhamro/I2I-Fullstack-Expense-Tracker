import json
import time
import random
import requests
from datetime import datetime


def generate_test_data(api_endpoint: str):
    """Generate realistic test data for the given API endpoint."""
    test_data = []
    for i in range(100):  # Generate 100 different payloads for testing
        payload = {
            "user_id": f"user_{random.randint(1, 1000)}",
            "action": random.choice(["create", "update", "delete"]),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "data": {"info": f"Test data {i}"}
        }
        test_data.append(payload)
    return test_data


def create_load_test_scenarios():
    """Define and structure various load testing scenarios."""
    scenarios = {
        "peak_load": {
            "description": "Simulate peak load on the API",
            "data": generate_test_data("/api/peak_load"),
            "expected_outcomes": {
                "response_time": "< 2 seconds",
                "error_rate": "< 1%"
            }
        },
        "endurance_test": {
            "description": "Simulate continuous load for an extended period",
            "data": generate_test_data("/api/endurance_test"),
            "expected_outcomes": {
                "response_time": "< 2 seconds",
                "error_rate": "< 5%"
            }
        },
        "stress_test": {
            "description": "Simulate stress conditions beyond normal operational capacity",
            "data": generate_test_data("/api/stress_test"),
            "expected_outcomes": {
                "response_time": "< 5 seconds",
                "error_rate": "< 10%"
            }
        }
    }
    return scenarios


def send_api_request(method: str, url: str, data: dict, headers=None):
    """Send the API request and return the response."""
    try:
        if method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method.upper() == "GET":
            response = requests.get(url, params=data, headers=headers)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data, headers=headers)
        elif method.upper() == "DELETE":
            response = requests.delete(url, json=data, headers=headers)
        else:
            raise ValueError(f"Unsupported method: {method}")
        response.raise_for_status()  # Raise an error for bad HTTP status code
        return response
    except requests.RequestException as e:
        return {"error": str(e)}


def log_test_metrics(filename: str, record: dict):
    """Log the test metrics to a specified file."""
    with open(filename, "a") as f:
        f.write(json.dumps(record) + "\n")


def execute_load_tests():
    """Execute the defined load tests and monitor performance."""
    scenarios = create_load_test_scenarios()
    metrics_log = "load_test_metrics.log"
    headers = {
        "Content-Type": "application/json"
    }

    for scenario_name, scenario in scenarios.items():
        print(f"Executing scenario: {scenario_name}")
        start_time = time.time()
        response_times = []
        error_count = 0

        for payload in scenario["data"]:
            response = send_api_request("POST", "https://api.testing.com" + payload["action"], payload, headers)
            if type(response) is dict and response.get("error"):
                error_count += 1
                log_test_metrics(metrics_log, {"scenario": scenario_name, "error": response["error"]})
            else:
                response_time = response.elapsed.total_seconds()
                response_times.append(response_time)
                log_test_metrics(metrics_log, {
                    "scenario": scenario_name,
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "response_time": response_time
                })

        end_time = time.time()
        total_duration = end_time - start_time
        avg_response_time = sum(response_times) / len(response_times) if response_times else float('inf')
        error_rate = (error_count / len(scenario["data"])) * 100

        print(f"Scenario '{scenario_name}' executed in {total_duration:.2f} seconds with average response time: {avg_response_time:.2f} seconds and error rate: {error_rate:.2f}%")

        log_test_metrics(metrics_log, {
            "scenario": scenario_name,
            "total_duration": total_duration,
            "avg_response_time": avg_response_time,
            "error_rate": error_rate
        })


def analyze_test_results(metrics_log: str):
    """Process collected data and identify bottlenecks or failure points."""
    with open(metrics_log, "r") as f:
        metrics = [json.loads(line) for line in f.readlines()]

    summary = {}
    for record in metrics:
        scenario = record["scenario"]
        if scenario not in summary:
            summary[scenario] = {
                "total_tests": 0,
                "total_duration": 0,
                "total_response_time": 0,
                "total_errors": 0
            }
        summary[scenario]["total_tests"] += 1
        summary[scenario]["total_duration"] += record.get("total_duration", 0)
        summary[scenario]["total_response_time"] += record.get("response_time", 0)
        if "error" in record:
            summary[scenario]["total_errors"] += 1

    for scenario, data in summary.items():
        avg_response_time = data["total_response_time"] / data["total_tests"] if data["total_tests"] else float('inf')
        error_rate = (data["total_errors"] / data["total_tests"]) * 100 if data["total_tests"] else float('inf')
        print(f"Scenario '{scenario}' - Avg Response Time: {avg_response_time:.2f}s, Error Rate: {error_rate:.2f}%")
        expected_outcomes = create_load_test_scenarios()[scenario]["expected_outcomes"]
        print(f"Expected Response Time: {expected_outcomes['response_time']}, Expected Error Rate: {expected_outcomes['error_rate']}")
