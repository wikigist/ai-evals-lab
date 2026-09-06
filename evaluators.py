import metrics
import evaluators
import pytest

def evaluate_answer(actual_answer, expected_answer):

    if actual_answer.lower() == expected_answer.lower():
        return "pass"

    return "fail"


def evaluate_contains(actual_answer, expected_answer):
    if expected_answer.lower() in actual_answer.lower():
        return "pass"

    return "fail"


def create_evaluation_record(
    actual_answer,
    expected_answer,
    evaluator,
    status
):
    evaluation_record = {
        "actual": actual_answer,
        "expected": expected_answer,
        "evaluator": evaluator,
        "status": status
    }

    return evaluation_record


def run_evaluation(actual_answer, expected_answer, evaluator):
    if evaluator == "contains":

        status = evaluate_contains(actual_answer, expected_answer)

    elif evaluator == "exact_match":

        status = evaluate_answer(actual_answer, expected_answer)

    else:
        raise ValueError("Unsupported evaluator")

    record = create_evaluation_record(
     actual_answer,
     expected_answer,
     evaluator,
     status
    )

    return record


def run_evaluation_batch(cases):
    results = []

    for case in cases:
        validate_evaluation_case(case)
        result = run_evaluation(
            case["actual"],
            case["expected"],
            case["evaluator"]
        )

        results.append(result)

    return results


def run_evaluation_suite(cases):
    results = run_evaluation_batch(cases)
    pass_rate = metrics.calculate_pass_rate(results)
    run_result = {
        "results": results,
        "pass_rate": pass_rate
    }

    return run_result


def validate_evaluation_case(case):
    required_keys = [
        "actual",
        "expected",
        "evaluator"
    ]

    for key in required_keys:
        if key not in case:
            raise ValueError(f"Missing required field: {key}")





