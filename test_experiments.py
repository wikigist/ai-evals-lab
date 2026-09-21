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

    assert saved_results[0]["comparison"] == result
    assert "timestamp" in saved_results[0]

    assert "comparison_id" in saved_results[0]
    assert saved_results[0]["comparison_id"].startswith("cmp_")


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



def test_compare_and_save_runs_handles_old_history_format(tmp_path):
    filename = tmp_path / "experiment_comparisons.json"

    old_comparison = {
        "baseline_pass_rate": 0.60,
        "candidate_pass_rate": 0.80,
        "pass_rate_difference": 0.20,
        "outcome": "improvement",
        "comparison_validity": "clean",
        "comparison_type": "model",
        "changed_fields": ["model"],
        "changed_count": 1,
        "baseline_model": "model_a",
        "candidate_model": "model_b",
        "baseline_prompt_version": "v1",
        "candidate_prompt_version": "v1",
        "baseline_dataset_name": "capital_eval",
        "candidate_dataset_name": "capital_eval"
        }
    
    file_utils.save_results([old_comparison], filename)
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

    experiments.compare_and_save_runs(baseline, candidate, filename)
    saved_results = file_utils.load_results(filename)

    assert len(saved_results) == 1
    assert saved_results[0] == old_comparison


def test_is_same_comparison_returns_true_for_same_experiment():
    existing = {
        "baseline_pass_rate": 0.60,
        "candidate_pass_rate": 0.80,
        "baseline_model": "model_a",
        "candidate_model": "model_b",
        "baseline_prompt_version": "v1",
        "candidate_prompt_version": "v1",
        "baseline_dataset_name": "capital_eval",
        "candidate_dataset_name": "capital_eval"
        }

    current = {
        "baseline_pass_rate": 0.60,
        "candidate_pass_rate": 0.80,
        "baseline_model": "model_a",
        "candidate_model": "model_b",
        "baseline_prompt_version": "v1",
        "candidate_prompt_version": "v1",
        "baseline_dataset_name": "capital_eval",
        "candidate_dataset_name": "capital_eval"
        }

    result = experiments.is_same_comparison(existing, current)
    assert result is True


def test_is_same_comparison_returns_false_for_different_model():
        existing = {
            "baseline_pass_rate": 0.60,
            "candidate_pass_rate": 0.80,
            "baseline_model": "model_a",
            "candidate_model": "model_b",
            "baseline_prompt_version": "v1",
            "candidate_prompt_version": "v1",
            "baseline_dataset_name": "capital_eval",
            "candidate_dataset_name": "capital_eval"
            }

        current = {
            "baseline_pass_rate": 0.60,
            "candidate_pass_rate": 0.80,
            "baseline_model": "model_a",
            "candidate_model": "model_c",
            "baseline_prompt_version": "v1",
            "candidate_prompt_version": "v1",
            "baseline_dataset_name": "capital_eval",
            "candidate_dataset_name": "capital_eval"
            }

        result = experiments.is_same_comparison(existing, current)
        assert result is False


def test_is_same_comparison_allows_tiny_float_difference():
    existing = {
        "baseline_pass_rate": 0.60,
        "candidate_pass_rate": 0.80,
        "baseline_model": "model_a",
        "candidate_model": "model_b",
        "baseline_prompt_version": "v1",
        "candidate_prompt_version": "v1",
        "baseline_dataset_name": "capital_eval",
        "candidate_dataset_name": "capital_eval"
    }

    current = {
        "baseline_pass_rate": 0.6000000000000001,
        "candidate_pass_rate": 0.80,
        "baseline_model": "model_a",
        "candidate_model": "model_b",
        "baseline_prompt_version": "v1",
        "candidate_prompt_version": "v1",
        "baseline_dataset_name": "capital_eval",
        "candidate_dataset_name": "capital_eval"
    }

    result = experiments.is_same_comparison(existing, current)

    assert result is True



def test_has_same_comparison_returns_true_when_match_exists():
    existing_comparison = {
        "baseline_pass_rate": 0.60,
        "candidate_pass_rate": 0.80,
        "baseline_model": "model_a",
        "candidate_model": "model_b",
        "baseline_prompt_version": "v1",
        "candidate_prompt_version": "v1",
        "baseline_dataset_name": "capital_eval",
        "candidate_dataset_name": "capital_eval"
    }

    current_comparison = {
        "baseline_pass_rate": 0.60,
        "candidate_pass_rate": 0.80,
        "baseline_model": "model_a",
        "candidate_model": "model_b",
        "baseline_prompt_version": "v1",
        "candidate_prompt_version": "v1",
        "baseline_dataset_name": "capital_eval",
        "candidate_dataset_name": "capital_eval"
    }

    result = experiments.has_same_comparison([existing_comparison], current_comparison)
    assert result is True


def test_has_same_comparison_returns_false_when_no_match_exists():

    existing_comparison = {
        "baseline_pass_rate": 0.60,
        "candidate_pass_rate": 0.80,
        "baseline_model": "model_a",
        "candidate_model": "model_b",
        "baseline_prompt_version": "v1",
        "candidate_prompt_version": "v1",
        "baseline_dataset_name": "capital_eval",
        "candidate_dataset_name": "capital_eval"
    }

    current_comparison = {
        "baseline_pass_rate": 0.60,
        "candidate_pass_rate": 0.80,
        "baseline_model": "model_a",
        "candidate_model": "model_c",
        "baseline_prompt_version": "v1",
        "candidate_prompt_version": "v1",
        "baseline_dataset_name": "capital_eval",
        "candidate_dataset_name": "capital_eval"
    }

    result = experiments.has_same_comparison([existing_comparison], current_comparison)
    assert result is False



def test_extract_existing_comparisons_handles_old_and_new_formats():
    old_comparison = {
        "baseline_pass_rate": 0.60,
        "candidate_pass_rate": 0.80,
        "baseline_model": "model_a",
        "candidate_model": "model_b",
        "baseline_prompt_version": "v1",
        "candidate_prompt_version": "v1",
        "baseline_dataset_name": "capital_eval",
        "candidate_dataset_name": "capital_eval"
    }

    new_record = {
    "comparison": {
        "baseline_pass_rate": 0.70,
        "candidate_pass_rate": 0.90,
        "baseline_model": "model_a",
        "candidate_model": "model_c",
        "baseline_prompt_version": "v1",
        "candidate_prompt_version": "v2",
        "baseline_dataset_name": "capital_eval",
        "candidate_dataset_name": "capital_eval"
    },
    "timestamp": "2026-09-18T17:00:00+00:00"
    }

    result = experiments.extract_existing_comparisons(
    [old_comparison, new_record]
    )

    assert result == [
    old_comparison,
    new_record["comparison"]
    ]


def test_generate_comparison_id_starts_with_cmp_prefix():
    cmp_id = experiments.generate_comparison_id()

    assert cmp_id.startswith("cmp_")


def test_generate_comparison_id_returns_unique_ids():

    cmp_id_one = experiments.generate_comparison_id()
    cmp_id_two = experiments.generate_comparison_id()

    assert cmp_id_one != cmp_id_two



def test_compare_runs_includes_run_ids():
    baseline = {
        "run_id": "run_baseline_123",
        "pass_rate": 0.60,
        "model": "model_a",
        "prompt_version": "v1",
        "dataset_name": "capital_eval"
    }

    candidate = {
        "run_id": "run_candidate_456",
        "pass_rate": 0.80,
        "model": "model_b",
        "prompt_version": "v1",
        "dataset_name": "capital_eval"
    }

    result = experiments.compare_runs(baseline, candidate)

    assert result["baseline_run_id"] == "run_baseline_123"
    assert result["candidate_run_id"] == "run_candidate_456"


def test_compare_and_save_runs_preserves_run_ids(tmp_path):
    baseline = {
        "run_id": "run_baseline_123",
        "pass_rate": 0.60,
        "model": "model_a",
        "prompt_version": "v1",
        "dataset_name": "capital_eval"
    }

    candidate = {
        "run_id": "run_candidate_456",
        "pass_rate": 0.80,
        "model": "model_b",
        "prompt_version": "v1",
        "dataset_name": "capital_eval"
    }

    filename = tmp_path / "experiment_comparisons.json"

    experiments.compare_and_save_runs(
        baseline,
        candidate,
        filename
    )

    saved_results = file_utils.load_results(filename)

    saved_comparison = saved_results[0]["comparison"]

    assert saved_comparison["baseline_run_id"] == "run_baseline_123"
    assert saved_comparison["candidate_run_id"] == "run_candidate_456"


def test_compare_runs_without_run_ids_still_works():
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

    assert result["outcome"] == "improvement"
    assert "baseline_run_id" not in result
    assert "candidate_run_id" not in result



def test_determine_quality_gate_passes_within_allowed_regression():
    result = experiments.determine_quality_gate(
        -0.02,
        0.04
    )

    assert result == "pass"


def test_determine_quality_gate_fails_beyond_allowed_regression():
    result = experiments.determine_quality_gate(
        -0.06,
        0.04
    )

    assert result == "fail"


def test_determine_quality_gate_passes_at_exact_threshold():
    result = experiments.determine_quality_gate(
        -0.04,
        0.04
    )

    assert result == "pass"


def test_determine_quality_gate_passes_for_improvement():
    result = experiments.determine_quality_gate(
        0.03,
        0.04
    )

    assert result == "pass"


def test_compare_runs_includes_quality_gate_when_threshold_provided():
    baseline = {
        "pass_rate": 0.80,
        "model": "model_a",
        "prompt_version": "v1",
        "dataset_name": "capital_eval"
    }

    candidate = {
        "pass_rate": 0.78,
        "model": "model_b",
        "prompt_version": "v1",
        "dataset_name": "capital_eval"
    }

    result = experiments.compare_runs(
        baseline,
        candidate,
        allowed_regression=0.04
    )

    assert result["quality_gate"] == "pass"