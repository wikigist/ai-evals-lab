import file_utils
from datetime import datetime, timezone
import math
from uuid import uuid4


def generate_comparison_id():
    return f"cmp_{uuid4()}"


def determine_outcome(pass_rate_difference):
    if pass_rate_difference > 0:
        return "improvement"
    elif pass_rate_difference < 0:
        return "regression"
    else:
        return "tie"


def determine_changed_fields(model_changed, prompt_version_changed, dataset_changed):

    changed_fields = []

    if model_changed:
        changed_fields.append("model")

    if prompt_version_changed:
        changed_fields.append("prompt_version")

    if dataset_changed:
        changed_fields.append("dataset_name")

    return changed_fields


def determine_comparison_validity(changed_count):
    if changed_count == 1:
        return "clean"
    elif changed_count > 1:
        return "confounded"
    else:
        return "same_setup"


def determine_comparison_type(
    model_changed,
    prompt_version_changed,
    dataset_changed,
    changed_count
    ):

    if model_changed and not prompt_version_changed and not dataset_changed:
        return "model"

    elif prompt_version_changed and not model_changed and not dataset_changed:
        return "prompt"

    elif dataset_changed and not model_changed and not prompt_version_changed:
        return "dataset"

    elif changed_count > 1:
        return "confounded"

    else:
        return "same_setup"
    


def compare_runs(baseline, candidate, allowed_regression=None):

    baseline_pass_rate = baseline["pass_rate"]
    candidate_pass_rate = candidate["pass_rate"]


    pass_rate_difference = candidate_pass_rate - baseline_pass_rate


    model_changed = baseline["model"] != candidate["model"]
    prompt_version_changed = (baseline["prompt_version"] != candidate["prompt_version"])
    dataset_changed = baseline["dataset_name"] != candidate["dataset_name"]


    changed_fields = determine_changed_fields(model_changed, prompt_version_changed, dataset_changed)


    changed_count = len(changed_fields)

    comparison_type = determine_comparison_type(model_changed, prompt_version_changed, dataset_changed, changed_count)


    comparison_validity = determine_comparison_validity(changed_count)


    outcome = determine_outcome(pass_rate_difference)


    comparison = {
        "baseline_pass_rate": baseline_pass_rate,
        "candidate_pass_rate": candidate_pass_rate,
        "pass_rate_difference": pass_rate_difference,
        "outcome": outcome,
        "comparison_validity": comparison_validity,
        "comparison_type": comparison_type,
        "changed_fields": changed_fields,
        "changed_count": changed_count,
        "baseline_model": baseline["model"],
        "candidate_model": candidate["model"],
        "baseline_prompt_version": baseline["prompt_version"],
        "candidate_prompt_version": candidate["prompt_version"],
        "baseline_dataset_name": baseline["dataset_name"],
        "candidate_dataset_name": candidate["dataset_name"]
        }

    if allowed_regression is not None:
        comparison["quality_gate"] = determine_quality_gate(
            pass_rate_difference,
            allowed_regression
            )
        comparison["allowed_regression"] = allowed_regression

    if "run_id" in baseline and "run_id" in candidate:
        comparison["baseline_run_id"] = baseline["run_id"]
        comparison["candidate_run_id"] = candidate["run_id"]

    return comparison


def is_same_comparison(existing, current):
    return (
        math.isclose(existing["baseline_pass_rate"], current["baseline_pass_rate"])
        and math.isclose(existing["candidate_pass_rate"], current["candidate_pass_rate"])
        and existing["baseline_model"] == current["baseline_model"]
        and existing["candidate_model"] == current["candidate_model"]
        and existing["baseline_prompt_version"] == current["baseline_prompt_version"]
        and existing["candidate_prompt_version"] == current["candidate_prompt_version"]
        and existing["baseline_dataset_name"] == current["baseline_dataset_name"]
        and existing["candidate_dataset_name"] == current["candidate_dataset_name"]
        )



def extract_existing_comparisons(saved_results):

    existing_comparisons = []

    for saved_result in saved_results:
        if "comparison" in saved_result:
            existing_comparisons.append(saved_result["comparison"])
        else:
            existing_comparisons.append(saved_result)

    return (existing_comparisons)



def has_same_comparison(existing_comparisons, comparison):
    same_comparison_found = False

    for existing_comparison in existing_comparisons:
        if is_same_comparison(existing_comparison, comparison):
            same_comparison_found = True
        break

    return same_comparison_found




def compare_and_save_runs(baseline, candidate, filename, allowed_regression=None):
    comparison = compare_runs(baseline, candidate, allowed_regression=allowed_regression)

    timestamp = datetime.now(timezone.utc).isoformat()

    saved_results = file_utils.load_results(filename)

    record = {
        "comparison_id": generate_comparison_id(),
        "comparison": comparison,
        "timestamp": timestamp
        }

    existing_comparisons = extract_existing_comparisons(saved_results)

    same_comparison_found = has_same_comparison(existing_comparisons, comparison)

    if not same_comparison_found:
        saved_results.append(record)

        file_utils.save_results(saved_results, filename)

    return comparison


def determine_quality_gate(pass_rate_difference, allowed_regression):
    if pass_rate_difference >= -allowed_regression:
        return "pass"
    else:
        return "fail"
