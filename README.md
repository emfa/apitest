# API Test Project

This project is designed to execute API tests defined in a JSON file and save the results to an Excel file.

## Prerequisites

- Python 3.x
- `pip` (Python package installer)

## Setup

1. Clone the repository or download the project files to your local machine.

2. Navigate to the project directory:
    ```sh
    cd /API_test
    ```

3. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

## Running the Tests

1. Ensure that the `api_tests.json` file is present in the project directory. This file should contain the API test cases.

2. Run the `apitest.py` script:
    ```sh
    python apitest.py
    ```

3. After the script completes, the test results will be saved to `api_test_results.xlsx` in the project directory.

## Project Structure

- `apitest.py`: Main script to execute API tests and save results to an Excel file.
- `requirements.txt`: List of required Python packages.
- `api_tests.json`: JSON file containing the API test cases.
- `api_test_results.xlsx`: Output Excel file with the test results (generated after running the script).

## Example `api_tests.json`

Here is an example of how the `api_tests.json` file should look:

```json
{
    "tests": [
        {
            "name": "Test GET User",
            "method": "GET",
            "url": "https://jsonplaceholder.typicode.com/users/1",
            "headers": {},
            "body": null,
            "expected_status_code": 200
        },
        {
            "name": "Test POST Create User",
            "method": "POST",
            "url": "https://jsonplaceholder.typicode.com/posts",
            "headers": {
                "Content-Type": "application/json"
            },
            "body": {
                "title": "foo",
                "body": "bar",
                "userId": 1
            },
            "expected_status_code": 201
        }
    ]
}
```

## Notes

- Ensure that the URLs in the `api_tests.json` file are accessible from your network.
- You can modify the `api_tests.json` file to include your own API test cases.

## License

This project is licensed under the MIT License.