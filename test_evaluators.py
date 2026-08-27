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