# AI Evals Lab

A Python evaluation and reliability lab for testing AI system behaviour,
comparing evaluation runs, detecting regressions, and enforcing quality gates in CI.

## Current Features

- Dataset-driven evaluation runner for testing AI outputs against structured cases
- Reusable evaluators and metrics for measuring evaluation performance
- Baseline vs candidate experiment comparison
- Regression detection using configurable quality thresholds
- Quality-gate enforcement using process exit codes
- JSON persistence for evaluation and experiment results
- Automated test coverage with pytest
- GitHub Actions CI with separate software-test and eval-quality jobs
- Required pull-request checks before changes can merge into `main`
- OpenAI API integration for model interaction


## Architecture

```text
Evaluation cases
      ↓
Evaluation runner
      ↓
Evaluators and metrics
      ↓
Baseline vs candidate comparison
      ↓
Quality gate
      ↓
Allow / block decision
      ↓
Process exit code
      ↓
GitHub Actions
      ↓
Required pull-request checks
```

## Project Status

Core evaluation, testing, experiment comparison, quality-gate, and CI workflows are implemented.