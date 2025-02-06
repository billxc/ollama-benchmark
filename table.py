import yaml
import os
import argparse

def read_yaml_file(file_path):
    """Read and parse the YAML file."""
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
    return data

def convert_to_markdown_table(data):
    """Convert the parsed YAML data into a Markdown table with readable headers and values."""
    # Mapping from YAML keys to readable column names
    header_mapping = {
        'prompt_eval_duration': 'Prompt Evaluation Duration',
        'prompt_eval_token_per_second': 'Prompt Tokens/Second',
        'prompt_token_count': 'Prompt Token Count',
        'response_eval_duration': 'Response Evaluation Duration',
        'response_eval_token_per_second': 'Response Tokens/Second',
        'response_token_count': 'Response Token Count',
        'word_count': 'Word Count'
    }
    
    # Extract headers (model names)
    models = list(data.keys())
    headers = ['Model'] + list(header_mapping.values())
    
    # Create header row
    header_row = '| ' + ' | '.join(headers) + ' |'
    
    # Create separator row
    separator = '| ' + (' :---: | ' * len(headers))
    
    def format_value(value, metric_key):
        """Format a value based on the metric key."""
        try:
            if 'eval_duration' in metric_key:
                # Format duration as minutes:seconds with one decimal place for tenths of a second
                total_seconds = float(value)
                minutes, seconds = divmod(total_seconds, 60)
                return f"{int(minutes)}:{int(seconds):02d}"
            elif 'token_per_second' in metric_key:
                # Format tokens per second to one decimal place
                return f"{float(value):.1f}"
            elif 'token_count' in metric_key or 'word_count' in metric_key:
                # Add commas to large numbers
                return f"{int(float(value)):,}"
            else:
                return str(value)
        except (ValueError, TypeError):
            # Return original value if formatting fails
            return str(value)

    # Create table rows for each model
    rows = []
    for model in models:
        metrics = data[model]
        row_values = [model] + [
            format_value(metrics[key], key) 
            for key in metrics.keys()
        ]
        row = '| ' + ' | '.join(row_values) + ' |'
        rows.append(row)
    
    # Combine all parts
    table = '\n'.join([header_row, separator] + rows)
    return table

def main():
    """Main function to parse arguments and generate the Markdown table."""
    parser = argparse.ArgumentParser(description='Convert YAML file to a Markdown table.')
    parser.add_argument('yaml_file', help='Path to the input YAML file')
    parser.add_argument('output_file', help='Name of the output file to save the Markdown table')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.yaml_file):
        print(f"Error: The file '{args.yaml_file}' does not exist.")
        return
    
    data = read_yaml_file(args.yaml_file)
    table = convert_to_markdown_table(data)
    
    with open(args.output_file, 'w') as f:
        f.write(table)
    
    print(f"Markdown table saved to '{args.output_file}'")

if __name__ == "__main__":
    main()