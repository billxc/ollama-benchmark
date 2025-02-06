import time
import yaml
import os
import ollama

def convert_to_markdown_table(data):
    """Convert the parsed YAML data into a Markdown table with readable headers and values."""
    header_mapping = {
        'prompt_eval_duration': 'Prompt Evaluation Duration',
        'prompt_eval_token_per_second': 'Prompt Tokens/Second',
        'prompt_token_count': 'Prompt Token Count',
        'response_eval_duration': 'Response Evaluation Duration',
        'response_eval_token_per_second': 'Response Tokens/Second',
        'response_token_count': 'Response Token Count',
        'word_count': 'Word Count'
    }
    
    models = list(data.keys())
    headers = ['Model'] + list(header_mapping.values())
    header_row = '| ' + ' | '.join(headers) + ' |'
    separator = '| ' + (' :---: | ' * len(headers))

    def format_value(value, metric_key):
        try:
            if 'eval_duration' in metric_key:
                total_seconds = float(value)
                minutes, seconds = divmod(total_seconds, 60)
                return f"{int(minutes)}:{int(seconds):02d}"
            elif 'token_per_second' in metric_key:
                return f"{float(value):.1f}"
            elif 'token_count' in metric_key or 'word_count' in metric_key:
                return f"{int(float(value)):,}"
            else:
                return str(value)
        except (ValueError, TypeError):
            return str(value)

    rows = []
    for model in models:
        metrics = data[model]
        row_values = [model] + [
            format_value(metrics[key], key) 
            for key in metrics.keys()
        ]
        row = '| ' + ' | '.join(row_values) + ' |'
        rows.append(row)
    
    table = '\n'.join([header_row, separator] + rows)
    return table
from ollama import chat

def load_config(config_path='config.yaml'):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def load_dataset(dataset_name='default'):
    with open(os.path.join("dataset",dataset_name+".yaml"), 'r') as file:
        data = yaml.safe_load(file)
    return data

class BenchmarkResult:
    def __init__(self, response: ollama.ChatResponse = None, prompt = None):
        if not isinstance(response, ollama.ChatResponse):
            self.prompt_token_count = 0
            self.prompt_eval_duration = 0
            self.response_token_count = 0
            self.response_eval_duration = 0
            self.prompt_eval_token_per_second = 0
            self.response_eval_token_per_second = 0
            self.word_count = 0
            return

        self.prompt_token_count = response.prompt_eval_count
        self.prompt_eval_duration = response.prompt_eval_duration / 1000000
        self.response_token_count = response.eval_count
        self.response_eval_duration = response.eval_duration / 1000000
        self.prompt_eval_token_per_second = self.prompt_token_count / (self.prompt_eval_duration / 1000)
        self.response_eval_token_per_second = self.response_token_count / (self.response_eval_duration / 1000)
        self.prompt = prompt
        self.response = response.message.content
        self.word_count = len(response.message.content)


    def to_dict(self):
        return {
            "prompt_token_count": self.prompt_token_count,
            "prompt_eval_duration": self.prompt_eval_duration,
            "response_token_count": self.response_token_count,
            "response_eval_duration": self.response_eval_duration,
            "prompt_eval_token_per_second": self.prompt_eval_token_per_second,
            "response_eval_token_per_second": self.response_eval_token_per_second,
            "word_count": self.word_count,
        }
    
    def combine(self, other):
        self.prompt_token_count += other.prompt_token_count
        self.prompt_eval_duration += other.prompt_eval_duration
        self.response_token_count += other.response_token_count
        self.response_eval_duration += other.response_eval_duration
        self.prompt_eval_token_per_second = self.prompt_token_count / (self.prompt_eval_duration / 1000)
        self.response_eval_token_per_second = self.response_token_count / (self.response_eval_duration / 1000)
        self.word_count += other.word_count
        return self

def run_benchmark(model_name, prompt):
    print(f"Running benchmark for model: {model_name} with prompt: {prompt}")
    # Simulate benchmark result
    
    response: ollama.ChatResponse = chat(model=model_name, messages=[
    {
        'role': 'user',
        'content': prompt,
    },])
    print(response.message.content)

    # return [
    #     {"prompt_token_count": response.prompt_eval_count},
    #     {"prompt_eval_duration": response.prompt_eval_duration / 1000000000},
    #     {"response_token_count": response.eval_count,},
    #     {"response_eval_duration": response.eval_duration / 1000000000,},
    #     {"prompt_eval_token_per_second": response.eval_count / (response.prompt_eval_duration / 1000000000),},
    #     {"response_eval_token_per_second": response.eval_count / (response.eval_duration / 1000000000),},
    # ]
    return BenchmarkResult(response)


def main():
    config = load_config()
    dataset = load_dataset("lite")
    models = config['models']
    compare_results = {}
    for model_name in models:
        output_dir = config['output_dir'] + "-" + model_name.replace("/", "-").replace(" ", "_").replace(":", "_")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        else:
        # clean output directory
            for file in os.listdir(output_dir):
                os.remove(os.path.join(output_dir, file))

        total = BenchmarkResult()
        for task, prompts in dataset['tasks'].items():
            task_results = BenchmarkResult()
            for prompt in prompts:
                result = run_benchmark(model_name, prompt)
                total.combine(result)
                task_results.combine(result)
                with open(os.path.join(output_dir, f"{task}_detail_results.yaml"), 'a') as file:
                    yaml.dump(result, file)
            output_path = os.path.join(output_dir, f"{task}_results.yaml")
            with open(output_path, 'w') as file:
                yaml.dump(task_results.to_dict(), file)
            print(f"Results for {task} saved to {output_path}")
        print("Total results:")
        print(total.to_dict())
        with open(os.path.join(output_dir, f"results.yaml"), 'w') as file:
                yaml.dump(result.to_dict(), file)
        compare_results[model_name] = total.to_dict()
        with open("compare_results.yaml", 'w') as file:
            yaml.dump(compare_results, file)

        # Convert compare_results to Markdown and save to a file
        markdown_table = convert_to_markdown_table(compare_results)
        with open("compare_results.md", 'w') as md_file:
            md_file.write(markdown_table)
        print("Markdown table saved to 'compare_results.md'")

if __name__ == "__main__":
    main()
