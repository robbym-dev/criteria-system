import dspy

class RatingPredictor(dspy.Signature):
    """Predict rating (Good, Bad, or Unsure) and provide explanation with criteria."""
    
    input_data = dspy.InputField()
    prompt_template = dspy.InputField()
    generated_content = dspy.InputField()
    rating = dspy.OutputField(desc="Predicted rating: Good, Bad, or Unsure")
    explanation = dspy.OutputField(desc="Detailed explanation with clear criteria for the rating")

class RatingPredictorModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predictor = dspy.Predict(RatingPredictor)
    
    def forward(self, input_data, prompt_template, generated_content):
        return self.predictor(
            input_data=input_data,
            prompt_template=prompt_template,
            generated_content=generated_content
        )