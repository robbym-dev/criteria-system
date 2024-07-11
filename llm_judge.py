import dspy
import pandas as pd
from predictor import RatingPredictorModule
from optimizer import RatingOptimizer

class LLMJudge:
    def __init__(self):
        self.predictor = None
        self.compiled_predictor = None
        self.optimizer = None

    def _load_examples(self, file_path):
        df = pd.read_csv(file_path, sep='\t')
        return df.to_dict('records')

    def train(self, training_file):
        examples = self._load_examples(training_file)
        self.predictor = RatingPredictorModule()
        self.optimizer = RatingOptimizer()
        self.compiled_predictor = self.optimizer.optimize(self.predictor, examples)
        print("Criteria system trained successfully.")

    def evaluate(self, evaluation_file):
        examples = self._load_examples(evaluation_file)
        
        if not self.compiled_predictor:
            raise ValueError("Criteria system not trained. Please run train() first.")
        
        results = []
        correct_predictions = 0
        total_predictions = 0
        
        for example in examples:
            prediction = self.compiled_predictor(
                input_data=example['input_data'],
                prompt_template=example['prompt_template'],
                generated_content=example['generated_content']
            )
            rating = self._post_process_rating(prediction.rating, prediction.explanation)
            criteria = self._extract_criteria(prediction.explanation)
            
            result = {
                "input_data": example['input_data'],
                "prompt_template": example['prompt_template'],
                "generated_content": example['generated_content'],
                "predicted_rating": rating,
                "explanation": prediction.explanation,
                "criteria": criteria,
                "original_rating": prediction.rating  # Add this line
            }
            
            if 'rating' in example:  # Check if ground truth is available
                result["ground_truth"] = example['rating']
                total_predictions += 1
                if rating.lower() == example['rating'].lower():
                    correct_predictions += 1
            
            results.append(result)
        
        accuracy = correct_predictions / total_predictions if total_predictions > 0 else None
        
        return results, accuracy

    def _post_process_rating(self, rating, explanation):
        rating = rating.split(": ")[-1].lower()  # Remove "Predicted rating: " prefix and lowercase
        explanation_lower = explanation.lower()
        
        risk_keywords = ["risk", "danger", "harm", "incorrect", "misleading", "incomplete", "inaccurate"]
        safe_keywords = ["safe", "accurate", "helpful", "comprehensive", "correct", "beneficial"]
        
        risk_count = sum(1 for keyword in risk_keywords if keyword in explanation_lower)
        safe_count = sum(1 for keyword in safe_keywords if keyword in explanation_lower)
        
        if risk_count > safe_count or any(word in explanation_lower for word in ["high risk", "very dangerous", "extremely harmful"]):
            return "Bad"
        elif "balanced" in explanation_lower or "both positive and negative" in explanation_lower or rating == "unsure":
            return "Unsure"
        else:
            return rating.capitalize()
    
    def _extract_criteria(self, explanation):
        sentences = explanation.split('. ')
        criteria = []
        for sent in sentences:
            if any(keyword in sent.lower() for keyword in ["because", "due to", "as", "since", "reason", "criteria", "factor", "aspect", "consideration"]):
                criteria.append(sent.strip())
        return criteria[:3]  # Return up to 3 criteria
    
llm_judge = LLMJudge()