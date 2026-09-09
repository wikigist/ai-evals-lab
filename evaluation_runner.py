import file_utils
import evaluators

def run_evaluation_file(filename):
    cases = file_utils.load_required_results(filename)
    evaluators.validate_evaluation_dataset(cases)
    suite_result = evaluators.run_evaluation_suite(cases)
    return suite_result


