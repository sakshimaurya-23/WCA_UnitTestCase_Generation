# WCA_UnitTestCase_Generation
## Overview

This repository contains a FastAPI project (main.py) and its corresponding unit test file (test_main.py). The unit test cases are generated using IBM Watsonx Code Assistant (WCA) with a structured prompt to ensure proper mocking, fixture management, and database session handling.

## Setup Instructions

- Prerequisites
- Ensure you have the following installed:
- Python 3.x
- FastAPI
- Ollama with Llama 3.1
- Watsonx Code Assistant (WCA)
- Required dependencies from requirements.txt

## Installation Steps

- Set up a virtual environment (optional but recommended)

```sh
python -m venv venv
source venv/bin/activate
```
- Install dependencies

```sh
pip install -r requirements.txt
```

## Generating Unit Tests with WCA and Ollama

### Steps to Use Watsonx Code Assistant

#### 1. Install and Configure WCA
- Ensure the necessary plugins and extensions are installed in your development environment.
- Authenticate using IBM Cloud credentials if required.
#### 2. Provide a Prompt
- Input the following prompt into WCA:

```sh
Generate unit test cases test_main.py for above fastapi endpoints.
Use mock and fixture wherever required.
Use all required import statements from above code.
use required functions from above code.
Ensure tests are independent, database sessions are properly managed, and avoid fixture not found errors.
```
- This will generate the test_main.py file.

#### 3. Review and Modify the Generated Tests
- Verify the correctness of test cases.
- Ensure they follow best practices and align with project requirements.

#### 4. Running Unit Tests
- To execute the generated unit tests, run:
```sh
pytest test_main.py
```





