import apitest

def main():
    file_name = 'api_tests.json'
    apitest.run(input_file_name=file_name,output_file_name="mfa_api_test_results.xlsx")

if __name__ == "__main__":
    main()