import streamlit as st
import pandas as pd
import pickle
from utils.code_executor import CodeExecutor
from utils.problem_generator import ProblemGenerator
from utils.difficulty_analyzer import DifficultyAnalyzer
from utils.embeddings import EmbeddingsManager
import time

class AdaptiveInterviewApp:
    def __init__(self):
        self.initialize_session_state()
        self.code_executor = CodeExecutor()
        self.problem_generator = ProblemGenerator()
        self.difficulty_analyzer = DifficultyAnalyzer()
        self.embeddings_manager = EmbeddingsManager()

    def initialize_session_state(self):
        if 'current_problem' not in st.session_state:
            st.session_state.current_problem = None
        if 'problems_history' not in st.session_state:
            st.session_state.problems_history = []
        if 'difficulty_level' not in st.session_state:
            st.session_state.difficulty_level = 'medium'
        if 'start_time' not in st.session_state:
            st.session_state.start_time = None

    def render_sidebar(self):
        with st.sidebar:
            st.title("Interview Preparation Settings")
            problem_type = st.selectbox(
                "Select Problem Type",
                ["Python", "SQL", "Pandas"]
            )
            
            st.subheader("Optional Job Details")
            company_name = st.text_input("Company Name")
            job_description = st.text_area("Job Description")
            
            if st.button("Generate New Problem"):
                self.generate_new_problem(problem_type, company_name, job_description)

    def generate_new_problem(self, problem_type, company_name=None, job_description=None):
        st.session_state.current_problem = self.problem_generator.generate_problem(
            problem_type,
            st.session_state.difficulty_level,
            company_name,
            job_description
        )
        st.session_state.start_time = time.time()

    def render_problem_section(self):
        if st.session_state.current_problem:
            st.header("Problem")
            st.markdown(st.session_state.current_problem['description'])
            
            if st.session_state.current_problem['type'] in ['Python', 'Pandas']:
                user_code = st.text_area(
                    "Your Solution",
                    height=300,
                    key="solution_code"
                )
            else:  # SQL
                user_code = st.text_area(
                    "Your SQL Query",
                    height=150,
                    key="solution_sql"
                )

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Run Code"):
                    self.run_solution(user_code)
            with col2:
                if st.button("Show Hints"):
                    st.markdown(st.session_state.current_problem['hints'])

    def run_solution(self, user_code):
        execution_time = time.time() - st.session_state.start_time
        result = self.code_executor.execute_code(
            user_code,
            st.session_state.current_problem
        )
        
        if result['success']:
            st.success("All test cases passed!")
            self.update_difficulty(True, execution_time)
        else:
            st.error(f"Test cases failed: {result['error']}")
            if st.button("Show Edge Cases"):
                st.code(st.session_state.current_problem['edge_cases'])

    def update_difficulty(self, passed, execution_time):
        problem_stats = {
            'difficulty': st.session_state.difficulty_level,
            'passed': passed,
            'execution_time': execution_time,
            'problem_id': st.session_state.current_problem['id']
        }
        st.session_state.problems_history.append(problem_stats)
        
        new_difficulty = self.difficulty_analyzer.calculate_next_difficulty(
            st.session_state.problems_history
        )
        st.session_state.difficulty_level = new_difficulty

    def run(self):
        st.title("Adaptive Interview Preparation Platform")
        
        self.render_sidebar()
        self.render_problem_section()
        
        # Display performance analytics
        if st.session_state.problems_history:
            st.subheader("Your Performance")
            df = pd.DataFrame(st.session_state.problems_history)
            st.line_chart(df['execution_time'])
            st.write(f"Current Difficulty Level: {st.session_state.difficulty_level}")

if __name__ == "__main__":
    app = AdaptiveInterviewApp()
    app.run()
