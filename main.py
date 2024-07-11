from llm_judge import llm_judge
import json
import dspy
from dotenv import load_dotenv
import os

def main():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")

    lm = dspy.OpenAI(api_key=api_key, model="gpt-4o")
    dspy.settings.configure(lm=lm)

    training_file = "<training_file_path_here>"
    llm_judge.train(training_file)

    evaluation_file = "<evaluation_file_path_here>"
    results, accuracy = llm_judge.evaluate(evaluation_file)
    
    for result in results:
        print(f"Input: {result['input_data']}")
        print(f"Predicted Rating: {result['predicted_rating']}")
        print(f"Original Rating: {result['original_rating']}")
        if 'ground_truth' in result:
            print(f"Ground Truth: {result['ground_truth']}")
            print(f"Correct: {'Yes' if result['predicted_rating'].lower() == result['ground_truth'].lower() else 'No'}")
        # print(f"Explanation: {result['explanation']}")
        # print(f"Extracted Criteria: {', '.join(result['criteria'])}")
        print("---")

    if accuracy is not None:
        print(f"\nOverall Accuracy: {accuracy:.2%}")
    else:
        print("\nNo ground truth available for accuracy calculation.")

    with open('llm_judge_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"Results saved to llm_judge_results.json")

if __name__ == "__main__":
    main()