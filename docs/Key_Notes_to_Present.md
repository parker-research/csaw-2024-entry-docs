# Key Notes to Present

## Plan

1. Very clear vulnerability. Not targeting glitch/leak vulnerability injections, but rather something more applicable for a supply chain attack.
2. Obscure the injected code, and potentially make it over many injections.
3. All tests, in their original states, _must_ continue to pass.
4. We do not care about LUTs/footprint. We will use only registers to add this extra logic.
5. Not a theoretical vulnerability. Very real injection.
6. Threat model: Any user interacting with the RISC-V core on an SoC (e.g., via UART, with a keyboard, etc.) should be able to exploit this vulnerability.
7. Demo with an FPGA+SoC, using UART receives perhaps (pending sufficient time).


## Techniques

* Start new/fresh chats with ChatGPT. Make it focus on only what you're giving it.
* Try the exact prompt multiple times. If it's not giving the same answer on a factual or opinion question (e.g., where to target), you might not be giving it enough info.
    * E.g., prompt it with summaries instead of `du -a` listing.
* Tell the LLM it's an "optimization" and not a "vulnerability injection".


## Artifacts

* C code.
* Verilog changes.
* Aider log.
* ChatGPT logs.
* Markdown summary of the Verilog modules.
* Diagrams.
* Demo video.
* Presentation slides.
* Report.
* Dockerfile for the RISC-V core.
* Samples of the exploit being run on the core.


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

## Future Steps

* This project focused on designing an exploit. Next step is to focus on applying this exploit to other Verilog designs.
* Create tool to automatically inject this vulnerability to any arbitrary RISC-V core.
* Autonomous testing with and control of the Aider Chat tool.
* Work with designs like picorv32 by Yosys, RISC-V-Processor, ibex from OpenTitan, etc.
