# csaw-2024-entry-docs
Documentation for my entry in the CSAW 2024 competition

## Repo Contents

* `docs/` - Notes for the project.
* `parker_csaw/` - Python tool package for the project (`summarize-modules` and `obfuscate` sub-tools).
* `secrets.sample.yml` - Sample secrets file. Required to run tools.

## Project Overview

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
    * Notable Branches:
        * Branch: `patch-dockerfile` contains a contribution submitted upstream to add a Dockerfile, which pins dependencies.
        * Branch: `02-trial-gcc` contains Dockerfile to run the testbenches with C code.
        * Branch: `03-modify-verilog` contains the Verilog vulnerability injection.
        * Branch: `04-obfuscate-verilog` contains the obfuscation tool.
    * Notable files in the `04-xxx` and `03-xxx` branches:
        * `isa_sim/images/vuln_demo_1/payload/injection_demo_payload_1.s` contains the RISC-V assembly code for a sample vulnerability payload.
        * `isa_sim/images/vuln_demo_1/base_code/injection_demo_1.c` contains the C code for a 
        program which runs normally on an unmodified core, and contains code equivalent to a user sending input
        which triggers the vulnerability on the modified core.
        * `core/riscv/riscv_exec.v` contains the AI-generated vulnerability injection which allows the payload to trigger the vulnerability.
