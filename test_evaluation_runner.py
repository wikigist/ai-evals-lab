import evaluation_runner
import file_utils
import pytest
import json
import evaluators

def test_run_evaluation_file_with_project_dataset():
    actual = evaluation_runner.run_evaluation_file("evaluation_cases.json")
    expected = {
    "results": [
        {
            "actual": "Paris",
            "expected": "Paris",
            "evaluator": "exact_match",
            "status": "pass"
        },
        {
            "actual": "The capital of France is London.",
            "expected": "Paris",
            "evaluator": "contains",
            "status": "fail"
        }
    ],
    "pass_rate": 0.5
    }

    assert actual == expected


def test_run_evaluation_file_with_tmp_path(tmp_path):
    test_file = tmp_path / "evaluation_cases.json"
    test_cases = [
    {
        "actual": "Paris",
        "expected": "Paris",
        "evaluator": "exact_match"
    },
    {
        "actual": "The capital of France is London.",
        "expected": "Paris",
        "evaluator": "contains"
    }
    ]
    file_utils.save_results(test_cases, test_file)

    actual = evaluation_runner.run_evaluation_file(test_file)
    expected = {
    "results": [
        {
            "actual": "Paris",
            "expected": "Paris",
            "evaluator": "exact_match",
            "status": "pass"
        },
        {
            "actual": "The capital of France is London.",
            "expected": "Paris",
            "evaluator": "contains",
            "status": "fail"
        }
    ],
    "pass_rate": 0.5
    }

    assert actual == expected




def test_run_evaluation_file_with_empty_list(tmp_path):
    test_file = tmp_path /  "evaluation_cases.json"
    test_cases = []

    file_utils.save_results(test_cases, test_file)

    actual = evaluation_runner.run_evaluation_file(test_file)
    expected = {
        "results": [],
        "pass_rate": 0
    }

    assert actual == expected 



def test_run_evaluation_file_missing_file(tmp_path):
    test_file = tmp_path / "missing.json"

    with pytest.raises(FileNotFoundError):
        evaluation_runner.run_evaluation_file(test_file)




def test_run_evaluation_file_broken_file(tmp_path):
    test_file = tmp_path / "broken.json"
    test_file.write_text('{"actual": "Paris"')
    with pytest.raises(json.JSONDecodeError):
        evaluation_runner.run_evaluation_file(test_file)



def test_run_evaluation_file_missing_expected(tmp_path):
    test_file = tmp_path / "missing_case.json"
    test_cases = [
    {
        "actual": "Paris",
        "evaluator": "exact_match"
    }
    ]

    file_utils.save_results(test_cases, test_file)
    with pytest.raises(ValueError, match="Missing required field: expected"):
        evaluation_runner.run_evaluation_file(test_file)


def test_run_evaluation_file_missing_evaluator(tmp_path):
    test_file = tmp_path / "missing_case.json"
    test_cases = [
    {
        "actual": "Paris",
        "expected": "Paris"
    }
    ]

    file_utils.save_results(test_cases, test_file)
    with pytest.raises(ValueError, match="Missing required field: evaluator"):
        evaluation_runner.run_evaluation_file(test_file)



def test_run_evaluation_file_bad_dataset(tmp_path):
    test_file = tmp_path / "invalid_dataset.json"
    bad_dataset = {
        "actual": "Paris",
        "expected": "Paris",
        "evaluator": "exact_match"
        }

    file_utils.save_results(bad_dataset, test_file)
    with pytest.raises(TypeError, match="Evaluation dataset must be a list"):
        evaluation_runner.run_evaluation_file(test_file)



def test_run_evaluation_file_unsupported_dataset(tmp_path):
    test_file = tmp_path / "invalid_dataset.json"
    bad_dataset = [
        {
            "actual": "Paris",
            "expected": "Paris",
            "evaluator": "exact_match"
            },
            "banana"
            ]
    file_utils.save_results(bad_dataset, test_file)
    with pytest.raises(TypeError, match="Evaluation case must be a dictionary"):
        evaluation_runner.run_evaluation_file(test_file)


def test_run_evaluation_file_unsupported_evaluator(tmp_path):
    test_file = tmp_path / "unsupported_evaluator.json"
    bad_dataset = [
        {
            "actual": "Paris",
            "expected": "Paris",
            "evaluator": "banana"
            }
            ]

    file_utils.save_results(bad_dataset, test_file)
    with pytest.raises(ValueError, match="Unsupported evaluator"):
        evaluation_runner.run_evaluation_file(test_file)


def test_run_evaluation_file_wrong_field_type(tmp_path):
    test_file = tmp_path / "wrong_field_type.json"
    bad_dataset =[
        {
            "actual": 123,
            "expected": "Paris",
            "evaluator": "contains"
            }
            ]

    file_utils.save_results(bad_dataset, test_file)
    with pytest.raises(TypeError, match="Actual must be a string"):
        evaluation_runner.run_evaluation_file(test_file)

    

def test_run_evaluation_file_wrong_field_type_evaluator(tmp_path):
    test_file = tmp_path / "wrong_field_type.json"
    bad_dataset =[
        {
            "actual": "Paris",
            "expected": "Paris",
            "evaluator": 123
            }
            ]

    file_utils.save_results(bad_dataset, test_file)
    with pytest.raises(TypeError, match="Evaluator must be a string"):
        evaluation_runner.run_evaluation_file(test_file)

