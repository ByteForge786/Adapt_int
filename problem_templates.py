PYTHON_PROBLEM_TEMPLATE = """
Given the following context, generate a unique Python coding problem:
Context:
- Difficulty Level: {difficulty}
- Previously covered topics: {previous_topics}
- Company (if specified): {company}
- Required skills from JD: {required_skills}

Guidelines for problem generation:
1. Create a completely new and unique problem not commonly found on coding platforms
2. Problem should incorporate real-world scenarios when possible
3. Include domain-specific challenges if company is provided
4. Ensure problem tests understanding of core concepts
5. Generate appropriate edge cases based on difficulty level

Return the problem in this JSON format:
{
    "id": "unique_id",
    "type": "Python",
    "difficulty": "difficulty_level",
    "title": "problem_title",
    "description": "detailed_problem_description",
    "function_name": "expected_function_name",
    "constraints": ["list_of_constraints"],
    "examples": ["list_of_examples"],
    "test_cases": [
        {"input": [test_inputs], "output": expected_output}
    ],
    "hints": ["list_of_hints"],
    "edge_cases": ["list_of_edge_cases"],
    "concepts_tested": ["list_of_concepts"]
}
"""

SQL_PROBLEM_TEMPLATE = """
Create a unique SQL problem based on the following context:
Context:
- Difficulty Level: {difficulty}
- Previous SQL concepts covered: {previous_topics}
- Company (if specified): {company}
- Required skills from JD: {required_skills}

Guidelines for problem generation:
1. Create a realistic business scenario
2. Generate schema and sample data that makes sense for the scenario
3. Include complex relationships and data patterns based on difficulty
4. Focus on company-specific data scenarios if company is provided
5. Test multiple SQL concepts in a single problem

Generate all data in this JSON format:
{
    "id": "unique_id",
    "type": "SQL",
    "difficulty": "difficulty_level",
    "title": "problem_title",
    "description": "problem_description",
    "business_context": "business_scenario",
    "schema": [
        {
            "table_name": "name",
            "columns": [
                {"name": "column_name", "type": "data_type", "description": "description"}
            ],
            "sample_data_parameters": {
                "num_rows": rows_to_generate,
                "value_ranges": {"column": "range_spec"},
                "patterns": {"column": "pattern_spec"}
            }
        }
    ],
    "task": "specific_task_description",
    "hints": ["list_of_hints"],
    "concepts_tested": ["list_of_concepts"]
}
"""

PANDAS_PROBLEM_TEMPLATE = """
Create a unique Pandas data analysis problem with the following context:
Context:
- Difficulty Level: {difficulty}
- Previous Pandas concepts covered: {previous_topics}
- Company (if specified): {company}
- Required skills from JD: {required_skills}

Guidelines for problem generation:
1. Create realistic data analysis scenarios
2. Generate sample datasets that reflect real-world data challenges
3. Include data cleaning and preprocessing tasks
4. Focus on industry-specific analysis if company provided
5. Test multiple Pandas operations in meaningful ways

Return the problem in this JSON format:
{
    "id": "unique_id",
    "type": "Pandas",
    "difficulty": "difficulty_level",
    "title": "problem_title",
    "description": "problem_description",
    "business_context": "analysis_scenario",
    "datasets": [
        {
            "name": "dataset_name",
            "description": "dataset_description",
            "columns": [
                {"name": "column_name", "type": "data_type", "description": "description"}
            ],
            "generation_params": {
                "num_rows": rows_to_generate,
                "distributions": {"column": "distribution_spec"},
                "missing_data": {"column": "missing_pattern"},
                "special_cases": ["list_of_special_cases"]
            }
        }
    ],
    "tasks": ["list_of_analysis_tasks"],
    "hints": ["list_of_hints"],
    "validation_criteria": ["list_of_criteria"],
    "concepts_tested": ["list_of_concepts"]
}
"""

DATASET_GENERATION_TEMPLATE = """
Generate a realistic dataset based on these specifications:
{dataset_specs}

Guidelines:
1. Data should be realistic and internally consistent
2. Include edge cases and special patterns
3. Maintain referential integrity across related tables
4. Include some interesting anomalies or patterns to discover
5. Generate appropriate missing data if specified

Return only the CSV content with header row.
Do not include any explanations or additional text.
"""
