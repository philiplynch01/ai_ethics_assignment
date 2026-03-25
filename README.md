# COMP41820 AI & Ethics: Police Facial Recognition System

This repository contains the executable code and formal logic implementations for the AI & Ethics module assignment. It uses the `z3` SMT solver to mathematically validate the functional and ethical goals of the Police Facial Recognition Technology (FRT) system detailed in the accompanying report.

The implementation models three distinct ethical frameworks:
1. **Deontology:** First-Order Logic (FOL) constraints to prevent demographic bias.
2. **Utilitarianism:** SMT constraints for dynamic, severity-based thresholding.
3. **Virtue Ethics:** Computation Tree Logic (CTL) state machine to enforce human-in-the-loop accountability.

## Environment Setup

This project uses **Python 3.13**. You can set up the environment using either `uv` (recommended) or standard `pip`. The primary dependencies are `z3-solver` and `ipykernel`.

### Option 1: Using `uv` (Recommended)
If you have [uv](https://github.com/astral-sh/uv) installed, the project includes a `pyproject.toml` file. Simply run:
```bash
uv sync
```

### Option 2: Using standard `pip`
If you prefer standard Python tools, a `requirements.txt` file is provided. Set up your virtual environment as usual:
```bash
pip install -r requirements.txt
```

## Project Structure

* `cases/`
  * `case_01.py` - FOL implementation of the Deontological equitability limit (5% FPIR).
  * `case_02.py` - SMT implementation of Utilitarian proportionality and dynamic thresholding.
  * `case_03.py` - CTL implementation of the Virtue Ethics UI lock.
* `ctl_checker.py` - Symbolic Model Checker utility class (provided via module practical labs).
* `run_cases.ipynb` - The primary Jupyter Notebook used to execute all three cases and generate the evidence outputs for the report.
* `pyproject.toml` / `requirements.txt` - Dependency management files.

## How to Run

To view the evidence and test the ethical constraints:
1. Complete the environment setup above.
2. Open `run_cases.ipynb` in your Jupyter environment.
3. Run all cells sequentially. The notebook imports the logic from the `cases/` directory and outputs the `z3` solver results (`sat`, `unsat`, or `Property Verified`).