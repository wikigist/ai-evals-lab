import experiments
import pytest

def test_compare_runs_improvement():
    baseline = {
        "pass_rate": 0.60,
        "model": "model_a",
        "prompt_version": "v1",
        "dataset_name": "capital_eval"
    }

    candidate = {
        "pass_rate": 0.80,
        "model": "model_b",
        "prompt_version": "v1",
        "dataset_name": "capital_eval"
    }

    result = experiments.compare_runs(baseline, candidate)

    assert result["baseline_pass_rate"] == 0.60
    assert result["candidate_pass_rate"] == 0.80
    assert result["pass_rate_difference"] == pytest.approx(0.20)
    assert result["outcome"] == "improvement"
    assert result["comparison_validity"] == "clean"



def test_compare_runs_regression():
    baseline = {
        "pass_rate": 0.90,
        "model": "model_a",
        "prompt_version": "v1",
        "dataset_name": "capital_eval"
        }

    candidate = {
        "pass_rate": 0.85,
        "model": "model_b",
        "prompt_version": "v1",
        "dataset_name": "capital_eval"
        }

    result = experiments.compare_runs(baseline, candidate)

    assert result["baseline_pass_rate"] == 0.90
    assert result["candidate_pass_rate"] == 0.85
    assert result["pass_rate_difference"] == pytest.approx(-0.05)
    assert result["outcome"] == "regression"
    assert result["comparison_validity"] == "clean"



def test_compare_runs_tie():

    baseline = {
        "pass_rate": 0.75,
        "model": "model_a",
        "prompt_version": "v1",
        "dataset_name": "capital_eval"
        }

    candidate = {
        "pass_rate": 0.75,
        "model": "model_a",
        "prompt_version": "v1",
        "dataset_name": "capital_eval"
        }

    result = experiments.compare_runs(baseline, candidate)

    assert result["baseline_pass_rate"] == 0.75
    assert result["candidate_pass_rate"] == 0.75
    assert result["pass_rate_difference"] == pytest.approx(0.0)
    assert result["outcome"] == "tie"
    assert result["comparison_validity"] == "same_setup"


