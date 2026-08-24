import json 

def load_results(filename):
    try:
        with open(filename, "r") as file:
            results = json.load(file)
        return results

    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []



def save_results(results, filename):
    with open(filename, "w") as file:
        json.dump(results, file, indent=4)


def add_result(result, filename):
    results = load_results(filename)

    if result not in results:
        results.append(result)

    save_results(results, filename)

    return results