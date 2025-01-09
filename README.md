# Ollama-Benchmark

Ollama-Benchmark is a tool for evaluating and comparing the performance of different machine learning models. It offers a suite of standardized benchmarks to help users quickly understand the strengths and weaknesses of various models.

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Contributing](#contributing)
5. [License](#license)

## Introduction

Ollama-Benchmark provides a comprehensive benchmarking framework designed to help researchers and engineers assess the performance of machine learning models across a variety of tasks. With standardized testing procedures and detailed report generation, users can easily compare the performance of different models.

## Installation

To use Ollama-Benchmark, follow these installation steps:

1. **Clone the Repository**

   First, clone the Ollama-Benchmark GitHub repository to your local machine:

   ```bash
   git clone https://github.com/billxc/ollama-benchmark.git
   cd ollama-benchmark
   ```

2. **Install Dependencies**

   Use `pip` to install the required Python libraries:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Ollama-Benchmark provides an easy-to-use command-line interface. Here are the basic steps to use it:

1. **Configure the Benchmark**

   Before running the benchmark, you need to configure the test parameters. Edit the `config.yaml` file to set the model paths, dataset paths, and other parameters according to your requirements.

2. **Run the Benchmark**

   Use the following command to run the benchmark:

   ```bash
   python benchmark.py
   ```

   This command will automatically load the configuration file, execute the benchmark tests, and generate a report.

3. **View the Results**

   After the tests are completed, the results will be saved in the `results/` directory. You can review the generated report files to understand the detailed performance metrics of each model.

## Contributing

We welcome contributions from the community! If you have any suggestions, issues, or improvements, please feel free to submit an issue or a pull request. For guidelines on contributing, please refer to the `CONTRIBUTING.md` file.

## License

Ollama-Benchmark is licensed under the MIT License. For more details, please refer to the `LICENSE` file.

---

Thank you for using Ollama-Benchmark! We look forward to your feedback and contributions.
