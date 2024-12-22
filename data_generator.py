import json
import os
from typing import Dict, Any, List
import pandas as pd
from datetime import datetime
import uuid

class DataGenerator:
    def __init__(self):
        self.data_dir = "data/generated"
        self.ensure_directories()
        
    def ensure_directories(self):
        """Create necessary directories if they don't exist."""
        directories = [
            "data/generated/python",
            "data/generated/sql",
            "data/generated/pandas",
            "data/templates"
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    def generate_problem_data(self, problem_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Generate all necessary data for a problem."""
        problem_type = problem_spec['type']
        
        if problem_type == 'SQL':
            return self._generate_sql_data(problem_spec)
        elif problem_type == 'Pandas':
            return self._generate_pandas_data(problem_spec)
        else:  # Python
            return self._generate_python_data(problem_spec)

    def _generate_sql_data(self, problem_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Generate SQL tables and sample data."""
        problem_id = str(uuid.uuid4())
        schema = problem_spec['schema']
        
        # Generate data for each table
        table_files = {}
        for table_spec in schema:
            # Create prompt for data generation
            dataset_specs = {
                'table_name': table_spec['table_name'],
                'columns': table_spec['columns'],
                'parameters': table_spec['sample_data_parameters']
            }
            
            # Get data from LLM
            csv_content = llm_response(DATASET_GENERATION_TEMPLATE.format(
                dataset_specs=json.dumps(dataset_specs, indent=2)
            ))
            
            # Save to file
            filename = f"{self.data_dir}/sql/{problem_id}_{table_spec['table_name']}.csv"
            with open(filename, 'w') as f:
                f.write(csv_content)
            
            table_files[table_spec['table_name']] = filename
            
        # Generate expected output data
        expected_output = llm_response(f"""
        Given the problem: {problem_spec['task']}
        Generate the expected output data that would result from the correct SQL query.
        Return only the CSV content with header row.
        """)
        
        output_file = f"{self.data_dir}/sql/{problem_id}_expected.csv"
        with open(output_file, 'w') as f:
            f.write(expected_output)
            
        return {
            'problem_id': problem_id,
            'table_files': table_files,
            'expected_output': output_file
        }

    def _generate_pandas_data(self, problem_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Pandas datasets."""
        problem_id = str(uuid.uuid4())
        datasets = problem_spec['datasets']
        
        dataset_files = {}
        for dataset_spec in datasets:
            # Create prompt for data generation
            generation_params = {
                'name': dataset_spec['name'],
                'columns': dataset_spec['columns'],
                'params': dataset_spec['generation_params']
            }
            
            # Get data from LLM
            csv_content = llm_response(DATASET_GENERATION_TEMPLATE.format(
                dataset_specs=json.dumps(generation_params, indent=2)
            ))
            
            # Save to file
            filename = f"{self.data_dir}/pandas/{problem_id}_{dataset_spec['name']}.csv"
            with open(filename, 'w') as f:
                f.write(csv_content)
            
            dataset_files[dataset_spec['name']] = filename
            
        # Generate expected output
        tasks_str = "\n".join(problem_spec['tasks'])
        expected_output = llm_response(f"""
        Given these analysis tasks:
        {tasks_str}
        
        Generate the expected output DataFrame that would result from correct analysis.
        Return only the CSV content with header row.
        """)
        
        output_file = f"{self.data_dir}/pandas/{problem_id}_expected.csv"
        with open(output_file, 'w') as f:
            f.write(expected_output)
            
        return {
            'problem_id': problem_id,
            'dataset_files': dataset_files,
            'expected_output': output_file
        }

    def _generate_python_data(self, problem_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Generate test cases for Python problems."""
        problem_id = str(uuid.uuid4())
        
        # Convert test cases to proper format
        formatted_tests = []
        for test in problem_spec['test_cases']:
            formatted_tests.append({
                'input': test['input'],
                'expected_output': test['output'],
                'description': test.get('description', '')
            })
            
        # Add edge cases
        for edge_case in problem_spec['edge_cases']:
            # Generate test case from edge case description
            test_case = llm_response(f"""
            Create a test case for this edge case: {edge_case}
            Return as JSON with input and expected_output fields.
            """)
            formatted_tests.append(json.loads(test_case))
            
        # Save test cases
        test_file = f"{self.data_dir}/python/{problem_id}_tests.json"
        with open(test_file, 'w') as f:
            json.dump(formatted_tests, f, indent=2)
            
        return {
            'problem_id': problem_id,
            'test_file': test_file
        }

    def cleanup_old_data(self, days_old: int = 7):
        """Remove generated data files older than specified days."""
        current_time = datetime.now()
        
        for root, _, files in os.walk(self.data_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_time = datetime.fromtimestamp(os.path.getctime(file_path))
                
                if (current_time - file_time).days > days_old:
                    os.remove(file_path)
