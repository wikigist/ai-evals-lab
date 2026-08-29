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
