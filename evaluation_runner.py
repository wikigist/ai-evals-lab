import file_utils
import evaluators

def run_evaluation_file(filename, model, prompt_version, dataset_name):
    cases = file_utils.load_required_results(filename)
    suite_result = evaluators.run_evaluation_suite(cases, model, prompt_version, dataset_name)
    return suite_result


