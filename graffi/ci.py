from pathlib import Path
from textwrap import dedent
def generate_ci():
    p = Path('.github/workflows')
    p.mkdir(parents=True, exist_ok=True)
    ci_path = p / 'graffi-omega-ci.yml'
    ci_path.write_text(dedent('''name: Graffi Omega CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Run graffi doctor
        run: |
          python graffi_helper.py doctor
'''))
    return ci_path
