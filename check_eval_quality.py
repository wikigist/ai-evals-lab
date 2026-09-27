import evaluation_runner
import experiments
import file_utils
import quality_gate_runner

baseline = file_utils.load_required_results("approved_baseline.json")
candidate = evaluation_runner.run_evaluation_file(
    "evaluation_cases.json",
    "candidate-model",
    "v1",
    "evaluation_cases"
    )

comparison = experiments.compare_runs(
    baseline,
    candidate,
    allowed_regression=0.04
)


print("Baseline pass rate:", comparison["baseline_pass_rate"])
print("Candidate pass rate:", comparison["candidate_pass_rate"])
print("Pass rate difference:", comparison["pass_rate_difference"])
print("Allowed regression:", comparison["allowed_regression"])
print("Gate action:", comparison["gate_action"])

quality_gate_runner.run_gate(comparison)