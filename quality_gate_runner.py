def enforce_gate_action(gate_action):
    if gate_action == "allow":
        raise SystemExit(0)

    if gate_action == "block":
        raise SystemExit(1)


    raise ValueError("Unsupported gate action")


def run_gate(comparison):
    gate_action = comparison["gate_action"]
    enforce_gate_action(gate_action)