import pickle
import numpy as np
from typing import List, Dict, Any, Optional
import os

class EmbeddingsManager:
    def __init__(self):
        self.embeddings_file = 'data/embeddings.pkl'
        self.problems_embeddings = self._load_embeddings()

    def _load_embeddings(self) -> Dict[str, Any]:
        """Load embeddings from pickle file if it exists."""
        if os.path.exists(self.embeddings_file):
            with open(self.embeddings_file, 'rb') as f:
                return pickle.load(f)
        return {'problems': {}, 'vectors': {}}

    def _save_embeddings(self) -> None:
        """Save embeddings to pickle file."""
        with open(self.embeddings_file, 'wb') as f:
            pickle.dump(self.problems_embeddings, f)

    def add_problem(self, problem_data: Dict[str, Any]) -> None:
        """
        Generate embedding for a new problem and add it to the database.
        """
        # Create prompt for embedding
        prompt = f"""
        Generate an embedding descriptor for this problem:
        Title: {problem_data['title']}
        Description: {problem_data['description']}
        Type: {problem_data['type']}
        Difficulty: {problem_data['difficulty']}
        
        Return a comma-separated list of 10-15 key concepts and skills tested by this problem.
        """
        
        # Get embedding concepts from LLM
        concepts = llm_response(prompt).strip().split(',')
        concepts = [c.strip().lower() for c in concepts]
        
        # Create simple one-hot encoding for concepts
        all_concepts = set(concepts)
        for problem_id in self.problems_embeddings['problems']:
            all_concepts.update(self.problems_embeddings['vectors'][problem_id]['concepts'])
        
        vector = np.zeros(len(all_concepts))
        concept_to_idx = {concept: idx for idx, concept in enumerate(all_concepts)}
        
        for concept in concepts:
            vector[concept_to_idx[concept]] = 1
        
        # Store problem data and its vector
        self.problems_embeddings['problems'][problem_data['id']] = problem_data
        self.problems_embeddings['vectors'][problem_data['id']] = {
            'vector': vector,
            'concepts': concepts
        }
        
        self._save_embeddings()

    def find_similar_problems(
        self,
        problem_id: str,
        n: int = 3,
        difficulty_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Find n most similar problems to the given problem.
        Optionally filter by difficulty level.
        """
        if problem_id not in self.problems_embeddings['vectors']:
            return []
        
        query_vector = self.problems_embeddings['vectors'][problem_id]['vector']
        similarities = {}
        
        for pid, data in self.problems_embeddings['vectors'].items():
            if pid != problem_id:
                if difficulty_filter and self.problems_embeddings['problems'][pid]['difficulty'] != difficulty_filter:
                    continue
                
                # Calculate cosine similarity
                similarity = np.dot(query_vector, data['vector']) / (
                    np.linalg.norm(query_vector) * np.linalg.norm(data['vector'])
                )
                similarities[pid] = similarity
        
        # Get top n similar problems
        similar_problem_ids = sorted(similarities.keys(), key=lambda x: similarities[x], reverse=True)[:n]
        return [self.problems_embeddings['problems'][pid] for pid in similar_problem_ids]

    def get_problem_concepts(self, problem_id: str) -> List[str]:
        """Get the concepts tested by a specific problem."""
        if problem_id in self.problems_embeddings['vectors']:
            return self.problems_embeddings['vectors'][problem_id]['concepts']
        return []

    def get_concept_coverage(self, user_history: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Analyze concept coverage based on user's problem-solving history.
        Returns a dictionary of concepts and their mastery levels.
        """
        concept_attempts = {}
        concept_successes = {}

        for problem in user_history:
            problem_id = problem['problem_id']
            if problem_id in self.problems_embeddings['vectors']:
                concepts = self.problems_embeddings['vectors'][problem_id]['concepts']
                
                for concept in concepts:
                    concept_attempts[concept] = concept_attempts.get(concept, 0) + 1
                    if problem['passed']:
                        concept_successes[concept] = concept_successes.get(concept, 0) + 1

        # Calculate mastery level for each concept
        mastery_levels = {}
        for concept in concept_attempts:
            attempts = concept_attempts[concept]
            successes = concept_successes.get(concept, 0)
            
            # Calculate mastery level (0.0 to 1.0)
            if attempts >= 3:
                mastery_levels[concept] = successes / attempts
            else:
                # Not enough attempts to determine mastery
                mastery_levels[concept] = 0.0

        return mastery_levels

    def recommend_next_concepts(self, user_history: List[Dict[str, Any]], n: int = 3) -> List[str]:
        """
        Recommend next concepts for the user to practice based on their history.
        """
        if not user_history:
            return []

        # Get current concept mastery levels
        mastery_levels = self.get_concept_coverage(user_history)
        
        # Get all available concepts
        all_concepts = set()
        for data in self.problems_embeddings['vectors'].values():
            all_concepts.update(data['concepts'])

        # Score concepts based on learning value
        concept_scores = {}
        for concept in all_concepts:
            current_mastery = mastery_levels.get(concept, 0.0)
            
            # Prioritize concepts with low mastery but not completely new
            if current_mastery == 0.0:
                score = 0.5  # Some priority for new concepts
            else:
                # Higher score for concepts that need improvement
                score = 1.0 - current_mastery

            # Adjust score based on concept prerequisites (if defined)
            prerequisites_met = self._check_concept_prerequisites(concept, mastery_levels)
            if not prerequisites_met:
                score *= 0.5

            concept_scores[concept] = score

        # Return top N concepts
        return sorted(concept_scores.keys(), key=lambda x: concept_scores[x], reverse=True)[:n]

    def _check_concept_prerequisites(self, concept: str, mastery_levels: Dict[str, float]) -> bool:
        """
        Check if prerequisites for a concept are met.
        This is a simplified version - in a real system, you'd want a proper prerequisite graph.
        """
        # Example prerequisite rules (could be made more sophisticated)
        prerequisites = {
            'dynamic_programming': ['recursion', 'arrays'],
            'graph_traversal': ['arrays', 'recursion'],
            'advanced_sql': ['basic_sql', 'joins'],
            'window_functions': ['basic_sql', 'aggregations']
        }

        if concept in prerequisites:
            required_concepts = prerequisites[concept]
            for req_concept in required_concepts:
                if mastery_levels.get(req_concept, 0.0) < 0.6:  # Minimum mastery threshold
                    return False
        return True
