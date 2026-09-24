import quality_gate_runner
import pytest
import experiments

def test_enforce_gate_action_exits_zero_for_allow():
    with pytest.raises(SystemExit) as exc_info:
        quality_gate_runner.enforce_gate_action("allow")

    assert exc_info.value.code == 0


def test_enforce_gate_action_exits_one_for_block():
    with pytest.raises(SystemExit) as exc_info:
        quality_gate_runner.enforce_gate_action("block")

    assert exc_info.value.code == 1


def test_enforce_gate_action_rejects_unknown_action():
    with pytest.raises(ValueError):
        quality_gate_runner.enforce_gate_action("maybe")


def test_run_gate_blocks_failed_comparison():
    comparison = {
        "gate_action": "block"
    }

    with pytest.raises(SystemExit) as exc_info:
        quality_gate_runner.run_gate(comparison)

    assert exc_info.value.code == 1


def test_run_gate_allows_passed_comparison():
    comparison = {
        "gate_action": "allow"
    }

    with pytest.raises(SystemExit) as exc_info:
        quality_gate_runner.run_gate(comparison)

    assert exc_info.value.code == 0


def test_run_gate_blocks_real_failed_comparison():
    baseline = {
        "pass_rate": 0.80,
        "model": "model_a",
        "prompt_version": "v1",
        "dataset_name": "capital_eval"
        }

    candidate = {
        "pass_rate": 0.72,
        "model": "model_b",
        "prompt_version": "v1",
        "dataset_name": "capital_eval"
        }

    comparison = experiments.compare_runs(
        baseline,
        candidate,
        allowed_regression=0.04
        )

    with pytest.raises(SystemExit) as exc_info:
        quality_gate_runner.run_gate(comparison)

    assert exc_info.value.code == 1


def test_run_gate_allows_real_passing_comparison():
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

    comparison = experiments.compare_runs(
        baseline,
        candidate,
        allowed_regression=0.04
        )

    with pytest.raises(SystemExit) as exc_info:
        quality_gate_runner.run_gate(comparison)

    assert exc_info.value.code == 0


def test_run_gate_allows_real_improvement():
    baseline = {
        "pass_rate": 0.80,
        "model": "model_a",
        "prompt_version": "v1",
        "dataset_name": "capital_eval"
        }

    candidate = {
        "pass_rate": 0.82,
        "model": "model_b",
        "prompt_version": "v1",
        "dataset_name": "capital_eval"
        }

    comparison = experiments.compare_runs(
        baseline,
        candidate,
        allowed_regression=0.04
        )

    with pytest.raises(SystemExit) as exc_info:
        quality_gate_runner.run_gate(comparison)

    assert comparison["outcome"] == "improvement"
    assert comparison["quality_gate"] == "pass"
    assert comparison["gate_action"] == "allow"
    assert exc_info.value.code == 0
