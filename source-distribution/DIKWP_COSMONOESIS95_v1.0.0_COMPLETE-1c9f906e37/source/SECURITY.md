# Security and Misuse Boundaries

## Supported security reports

Please report integrity bypasses, manifest weaknesses, unsafe path handling, code execution vulnerabilities, unauthorized network behavior or privacy leakage.

## Prohibited deployment patterns

Do not use the system for:

- covert religious profiling;
- employment, insurance, immigration, policing or loyalty scoring;
- coercive conversion or belief correction;
- medical diagnosis or treatment replacement;
- attributing disease to moral or mental failure;
- automated transmission to anomalous signals;
- impersonation or representation without consent;
- military targeting based on cultural or consciousness classifications.

## Data handling

The reference implementation is local and standard-library-only. It performs no automatic network request. Outputs may contain sensitive interpretations; owners should control access and redact before public release.

## External action

`automatic_external_action_authority` is fixed at `0`. Removing this constraint creates a fork outside the validated safety contract.
