import sys
import io
import pandas as pd
import sqlite3
from contextlib import contextmanager, redirect_stdout
import traceback

class CodeExecutor:
    def __init__(self):
        self.timeout = 10  # seconds

    def execute_code(self, user_code, problem_data):
        if problem_data['type'] == 'Python':
            return self.execute_python(user_code, problem_data)
        elif problem_data['type'] == 'SQL':
            return self.execute_sql(user_code, problem_data)
        else:  # Pandas
            return self.execute_pandas(user_code, problem_data)

    @contextmanager
    def capture_output(self):
        new_out = io.StringIO()
        old_out = sys.stdout
        try:
            sys.stdout = new_out
            yield sys.stdout
        finally:
            sys.stdout = old_out

    def execute_python(self, user_code, problem_data):
        try:
            # Create a namespace for execution
            namespace = {}
            
            # Execute the user's code
            with self.capture_output():
                exec(user_code, namespace)
            
            # Run test cases
            for test_case in problem_data['test_cases']:
                input_data = test_case['input']
                expected_output = test_case['output']
                
                # Get the main function name from the problem data
                func_name = problem_data['function_name']
                if func_name not in namespace:
                    return {
                        'success': False,
                        'error': f"Function '{func_name}' not found in your code"
                    }
                
                # Execute the function with test input
                actual_output = namespace[func_name](*input_data)
                
                if actual_output != expected_output:
                    return {
                        'success': False,
                        'error': f"Test case failed: Expected {expected_output}, got {actual_output}"
                    }
            
            return {'success': True}
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            }

    def execute_sql(self, user_code, problem_data):
        try:
            # Create in-memory SQLite database
            conn = sqlite3.connect(':memory:')
            
            # Load sample data from CSV
            for table_info in problem_data['sample_data']:
                df = pd.read_csv(table_info['file'])
                df.to_sql(table_info['table_name'], conn, index=False)
            
            # Execute user's query
            result_df = pd.read_sql_query(user_code, conn)
            
            # Compare with expected output
            expected_df = pd.read_csv(problem_data['expected_output'])
            
            # Check if results match
            if not result_df.equals(expected_df):
                return {
                    'success': False,
                    'error': "Query result doesn't match expected output"
                }
            
            return {'success': True}
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            }
        finally:
            conn.close()

    def execute_pandas(self, user_code, problem_data):
        try:
            # Load the sample data
            sample_data = {}
            for data_file in problem_data['sample_data']:
                df = pd.read_csv(data_file['file'])
                sample_data[data_file['variable_name']] = df
            
            # Create namespace with sample data
            namespace = {'pd': pd, **sample_data}
            
            # Execute user's code
            with self.capture_output():
                exec(user_code, namespace)
            
            # Get the result variable
            if 'result' not in namespace:
                return {
                    'success': False,
                    'error': "Your code must create a 'result' variable with the final DataFrame"
                }
            
            result_df = namespace['result']
            expected_df = pd.read_csv(problem_data['expected_output'])
            
            # Compare with expected output
            if not result_df.equals(expected_df):
                return {
                    'success': False,
                    'error': "Your result doesn't match the expected output"
                }
            
            return {'success': True}
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            }
