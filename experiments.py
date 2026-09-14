def compare_runs(baseline, candidate):

    baseline_pass_rate = baseline["pass_rate"]
    candidate_pass_rate = candidate["pass_rate"]


    pass_rate_difference = candidate_pass_rate - baseline_pass_rate


    model_changed = baseline["model"] != candidate["model"]
    prompt_version_changed = (baseline["prompt_version"] != candidate["prompt_version"])
    dataset_changed = baseline["dataset_name"] != candidate["dataset_name"]


    changed_fields = []

    if model_changed:
        changed_fields.append("model")

    if prompt_version_changed:
        changed_fields.append("prompt_version")

    if dataset_changed:
        changed_fields.append("dataset_name")


    changed_count = len(changed_fields)

    if model_changed and not prompt_version_changed and not dataset_changed:
        comparison_type = "model"

    elif prompt_version_changed and not model_changed and not dataset_changed:
        comparison_type = "prompt"

    elif dataset_changed and not model_changed and not prompt_version_changed:
        comparison_type = "dataset"

    elif changed_count > 1:
        comparison_type = "confounded"

    else:
        comparison_type = "same_setup"



    if changed_count == 1:
        comparison_validity = "clean"
    elif changed_count > 1:
        comparison_validity = "confounded"
    else:
        comparison_validity = "same_setup"



    if pass_rate_difference > 0:
        outcome = "improvement"

    elif pass_rate_difference < 0:
        outcome = "regression"

    else: 
        outcome = "tie"

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
