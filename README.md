# Criteria System

The Criteria System is a versatile and domain-agnostic content evaluation tool designed to assess the quality of generated content across various fields. Leveraging the power of large language models, this system can analyze input data, prompt templates, and generated content to provide ratings (Good, Bad, or Unsure) along with detailed explanations and criteria.

## Key Features
- **Domain-independent evaluation**
- **Flexible rating system**
- **Detailed explanations and criteria extraction**
- **Easy integration with OpenAI's GPT models**
- **Customizable for different content types and evaluation needs**

## How to Use

### Prerequisites
- Python 3.11+
- OpenAI API key

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/robbym-dev/criteria-system.git
    cd criteria-system
    ```

2. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up your OpenAI API key:**
    ```bash
    export OPENAI_API_KEY='your-api-key-here'
    ```

### Usage

1. **Update file paths in `main.py`:**
    - Open the `main.py` file and locate lines 17 and 20.
    - Update the file paths to point to the dataset you want to use. The repository includes datasets for customer service, finance, and hotels. Use relative paths to these files:

    ```python
    # Line 17: Set the path for the training file
    training_file = "datasets/customer_service_train.tsv"

    # Line 20: Set the path for the evaluation file
    evaluation_file = "datasets/customer_service_eval.tsv"
    ```

    You can choose from:
    - `datasets/customer_service_train.tsv` and `datasets/customer_service_eval.tsv`
    - `datasets/finance_train.tsv` and `datasets/finance_eval.tsv`
    - `datasets/hotels_train.tsv` and `datasets/hotels_eval.tsv`

2. **Run the system in terminal:**
    ```bash
    python main.py
    ```

    The system will train on the specified training dataset and then evaluate the content in the evaluation dataset. It will output the results, including predicted ratings, explanations, and extracted criteria for each item in the evaluation set.

### Customization

You can customize the system by modifying the prompt in the `generate_prompt` method of the `RatingOptimizer` class in `optimizer.py`. This allows you to tailor the evaluation criteria to your specific needs.

### Future Work
Future work will involve engineering a UI interface and tightening evaluation accuracy.

---

By following these steps, you'll be able to set up and run the Criteria System to evaluate content quality in your chosen domain. For any further customization or advanced usage, refer to the comments and documentation within the codebase.
