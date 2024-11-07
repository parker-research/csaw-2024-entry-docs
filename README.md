# csaw-2024-entry-docs
Documentation for my entry in the CSAW 2024 competition

* Challenge documentation: https://docs.google.com/document/d/1POekJf40zNocSZcW5b8qP-nlq37Dnbj-Nf1Oe7FnchM/edit?tab=t.0

The project involves injecting a vulnerability into a RISC-V core design and then obfuscating the design to hide the vulnerability. The project uses the Aider Chat tool and ChatGPT to generate the vulnerability.

This repository contains several sub-tools to help with parts of this process (including summarizing a large Verilog design, and obfuscating changes to that design).


## Tool Setup and Usage

```bash
# 1. Clone and cd into this repo.
git clone https://github.com/parker-research/csaw-2024-entry-docs
cd csaw-2024-entry-docs

# 2. Create a virtual environment. Install project.
python3 -m venv venv/
. venv/bin/activate
pip install -e .

# 3. Check it can run.
parker_csaw --help

# 4. Copy the `secrets.sample.yml` to `secrets.yml` and fill in the values.
cp secrets.sample.yml secrets.yml
nano secrets.yml

# 4. Run the tool - "summarize-modules" sub-tool.
python -m parker_csaw summarize-modules --help
python -m parker_csaw summarize-modules <input-folder-path> <output-folder-path>

# 5. Run the tool - "obfuscate" sub-tool.
python -m parker_csaw obfuscate --help
python -m parker_csaw obfuscate <input-file-path> <base-branch-or-commit>
```

## GitHub Repos

* Tools and Documentation: https://github.com/parker-research/csaw-2024-entry-docs
* Modified RISC-V Core with Vulnerability Injection: https://github.com/parker-research/ultraembedded-riscv-csaw-2024
    * Branch: `02-trial-gcc` contains Dockerfile to run the testbenches with C code.
    * Branch: `03-modify-verilog` contains the Verilog vulnerability injection.
    * Branch: `04-obfuscate-verilog` contains the obfuscation tool.
