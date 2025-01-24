import requests
import json
import time
from openpyxl import Workbook
from datetime import datetime


# Function to load test cases from a JSON file
def load_test_cases(file_path):
    with open(file_path, 'r') as f:
        try:
            return json.load(f)['tests']
        except KeyError:
            print(f"Error: 'tests' key not found in {file_path}")
            return []


# Function to execute an API test case
def execute_test_case(test_case):
    method = test_case['method']
    url = test_case['url']
    headers = test_case.get('headers', {})
    body = test_case.get('body', None)
    expected_status = test_case.get('expected_status_code', 200)  # Default to 200 OK if not provided

    try:
        # Measure response time
        start_time = time.time()
        response = requests.request(method, url, headers=headers, json=body, timeout=10)
        response_time = round((time.time() - start_time) * 1000, 2)  # ms

        # Prepare test result
        result = {
            "Test Name": test_case['name'],
            "HTTP Method": method,
            "Endpoint URL": url,
            "Request Headers": json.dumps(headers, indent=2),
            "Request Body": json.dumps(body, indent=2) if body else "N/A",
            "Expected Status Code": expected_status,
            "Actual Status Code": response.status_code,
            "Response Time (ms)": response_time,
            "Response Body": response.text,
            "Result": "Pass" if response.status_code == expected_status else "Fail",
            "Error Message": "N/A",
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except requests.exceptions.RequestException as e:
        # Handle errors
        result = {
            "Test Name": test_case['name'],
            "HTTP Method": method,
            "Endpoint URL": url,
            "Request Headers": json.dumps(headers, indent=2),
            "Request Body": json.dumps(body, indent=2) if body else "N/A",
            "Expected Status Code": expected_status,
            "Actual Status Code": "N/A",
            "Response Time (ms)": "N/A",
            "Response Body": "N/A",
            "Result": "Fail",
            "Error Message": str(e),
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    return result


# Function to write test results to an Excel file
def write_results_to_excel(results, output_file):
    """
    Write test results to an Excel file.

    Args:
        results (list): A list of dictionaries containing test results.
        output_file (str): The path to the output Excel file.

    Returns:
        None
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "API Test Results"

    # Write headers
    if not results:
        print("No results to write to Excel.")
        wb.save(output_file)
        return
    headers = list(results[0].keys())
    ws.append(headers)

    # Write data
    for result in results:
        ws.append(list(result.values()))

    # Save file
    wb.save(output_file)
    print(f"Test results saved to {output_file}")

def run(input_file_name, output_file_name="api_test_results.xlsx"):
    # Load test cases from the input JSON file
    test_cases = load_test_cases(input_file_name)

    # Execute each test case and collect the results in parallel
    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor() as executor:
        test_results = list(executor.map(execute_test_case, test_cases))

    # Write the collected test results to an Excel file
    write_results_to_excel(test_results, output_file_name)

if __name__ == "__main__":
    pass