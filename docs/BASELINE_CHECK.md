# Baseline Check

Use this checklist before starting localization changes. The goal is to ensure the fork still loads, discovers commands, and passes upstream static contracts.

## Environment Notes

- Local Python on this machine currently does not include `pytest`.
- GitHub Actions installs `pytest` separately in `.github/workflows/pytest.yml`.
- To run the full test suite locally, install test dependencies first:

```bash
python3 -m pip install -r requirements-dev.txt pytest
```

## Required Smoke Checks

Run from the repository root:

```bash
node -e "for (const f of ['.claude-plugin/plugin.json','.claude-plugin/marketplace.json','hooks/hooks.json']) JSON.parse(require('fs').readFileSync(f,'utf8')); console.log('json ok')"

python3 scripts/check_version_consistency.py
python3 scripts/check_data_access_level.py
python3 scripts/check_task_type.py
python3 scripts/check_v3_6_8_mark_read_commands.py
python3 scripts/check_v3_10_134_write_scope.py
python3 scripts/check_v3_9_2_phase_boundary.py
python3 scripts/check_v3_6_7_pattern_protection.py
python3 scripts/check_ci_pytest_manifest.py

python3 scripts/ars_cache_invalidate.py --help
python3 scripts/ars_mark_read.py --help
bash scripts/announce-ars-loaded.sh
```

## Command Reference Check

The command coverage audit is documented in `docs/UPSTREAM_CAPABILITY_AUDIT.md`. At baseline, all 14 slash commands must point to existing skills, modes, or direct scripts.

## Full Test Suite

After installing `pytest`, run:

```bash
python3 -m pytest scripts/ tests/
```

Some tests may depend on optional tools or network/API configuration. Treat the required smoke checks above as the minimum pre-localization gate.
