from typing import List, Dict, Any
import numpy as np
from collections import deque

class DifficultyAnalyzer:
    def __init__(self):
        self.difficulty_levels = ['easy', 'medium', 'hard']
        self.window_size = 3  # Number of recent problems to consider
        self.performance_threshold = 0.7  # Success rate threshold for increasing difficulty
        self.time_weights = {
            'easy': {'fast': 60, 'slow': 180},  # seconds
            'medium': {'fast': 300, 'slow': 600},
            'hard': {'fast': 900, 'slow': 1800}
        }

    def calculate_next_difficulty(self, problems_history: List[Dict[str, Any]]) -> str:
        """
        Calculate the next problem's difficulty based on user's performance history.
        """
        if len(problems_history) < self.window_size:
            return 'medium'  # Default difficulty for new users
        
        # Get recent problems
        recent_problems = problems_history[-self.window_size:]
        
        # Calculate performance metrics
        success_rate = self._calculate_success_rate(recent_problems)
        time_performance = self._analyze_time_performance(recent_problems)
        current_difficulty = recent_problems[-1]['difficulty']
        
        # Determine next difficulty
        current_level_idx = self.difficulty_levels.index(current_difficulty)
        
        if success_rate >= self.performance_threshold and time_performance == 'fast':
            # User is performing well and solving quickly - increase difficulty
            if current_level_idx < len(self.difficulty_levels) - 1:
                return self.difficulty_levels[current_level_idx + 1]
        elif success_rate < 0.3 or (success_rate < 0.5 and time_performance == 'slow'):
            # User is struggling - decrease difficulty
            if current_level_idx > 0:
                return self.difficulty_levels[current_level_idx - 1]
        
        # Keep same difficulty if no clear indication to change
        return current_difficulty

    def _calculate_success_rate(self, problems: List[Dict[str, Any]]) -> float:
        """Calculate the success rate for recent problems."""
        successful = sum(1 for p in problems if p['passed'])
        return successful / len(problems)

    def _analyze_time_performance(self, problems: List[Dict[str, Any]]) -> str:
        """
        Analyze if the user's solving time is fast or slow relative to expected times.
        """
        time_scores = []
        
        for problem in problems:
            difficulty = problem['difficulty']
            time_taken = problem['execution_time']
            
            # Calculate normalized time score
            fast_threshold = self.time_weights[difficulty]['fast']
            slow_threshold = self.time_weights[difficulty]['slow']
            
            if time_taken <= fast_threshold:
                score = 1.0
            elif time_taken >= slow_threshold:
                score = 0.0
            else:
                # Linear interpolation between fast and slow thresholds
                score = 1.0 - (time_taken - fast_threshold) / (slow_threshold - fast_threshold)
            
            time_scores.append(score)
        
        # Average time score
        avg_score = np.mean(time_scores)
        return 'fast' if avg_score >= 0.6 else 'slow'

    def analyze_performance_patterns(self, problems_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze patterns in user's problem-solving performance to provide insights.
        """
        if not problems_history:
            return {}
        
        analysis = {
            'total_problems': len(problems_history),
            'success_rate': self._calculate_success_rate(problems_history),
            'average_time': np.mean([p['execution_time'] for p in problems_history]),
            'difficulty_distribution': {},
            'performance_trend': self._calculate_performance_trend(problems_history)
        }
        
        # Calculate difficulty distribution
        for difficulty in self.difficulty_levels:
            difficulty_problems = [p for p in problems_history if p['difficulty'] == difficulty]
            if difficulty_problems:
                analysis['difficulty_distribution'][difficulty] = {
                    'count': len(difficulty_problems),
                    'success_rate': self._calculate_success_rate(difficulty_problems)
                }
        
        return analysis

    def _calculate_performance_trend(self, problems_history: List[Dict[str, Any]]) -> str:
        """Calculate if user's performance is improving, declining, or stable."""
        if len(problems_history) < 5:
            return 'not_enough_data'
        
        # Use a sliding window to calculate success rates
        window_size = 3
        success_rates = []
        
        for i in range(len(problems_history) - window_size + 1):
            window = problems_history[i:i + window_size]
            success_rates.append(self._calculate_success_rate(window))
        
        # Calculate trend using linear regression slope
        x = np.arange(len(success_rates))
        slope = np.polyfit(x, success_rates, 1)[0]
        
        if slope > 0.1:
            return 'improving'
        elif slope < -0.1:
            return 'declining'
        else:
            return 'stable'
