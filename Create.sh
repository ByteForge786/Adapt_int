#!/bin/bash

# Create utils package
mkdir -p utils
touch utils/__init__.py

# Create main utils files
touch utils/code_executor.py
touch utils/problem_generator.py
touch utils/difficulty_analyzer.py
touch utils/embeddings.py
touch utils/data_generator.py

# Create data directories with .gitkeep files
mkdir -p data/generated/python
mkdir -p data/generated/sql
mkdir -p data/generated/pandas
touch data/generated/python/.gitkeep
touch data/generated/sql/.gitkeep
touch data/generated/pandas/.gitkeep

# Create templates and sample data directories
mkdir -p data/templates/sample_data
mkdir -p templates/prompts

# Create sample data files
touch data/templates/sample_data/e_commerce.csv
touch data/templates/sample_data/customer_orders.csv
touch data/templates/sample_data/product_inventory.csv

# Create main application files
touch app.py
touch requirements.txt

# Create prompt templates
touch templates/prompts/problem_templates.py

# Create gitignore
echo "# Generated data
data/generated/*
!data/generated/python/.gitkeep
!data/generated/sql/.gitkeep
!data/generated/pandas/.gitkeep

# Python
__pycache__/
*.py[cod]
*$py.class
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Virtual environment
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo" > .gitignore

echo "Directory structure created successfully!"
