def calculate_pass_rate(results):
    if len(results) == 0:
        return 0

    passed = 0

    for result in results:
        if result["status"] == "pass":
            passed += 1

    return passed / len(results)