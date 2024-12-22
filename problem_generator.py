import json
import uuid
import pandas as pd
from typing import Optional, Dict, Any

class ProblemGenerator:
    def __init__(self):
        self.problem_types = {
            'Python': self._generate_python_problem,
            'SQL': self._generate_sql_problem,
            'Pandas': self._generate_pandas_problem
        }
        self.data_generator = DataGenerator()
        self.load_templates()

    def generate_problem(
        self,
        problem_type: str,
        difficulty: str,
        company_name: Optional[str] = None,
        job_description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate a new problem based on the given parameters."""
        if problem_type not in self.problem_types:
            raise ValueError(f"Invalid problem type: {problem_type}")
        
        return self.problem_types[problem_type](difficulty, company_name, job_description)

    def load_templates(self):
        """Load problem generation templates."""
        from templates.prompts.problem_templates import (
            PYTHON_PROBLEM_TEMPLATE,
            SQL_PROBLEM_TEMPLATE,
            PANDAS_PROBLEM_TEMPLATE,
            DATASET_GENERATION_TEMPLATE
        )
        self.templates = {
            'Python': PYTHON_PROBLEM_TEMPLATE,
            'SQL': SQL_PROBLEM_TEMPLATE,
            'Pandas': PANDAS_PROBLEM_TEMPLATE
        }
        self.dataset_template = DATASET_GENERATION_TEMPLATE

    def _get_previous_topics(self, user_history: List[Dict[str, Any]], problem_type: str) -> List[str]:
        """Extract previously covered topics from user history."""
        topics = set()
        for problem in user_history:
            if problem['type'] == problem_type and 'concepts_tested' in problem:
                topics.update(problem['concepts_tested'])
        return list(topics)

    def _generate_python_problem(
        self,
        difficulty: str,
        company_name: Optional[str],
        job_description: Optional[str],
        user_history: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Generate a unique Python coding problem."""
, and examples
        - Provide test cases including edge cases
        - Include hints that help with problem-solving approach
        
        Additional context:
        {context}
        
        Return the response in the following JSON format:
        {{
            "id": "unique_id",
            "type": "Python",
            "difficulty": "difficulty_level",
            "title": "problem_title",
            "description": "detailed_problem_description",
            "function_name": "expected_function_name",
            "constraints": ["list_of_constraints"],
            "examples": ["list_of_examples"],
            "test_cases": [
                {{"input": [test_inputs], "output": expected_output}}
            ],
            "hints": ["list_of_hints"],
            "edge_cases": ["list_of_edge_cases"]
        }}
        """
        
        response = llm_response(prompt)
        problem_data = json.loads(response)
        problem_data['id'] = str(uuid.uuid4())
        return problem_data

    def _generate_sql_problem(
        self,
        difficulty: str,
        company_name: Optional[str],
        job_description: Optional[str]
    ) -> Dict[str, Any]:
        """Generate a SQL problem."""
        context = self._build_context(difficulty, company_name, job_description)
        
        prompt = f"""
        Generate a SQL problem with the following specifications:
        - Difficulty: {difficulty}
        - Should include real-world business scenario
        - Include sample data structure and sample records
        - Must test important SQL concepts based on difficulty
        - Include expected output format
        
        Additional context:
        {context}
        
        Return the response in the following JSON format:
        {{
            "id": "unique_id",
            "type": "SQL",
            "difficulty": "difficulty_level",
            "title": "problem_title",
            "description": "detailed_problem_description",
            "sample_data": [
                {{"table_name": "table_name", "file": "path_to_csv", "schema": "table_schema"}}
            ],
            "expected_output": "path_to_expected_output_csv",
            "hints": ["list_of_hints"],
            "constraints": ["list_of_constraints"],
            "examples": ["list_of_examples"]
        }}
        """
        
        response = llm_response(prompt)
        problem_data = json.loads(response)
        
        # Generate sample data CSVs based on the schema
        self._generate_sample_data(problem_data)
        
        problem_data['id'] = str(uuid.uuid4())
        return problem_data

    def _generate_pandas_problem(
        self,
        difficulty: str,
        company_name: Optional[str],
        job_description: Optional[str]
    ) -> Dict[str, Any]:
        """Generate a Pandas data manipulation problem."""
        context = self._build_context(difficulty, company_name, job_description)
        
        prompt = f"""
        Generate a Pandas data manipulation problem with the following specifications:
        - Difficulty: {difficulty}
        - Should include real-world data analysis scenario
        - Include sample datasets and their structures
        - Must test important Pandas operations based on difficulty
        - Include expected output format
        
        Additional context:
        {context}
        
        Return the response in the following JSON format:
        {{
            "id": "unique_id",
            "type": "Pandas",
            "difficulty": "difficulty_level",
            "title": "problem_title",
            "description": "detailed_problem_description",
            "sample_data": [
                {{"variable_name": "df_name", "file": "path_to_csv", "description": "dataset_description"}}
            ],
            "expected_output": "path_to_expected_output_csv",
            "hints": ["list_of_hints"],
            "constraints": ["list_of_constraints"],
            "examples": ["list_of_examples"]
        }}
        """
        
        response = llm_response(prompt)
        problem_data = json.loads(response)
        
        # Generate sample datasets based on the problem
        self._generate_sample_data(problem_data)
        
        problem_data['id'] = str(uuid.uuid4())
        return problem_data

    def _build_context(
        self,
        difficulty: str,
        company_name: Optional[str],
        job_description: Optional[str]
    ) -> str:
        """Build context string for LLM prompt based on available information."""
        context_parts = [f"Difficulty level: {difficulty}"]
        
        if company_name:
            context_parts.append(f"Company: {company_name}")
            
            # Get company-specific problem style
            prompt = f"""
            Given the company {company_name}, what are the key technical areas and problem-solving styles
            typically asked in their interviews? Return response as a brief bullet point list.
            """
            company_context = llm_response(prompt)
            context_parts.append(f"Company interview style: {company_context}")
        
        if job_description:
            prompt = f"""
            Extract key technical skills and requirements from this job description:
            {job_description}
            Return as a comma-separated list of key technical areas to test.
            """
            skills = llm_response(prompt)
            context_parts.append(f"Required skills: {skills}")
        
        return "\n".join(context_parts)

    def _generate_sample_data(self, problem_data: Dict[str, Any]) -> None:
        """Generate sample datasets based on problem requirements."""
        if problem_data['type'] in ['SQL', 'Pandas']:
            for dataset in problem_data['sample_data']:
                prompt = f"""
                Generate sample data for the following dataset:
                Problem: {problem_data['description']}
                Dataset: {dataset['description'] if 'description' in dataset else ''}
                Schema: {dataset['schema'] if 'schema' in dataset else ''}
                
                Return the data as a CSV string with header row.
                Only return the CSV content, no additional text.
                """
                
                csv_data = llm_response(prompt)
                
                # Save to CSV file
                filename = f"data/sample_data/{problem_data['id']}_{dataset['table_name'] if 'table_name' in dataset else dataset['variable_name']}.csv"
                with open(filename, 'w') as f:
                    f.write(csv_data)
                dataset['file'] = filename
            
            # Generate expected output data
            prompt = f"""
            Generate expected output data for the following problem:
            Problem: {problem_data['description']}
            
            Return the data as a CSV string with header row.
            Only return the CSV content, no additional text.
            """
            
            expected_output = llm_response(prompt)
            
            # Save expected output
            filename = f"data/sample_data/{problem_data['id']}_expected_output.csv"
            with open(filename, 'w') as f:
                f.write(expected_output)
            problem_data['expected_output'] = filename
