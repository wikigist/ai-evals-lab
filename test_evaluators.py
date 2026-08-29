import evaluators 

def test_evaluate_answer():

    actual = evaluators.evaluate_answer("Paris", "Paris")
    expected = "pass"

    assert actual == expected



def test_evaluate_answer_fails_when_answers_do_not_match():

    actual = evaluators.evaluate_answer("London", "Paris")
    expected = "fail"

    assert actual == expected



def test_evaluate_answer_ignores_case():

    actual = evaluators.evaluate_answer("PARIS", "paris")
    expected = "pass"

    assert actual == expected


def test_evaluate_contains_passes_when_expected_text_is_present():

    actual = evaluators.evaluate_contains("The capital of France is Paris.", "Paris")
    expected = "pass"

    assert actual == expected


def test_evaluate_contains_fails_when_expected_text_is_missing():
    actual = evaluators.evaluate_contains(
        "The capital of France is London.",
        "Paris"
    )
    expected = "fail"

    assert actual == expected


def test_create_evaluation_record():
    actual = evaluators.create_evaluation_record(
        "The capital of France is Paris.",
        "Paris",
        "contains",
        "pass"
    )

    expected = {
        "actual": "The capital of France is Paris.",
        "expected": "Paris",
        "evaluator": "contains",
        "status": "pass"
    }

    assert actual == expected



def test_create_evaluation_record_for_failed_exact_match():
    actual = evaluators.create_evaluation_record(
        "The capital of France is London.",
        "Paris",
        "exact_match",
        "fail"
    )

    expected = {
        "actual": "The capital of France is London.",
        "expected": "Paris",
        "evaluator": "exact_match",
        "status": "fail"
    }

    assert actual == expected