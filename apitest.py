from os import path
import requests
import json
import time
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Side
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
    description = test_case.get('description', 'NA')
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
            "Description": description,
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

def format_excel_sheet(ws,headers):

    # Formatting: Bold headers
    for col in ws.iter_cols(min_row=1, max_row=1, max_col=len(headers)):
        for cell in col:
            cell.font = cell.font.copy(bold=True)

    # Auto-adjust column widths and apply word-wrap to cells
    for col in ws.columns:
        max_length = 0
        col_letter = col[0].column_letter
        for cell in col:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
                cell.alignment = Alignment(
                    wrap_text=True,
                    vertical="top",
                    horizontal="left"
                )
            except:
                pass
        
        ws.column_dimensions[col_letter].width = min(max_length + 2,50)

    # Set a fixed row height for all rows
    fixed_row_height = 100
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
        ws.row_dimensions[row[0].row].height = fixed_row_height

    # Add borders to all cells
    thin_border = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin")
    )
    for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=len(headers)):
        for cell in row:
            cell.border = thin_border


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

    # Write Headers
    headers = list(results[0].keys())
    ws.append(headers)

    # Write data
    for result in results:
        ws.append(list(result.values()))

    # Format the Excel sheet
    format_excel_sheet(ws, headers)

    # Save file
    wb.save(output_file)
    print(f"Test results saved to {output_file}")

def run(input_file_name, output_file_name="api_test_results.xlsx"):

    input_file_path = path.join(path.dirname(path.abspath(__file__)),'testfiles', input_file_name)

    # Load test cases from the input JSON file
    test_cases = load_test_cases(input_file_path)

    output_file_path = path.join(path.dirname(path.abspath(__file__)),'results', output_file_name)

    # Execute each test case and collect the results in parallel
    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor() as executor:
        test_results = list(executor.map(execute_test_case, test_cases))

    # Write the collected test results to an Excel file
    write_results_to_excel(test_results, output_file_path)

if __name__ == "__main__":
    pass