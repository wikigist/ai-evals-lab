def compare_runs(baseline, candidate):

    baseline_pass_rate = baseline["pass_rate"]
    candidate_pass_rate = candidate["pass_rate"]


    pass_rate_difference = candidate_pass_rate - baseline_pass_rate


    model_changed = baseline["model"] != candidate["model"]
    prompt_version_changed = (baseline["prompt_version"] != candidate["prompt_version"])
    dataset_changed = baseline["dataset_name"] != candidate["dataset_name"]


    changed_count = (model_changed+ prompt_version_changed+ dataset_changed)

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
        "comparison_validity": comparison_validity
        }
