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
    


def compare_runs(baseline, candidate):

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

    return {
        "baseline_pass_rate": baseline_pass_rate,
        "candidate_pass_rate": candidate_pass_rate,
        "pass_rate_difference": pass_rate_difference,
        "outcome": outcome,
        "comparison_validity": comparison_validity,
        "comparison_type": comparison_type,
        "changed_fields": changed_fields,
        "changed_count": changed_count
        }
