import app
import file_utils

def test_app_is_empty():

    actual = app.validate_prompt("")
    expected = "empty"

    assert actual == expected




def test_prompt_hello():

    actual = app.validate_prompt("hello")
    expected = "too short"

    assert actual == expected

def test_prompt_valid():

    actual = app.validate_prompt("Explain Python Loops")
    expected = "valid"

    assert actual == expected


def test_prompt_long():

    actual = app.validate_prompt("a" * 501)
    expected = "too long"

    assert actual == expected


def test_right_prompt():

    actual = app.validate_prompt("a" * 10)
    expected = "valid"

    assert actual == expected


def test_valid_prompt():

    actual = app.validate_prompt("a" * 500)
    expected = "valid"

    assert actual == expected




def test_create_interaction_record():
    actual = app.create_interaction_record(
        "What is Python?",
        "Python is a programming language."
    )

    expected = {
        "prompt": "What is Python?",
        "answer": "Python is a programming language.",
        "prompt_length": 15
    }

    assert actual == expected


def test_interaction_record_prompt_length():
    actual = app.create_interaction_record(
        "hello",
        "test answer"
    )

    expected = 5

    assert actual["prompt_length"] == expected


def test_save_interaction_history_new_file(tmp_path):
    filename = tmp_path / "history.json"

    interaction_records = [
        {
            "prompt": "hello world",
            "answer": "test answer",
            "prompt_length": 11
        }
    ]

    app.save_interaction_history(interaction_records,filename)

    actual = file_utils.load_results(filename)
    expected = interaction_records

    assert actual == expected



def test_save_interaction_history_preserves_old_records(tmp_path):
    filename = tmp_path / "history.json"

    old_records = [
        {
            "prompt": "old question",
            "answer": "old answer",
            "prompt_length": 12
        }
    ]

    new_records = [
        {
            "prompt": "new_question",
            "answer": "new answer",
            "prompt_length": 12
        }
    ]

    file_utils.save_results(old_records, filename)

    app.save_interaction_history(new_records, filename)

    actual = file_utils.load_results(filename)
    expected = [
         {
            "prompt": "old question",
            "answer": "old answer",
            "prompt_length": 12
        },
    
        {
            "prompt": "new_question",
            "answer": "new answer",
            "prompt_length": 12
        }
    ]

    assert actual == expected



