import metrics

def test_calculate_pass_mixed():
    results = [
        {"status": "pass"},
        {"status": "fail"},
        {"status": "pass"},
        {"status": "pass"},

    ]

    actual = metrics.calculate_pass_rate(results)
    expected = 0.75

    assert actual == expected



def test_calculate_pass_rate_empty():
    results = []

    actual = metrics.calculate_pass_rate(results)
    expected = 0

    assert actual == expected



def test_calculate_pass_rate_all_fail():
    results = [
        {"status": "fail"},
        {"status": "fail"},
        {"status": "fail"},

    ]

    actual = metrics.calculate_pass_rate(results)
    expected = 0

    assert actual == expected



def test_calculate_pass_rate_all_pass():
    results = [

        {"status": "pass"},
        {"status": "pass"},
        {"status": "pass"},

    ]

    actual = metrics.calculate_pass_rate(results)
    expected = 1.0

    assert actual == expected


def test_calculate_pass_fail():
    results = [
        {"status": "pass"},
        {"status": "fail"},
        {"status": "pass"},
        {"status": "fail"},
    ]

    actual = metrics.calculate_pass_rate(results)
    expected = 0.50

    assert actual == expected