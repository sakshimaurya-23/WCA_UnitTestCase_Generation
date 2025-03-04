# WCA_UnitTestCase_Generation
# Overview

This repository contains a FastAPI project (main.py) and its corresponding unit test file (test_main.py). The unit test cases are generated using IBM Watsonx Code Assistant (WCA) with a structured prompt to ensure proper mocking, fixture management, and database session handling.

# Setup Instructions

- Prerequisites
- Ensure you have the following installed:
- Python 3.x
- FastAPI
- Ollama with Llama 3.1
- Watsonx Code Assistant (WCA)
- Required dependencies from requirements.txt

# Installation Steps

Set up a virtual environment (optional but recommended)

```sh
python -m venv venv```
```sh
source venv/bin/activate```



Install dependencies

```sh
pip install -r requirements.txt```

# Generating Unit Tests with WCA and Ollama

Steps to Use Watsonx Code Assistant

Install and Configure WCA

Ensure the necessary plugins and extensions are installed in your development environment.

Authenticate using IBM Cloud credentials if required.

Provide a Prompt

Input the following prompt into WCA:

'''Generate unit test cases test_main.py for above FastAPI endpoints.
Use mock and fixture wherever required.
Use all required import statements from above code.
Use required functions from above code.
Ensure tests are independent, database sessions are properly managed, and avoid fixture not found errors.'''

This will generate the test_main.py file.

Review and Modify the Generated Tests

Verify the correctness of test cases.

Ensure they follow best practices and align with project requirements.

Running Unit Tests

To execute the generated unit tests, run:

pytest test_main.py





