# switchtest

`switchtest` is a Python-based CLI framework for automating functional and security validation of network switches over SSH.

It is designed to let you define switch checks in YAML, run them against a real device, and generate machine-readable reports for engineering teams, QA, and CI/CD pipelines.

## What The Project Is About

This project exists to make switch validation repeatable, scriptable, and safe enough for regular use during:

- firmware upgrade validation,
- pre-production acceptance testing,
- regression testing,
- CIS-aligned hardening checks,
- lab smoke testing,
- CI/CD gating for network change workflows.

Instead of manually typing commands on a switch and checking output by eye, `switchtest` lets you:

1. define tests in YAML,
2. connect to a switch over SSH,
3. run setup steps and verification commands,
4. evaluate expected output,
5. collect structured results,
6. export JSON and JUnit reports.

The current implementation targets a single switch at a time and includes an AOS driver tuned for Alcatel-Lucent Enterprise OmniSwitch devices running AOS8.

## Current Capabilities

The project currently supports:

- SSH-based switch access,
- declarative YAML testcases and suites,
- read-only and config-changing test steps,
- validation types:
  - `contains`
  - `not_contains`
  - `regex`
  - `equals`
  - `ping`
- JSON reporting,
- JUnit XML reporting,
- dry-run mode,
- fail-fast mode,
- environment-variable-based secrets,
- AOS-specific metadata parsing,
- CIS-aligned smoke checks for AOS8 management hardening.

## Project Structure

```text
SwitchTestSuite/
├── configs/
│   ├── baselines/
│   ├── defaults.yaml
│   └── devices.yaml
├── reports/
├── suites/
│   ├── cis_smoke.yaml
│   ├── regression.yaml
│   └── smoke.yaml
├── testcases/
│   ├── cis/
│   ├── l3/
│   ├── system/
│   └── vlan/
├── tests/
└── src/
    └── switchtest/
```

## Getting Started

### Prerequisites

- Python 3.11+
- A reachable switch with SSH enabled
- Valid switch credentials
- Windows PowerShell or `cmd.exe`, or a Linux shell

### Install

From the project root:

```powershell
venv\Scripts\python.exe -m pip install -e .[dev]
venv\Scripts\switchtest --help
venv\Scripts\python.exe -m pytest
```

If the virtual environment is already activated, you can use `switchtest` directly.

## Configuration

### Devices

Devices are defined in [configs/devices.yaml](../SwitchTestSuite/configs/devices.yaml).

Example:

```yaml
devices:
  - name: ACSSW01
    host: 192.168.70.1
    port: 22
    username: admin
    password_env: SWITCH_SW1_PASSWORD
    enable_password_env:
    platform: aos
    baseline_strategy: load_config
    baseline_source: configs/baselines/core_switch.cfg
    expected_prompt: "ACSW01->"
    tags: [lab, core]
    connection_timeout: 15
    command_timeout: 30
    strict_host_key: false
```

Important:
- `password_env` is the name of the environment variable, not the password itself.
- `platform` currently supports `aos`.

### Secrets

In PowerShell:

```powershell
$env:SWITCH_SW1_PASSWORD="your-password"
```

In `cmd.exe`:

```cmd
set SWITCH_SW1_PASSWORD=your-password
```

## How To Run Tests

### Run a suite

Run the standard smoke suite:

```powershell
venv\Scripts\switchtest run --device ACSSW01 --suite suites\smoke.yaml --report-dir reports --json reports\result.json --junit reports\junit.xml
```

Run the CIS-aligned suite:

```powershell
venv\Scripts\switchtest run --device ACSSW01 --suite suites\cis_smoke.yaml --report-dir reports --json reports\cis_result.json --junit reports\cis_junit.xml
```

### Dry-run

Use dry-run to validate suite loading and execution flow without making device changes:

```powershell
venv\Scripts\switchtest run --device ACSSW01 --suite suites\smoke.yaml --report-dir reports --dry-run
```

### Validate YAML files

Validate a suite:

```powershell
venv\Scripts\switchtest validate-suite suites\cis_smoke.yaml
```

Validate a testcase:

```powershell
venv\Scripts\switchtest validate-testcase testcases\cis\check_snmpv3_configured.yaml
```

### List configured devices

```powershell
venv\Scripts\switchtest list-devices
```

## Reports

Successful and failed runs produce structured artifacts in `reports/`.

Typical outputs:

- `result.json` or `cis_result.json`
- `junit.xml` or `cis_junit.xml`
- `run-<timestamp>-<id>.summary.txt`

### JSON report

The JSON report contains:

- suite metadata,
- device metadata,
- test-level status,
- validation-level status,
- observed output,
- expected values,
- timings,
- cleanup state.

### JUnit XML

JUnit output is suitable for CI/CD systems such as Jenkins, GitLab CI, GitHub Actions, or Azure DevOps test reporting.

## Testcase Format

Testcases are YAML files under `testcases/`.

Example: [testcases/system/login.yaml](../SwitchTestSuite/testcases/system/login.yaml)

```yaml
id: TC-SYS-001
name: Verify management session and show system response
description: Validate that the switch accepts a session and returns key system information.
feature: system
tags: [smoke, system]
severity: high
setup: []

validations:
  - name: Show system includes description
    type: contains
    command: show system
    expected: "Description:"

  - name: Show system includes device name
    type: contains
    command: show system
    expected: "Name:         ACSW01"

cleanup: []
continue_on_failure: false
timeout: 60
```

## Validation Types

Supported validation types:

- `contains`
  Passes when `expected` exists in command output.
- `not_contains`
  Passes when `expected` does not exist in output.
- `regex`
  Passes when `pattern` matches the output.
- `equals`
  Passes when normalized output equals normalized expected text.
- `ping`
  Runs a host-side ping check instead of a switch CLI command.

## Suites

Suites are lists of testcase file paths.

Example: [suites/cis_smoke.yaml](../SwitchTestSuite/suites/cis_smoke.yaml)

```yaml
name: cis_smoke
description: CIS-aligned smoke validation for AOS8 management and hardening posture
tests:
  - ../testcases/system/login.yaml
  - ../testcases/system/check_firmware.yaml
  - ../testcases/cis/check_ssh_enabled.yaml
  - ../testcases/cis/check_telnet_disabled.yaml
  - ../testcases/cis/check_http_disabled.yaml
  - ../testcases/cis/check_https_enabled.yaml
  - ../testcases/cis/check_ntp_configured.yaml
  - ../testcases/cis/check_syslog_configured.yaml
  - ../testcases/cis/check_aaa_configured.yaml
  - ../testcases/cis/check_snmpv3_configured.yaml
```

## Example Workflows

### Example 1: Verify the switch firmware

Use [testcases/system/check_firmware.yaml](../SwitchTestSuite/testcases/system/check_firmware.yaml) to confirm the expected AOS release:

```powershell
venv\Scripts\switchtest run --device ACSSW01 --suite suites\smoke.yaml --report-dir reports --json reports\result.json --junit reports\junit.xml
```

Expected metadata in the JSON report:

```json
"firmware_version": "8.9.221.R03 GA",
"device_model": "OS6860E-P24"
```

### Example 2: Run CIS-aligned checks

```powershell
venv\Scripts\switchtest run --device ACSSW01 --suite suites\cis_smoke.yaml --report-dir reports --json reports\cis_result.json --junit reports\cis_junit.xml
```

This suite currently checks:

- management session responsiveness,
- firmware,
- SSH enabled,
- Telnet disabled,
- HTTP/WebView state,
- HTTPS/WebView enforcement,
- NTP sync,
- syslog configuration,
- AAA configuration,
- SNMPv3 posture.

## How To Add A New Testcase

1. Create a YAML file under the appropriate folder in `testcases/`.
2. Define `id`, `name`, `description`, `feature`, and `validations`.
3. Add the testcase path to a suite in `suites/`.
4. Validate the testcase.
5. Run the suite.

Example:

```powershell
venv\Scripts\switchtest validate-testcase testcases\system\check_firmware.yaml
venv\Scripts\switchtest validate-suite suites\smoke.yaml
```

## How To Tune Tests To Your Switch

Network devices often vary slightly by:

- command syntax,
- output formatting,
- feature names,
- enabled services,
- prompt style.

When a testcase fails:

1. inspect the `observed` output in the JSON report,
2. compare it with the YAML `expected` or `pattern`,
3. tune the testcase to the actual CLI output.

This is especially important for CIS-aligned checks because different AOS8 builds may expose services and security settings differently.

## Exit Codes

The CLI uses structured exit codes:

- `0` success
- `1` test failure
- `2` framework error
- `3` device connection error
- `4` cleanup failure
- `5` invalid input

## Notes About The Current AOS Driver

The AOS driver in [aos.py](../SwitchTestSuite/src/switchtest/drivers/aos.py) includes:

- metadata extraction from `show system`,
- cleanup of echoed prompt/command lines,
- retry on transient empty `show` output,
- Windows-safe SSH transport selection,
- suppression of noisy Windows close-time socket warnings from Paramiko.

This means the current implementation is already tuned to the OmniSwitch/AOS8 behavior observed in this repository’s lab runs.

## Development

Run tests:

```powershell
venv\Scripts\python.exe -m pytest
```

Run lint:

```powershell
venv\Scripts\python.exe -m ruff check .
```

## Limitations

Current limitations:

- one switch at a time,
- one platform driver (`aos`),
- CIS suite is CIS-aligned, not an official vendor-specific CIS benchmark,
- some testcases still need environment-specific tuning depending on switch configuration,
- console progress output is minimal and most detail is in reports.

## Next Steps

Useful next improvements:

- stricter AAA validation,
- stronger SNMPv3 checks,
- syslog-over-TLS validation,
- configuration drift checks,
- better console progress output,
- more AOS8 hardening testcases,
- multi-device topology testing.
