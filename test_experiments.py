import experiments
import pytest
import file_utils

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
    assert result["comparison_type"] == "model"
    assert result["changed_fields"] == ["model"]
    assert result["changed_count"] == 1
    assert result["baseline_model"] == "model_a"
    assert result["candidate_model"] == "model_b"



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
    assert result["comparison_type"] == "model"
    assert result["changed_fields"] == ["model"]
    assert result["changed_count"] == 1



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
    assert result["comparison_type"] == "same_setup"
    assert result["changed_fields"] == []
    assert result["changed_count"] == 0




def test_compare_runs_prompt_comparison():

    baseline = {
        "pass_rate": 0.70,
        "model": "model_a",
        "prompt_version": "v1",
        "dataset_name": "capital_eval"
        }

    candidate = {
        "pass_rate": 0.85,
        "model": "model_a",
        "prompt_version": "v2",
        "dataset_name": "capital_eval"
        }


    result = experiments.compare_runs(baseline, candidate)

    assert result["baseline_pass_rate"] == 0.70
    assert result["candidate_pass_rate"] == 0.85
    assert result["pass_rate_difference"] == pytest.approx(0.15)
    assert result["outcome"] == "improvement"
    assert result["comparison_type"] == "prompt"
    assert result["comparison_validity"] == "clean"
    assert result["changed_fields"] == ["prompt_version"]
    assert result["changed_count"] == 1
    assert result["baseline_prompt_version"] == "v1"
    assert result["candidate_prompt_version"] == "v2"
    
    


def test_compare_runs_dataset_comparison():

    baseline = {
        "pass_rate": 0.95,
        "model": "model_a",
        "prompt_version": "v1",
        "dataset_name": "capital_eval"
        }

    candidate = {
        "pass_rate": 0.85,
        "model": "model_a",
        "prompt_version": "v1",
        "dataset_name": "special_eval"
        }


    result = experiments.compare_runs(baseline, candidate)

    assert result["baseline_pass_rate"] == 0.95
    assert result["candidate_pass_rate"] == 0.85
    assert result["pass_rate_difference"] == pytest.approx(-0.1)
    assert result["outcome"] == "regression"
    assert result["comparison_type"] == "dataset"
    assert result["comparison_validity"] == "clean"
    assert result["changed_fields"] == ["dataset_name"]
    assert result["changed_count"] == 1
    assert result["baseline_dataset_name"] == "capital_eval"
    assert result["candidate_dataset_name"] == "special_eval"


def test_compare_runs_confounded():

    baseline = {
        "pass_rate": 0.65,
        "model": "model_a",
        "prompt_version": "v1",
        "dataset_name": "capital_eval"
        }

    candidate = {
        "pass_rate": 0.99,
        "model": "model_b",
        "prompt_version": "v2",
        "dataset_name": "capital_eval"
        }


    result = experiments.compare_runs(baseline, candidate)

    assert result["baseline_pass_rate"] == 0.65
    assert result["candidate_pass_rate"] == 0.99
    assert result["pass_rate_difference"] == pytest.approx(0.34)
    assert result["outcome"] == "improvement"
    assert result["comparison_type"] == "confounded"
    assert result["comparison_validity"] == "confounded"
    assert result["changed_fields"] == ["model", "prompt_version"]
    assert result["changed_count"] == 2



def test_compare_runs_all_fields_changed():

    baseline = {
        "pass_rate": 0.75,
        "model": "model_a",
        "prompt_version": "v1",
        "dataset_name": "capital_eval"
        }

    candidate = {
        "pass_rate": 0.80,
        "model": "model_b",
        "prompt_version": "v2",
        "dataset_name": "special_eval"
        }

    
    result = experiments.compare_runs(baseline, candidate)
    
    assert result["baseline_pass_rate"] == 0.75
    assert result["candidate_pass_rate"] == 0.80
    assert result["pass_rate_difference"] == pytest.approx(0.05)
    assert result["outcome"] == "improvement"
    assert result["comparison_type"] == "confounded"
    assert result["comparison_validity"] == "confounded"
    assert result["changed_fields"] == ["model", "prompt_version", "dataset_name"]
    assert result["changed_count"] == 3


def test_determine_outcome_improvement():
    result = experiments.determine_outcome(0.20)

    assert result == "improvement"


def test_determine_outcome_regression():
    result = experiments.determine_outcome(-0.05)

    assert result == "regression"


def test_determine_outcome_tie():
    result = experiments.determine_outcome(0)

    assert result == "tie"



def test_compare_and_save_runs(tmp_path):
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

    filename = tmp_path / "experiment_comparisons.json"

    result = experiments.compare_and_save_runs(
        baseline,
        candidate,
        filename
    )

    assert result["outcome"] == "improvement"
    assert result["comparison_type"] == "model"

    assert filename.exists()

    saved_results = file_utils.load_results(filename)

    assert saved_results == [result]


def test_compare_and_save_runs_builds_history(tmp_path):
    filename = tmp_path / "experiment_comparisons.json"

    baseline = {
        "pass_rate": 0.60,
        "model": "model_a",
        "prompt_version": "v1",
        "dataset_name": "capital_eval"
        }

    candidate_one = {
        "pass_rate": 0.80,
        "model": "model_b",
        "prompt_version": "v1",
        "dataset_name": "capital_eval"
        }

    candidate_two = {
        "pass_rate": 0.70,
        "model": "model_a",
        "prompt_version": "v2",
        "dataset_name": "capital_eval"
        }

    experiments.compare_and_save_runs(
        baseline,
        candidate_one,
        filename
        )

    experiments.compare_and_save_runs(
        baseline,
        candidate_two,
        filename
        )

    saved_results = file_utils.load_results(filename)
    assert len(saved_results) == 2


def test_compare_and_save_runs_avoids_duplicates(tmp_path):
    filename = tmp_path / "experiment_comparisons.json"

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

    experiments.compare_and_save_runs(
        baseline,
        candidate,
        filename
        )

    experiments.compare_and_save_runs(
        baseline,
        candidate,
        filename
        )

    saved_results = file_utils.load_results(filename)
    assert len(saved_results) == 1