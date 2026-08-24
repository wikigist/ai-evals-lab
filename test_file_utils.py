import file_utils

def test_no_filename():

    filename = "test_no_filename.json"
    

    actual = file_utils.load_results(filename)
    expected = []

    assert actual == expected 



def test_load_results_invalid_json():

    filename = "broken_results.json"

    actual = file_utils.load_results(filename)
    expected = []

    assert actual == expected


def test_load_results_valid_file():
    filename = "module_test_result.json"

    actual = file_utils.load_results(filename)
    expected = [
    {
        "status": "success",
        "score": 95
    },
    {
        "status": "success",
        "score": 99
    },
    {
        "status": "success",
        "score": 105
    }
]

    assert actual == expected



def test_save_results_round_trip():
    filename = "new_result_save.json"

    data_to_save = [
        {"status": "success", "score": 77}
    ]

    file_utils.save_results(data_to_save, filename)

    actual = file_utils.load_results(filename)
    expected = data_to_save

    assert actual == expected



def test_save_results_with_tmp_path(tmp_path):
    filename = tmp_path / "test_results.json"

    data_to_save = [
        {"status": "success", "score": 77}
    ]

    file_utils.save_results(data_to_save, filename)

    actual = file_utils.load_results(filename)
    expected = data_to_save

    assert actual == expected


def test_load_results_missing_file_with_tmp_path(tmp_path):
    filename = tmp_path / "missing.json"

    actual = file_utils.load_results(filename)
    expected = []

    assert actual == expected


def test_load_results_invalid_json_with_tmp_path(tmp_path):
    filename = tmp_path / "broken.json"

    invalid_json = '[{"status": "success", "score": 87}'

    with open(filename, "w") as file:
        file.write(invalid_json)

    actual = file_utils.load_results(filename)
    expected = []

    assert actual == expected




def test_load_results_valid_json_with_tmp_path(tmp_path):
    filename = tmp_path / "valid.json"

    valid_json = '[{"status": "success", "score": 88}]'

    with open(filename, "w") as file:
        file.write(valid_json)

    actual = file_utils.load_results(filename)
    expected = [{"status": "success", "score": 88}]

    assert actual == expected






def test_load_results_valid_file_with_tmp_path(tmp_path):
    filename = tmp_path / "the_valid.json"

    valid_json_2 = '[{"status": "success", "score": 97}]'

    with open(filename, "w") as file:
        file.write(valid_json_2)

    actual = file_utils.load_results(filename)
    expected = [
        {"status": "success", "score": 97}
    ]

    assert actual == expected




def test_add_result_to_missing_file(tmp_path):
    filename = tmp_path / "results.json"

    new_result = {
        "status": "success",
        "score": 91
    }

    actual = file_utils.add_result(new_result, filename)
    expected = [
        {
            "status": "success",
            "score": 91
        }
    ]

    assert actual == expected



def test_add_result_does_not_duplicate(tmp_path):
    filename = tmp_path / "results.json"

    new_result = {
        "status": "success",
        "score": 91
    }

    file_utils.add_result(new_result, filename)
    actual = file_utils.add_result(new_result, filename)

    expected = [
    {
        "status": "success",
        "score": 91
    }
    ]

    assert actual == expected



def test_add_result_adds_different_result(tmp_path):
    filename = tmp_path / "results.json"

    new_result = {
        "status": "success",
        "score": 91
    }

    latest_result = {
        "status": "success",
        "score": 93
    }


    file_utils.add_result(new_result, filename)
    actual = file_utils.add_result(latest_result, filename)

    expected = [

        {
            "status": "success",
            "score": 91
        },
    {
        "status": "success",
        "score": 93
    }
    ]

    assert actual == expected