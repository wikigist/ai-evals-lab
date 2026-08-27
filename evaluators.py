def evaluate_answer(actual_answer, expected_answer):

    if actual_answer.lower() == expected_answer.lower():
        return "pass"

    return "fail"
