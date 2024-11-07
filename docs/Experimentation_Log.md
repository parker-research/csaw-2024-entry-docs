# Experimentation Log

This log aims to document all steps completed during the progression of the project.

## 2024-10-15

- Created and submitted proposal for future work.

## 2024-10-25

- Created the project [repositories on GitHub](https://github.com/parker-research?tab=repositories&q=csaw&type=&language=&sort=).
- Ran various commands in the `picorv32-csaw-2024` repository to experiment with the PicoRV32 core.

```bash
make download-tools
make test_ez # Pass.

make test # Does work without external tools.
```

- Installed the gcc toolchain, following instructions in the README of the picorv32, but modified a bit:
```bash
# Ubuntu packages needed:
sudo apt-get install autoconf automake autotools-dev curl libmpc-dev \
        libmpfr-dev libgmp-dev gawk build-essential bison flex texinfo \
    gperf libtool patchutils bc zlib1g-dev git libexpat1-dev

sudo mkdir /opt/riscv32i
sudo chown $USER /opt/riscv32i

git clone https://github.com/riscv/riscv-gnu-toolchain riscv-gnu-toolchain-rv32i
cd riscv-gnu-toolchain-rv32i
git checkout 411d134 # <- Skip this step, and use the latest version (7aa6d5e, right now).
git submodule update --init --recursive

mkdir build; cd build
../configure --with-arch=rv32i --prefix=/opt/riscv32i
make -j$(nproc)

# Check that it's installed:
/opt/riscv32i/bin/riscv32-unknown-elf-gcc --version
```

- Check the build again, successfully:

```bash
cd picorv32-csaw-2024
make test_ez # Still good.
make test # Works now.
```

## 2024-10-28

* Created code to summarize verilog modules.
* Executed summary code on the following projects:
    1. picorv32
    2. ultraembedded-riscv
    3. RISC-V-Processor (https://github.com/ash-olakangal/RISC-V-Processor)

* Line counts of projects:

```
> cat picorv32-csaw-2024/**/*.v | wc -l
9133
> cat RISC-V-Processor-csaw-2024/**/*.v | wc -l
882
> cat ultraembedded-riscv-csaw-2024/**/*.v | wc -l
13992
> cat ultraembedded-biriscv/**/*.v | wc -l
13948

```

## 2024-10-31

### Implementation Planning

* Working on getting an implementation of the proposed bug working with assistance from ChatGPT.

* Constructed base prompt:
> I want to modify the ultraembedded-riscv project to insert an optimization-of-sorts that listening for a specific sequence of "memory store" instructions to be executed (which store the ASCII text "OPTIMIZE_START"). When this happens, I want the address of the next byte in memory past that to be stored to a "optimization_start_memory_address" register. Then, continue executing store instructions as they come in. In the stores, when the ASCII bytes "DONE" get stored, record the address of the "D" character into a memory called optimization_end_memory_address. Important optimization bytes will be stored in memory between those two addresses stored in registers which will be used later. 

* GPT Chat: Learn about RISC-V instructions and store widths.
* GPT Chat: Explain project a few times to see how it does. Did bad; didn't even grasp suggesting a state machine.
* GPT Chat: Give it problem prompt, description of summary, and summary.

> (Base project) I'm about to paste in a summary of each of the modules in the project. Please help rank the top 3 modules we should explore to setup a state machine which will track and then store these elements. (Summary)

* Investigate these modules (same suggestions twice):
    * riscv_lsu (Load/Store Unit)
    * dcache_core (Data Cache Core)
    * riscv_exec (Execution Unit)

* Doing it with filename, we got these:
    * riscv_core.v
    * riscv_decoder.v (x2)
    * dcache_core.v
    * riscv_lsu.v

### ultraembedded-riscv Test Setup

* Must install libelf: `sudo apt install libelf-dev`
* Must install `bfd.h` from binutils-dev: `sudo apt install binutils-dev`
* Discovered SoC: https://github.com/ultraembedded/riscv_soc
* Easiest to setup oss-cad: https://github.com/YosysHQ/oss-cad-suite-build
* After a while, created a good Dockerfile that lets you build and move on with life, as well as a Gitignore. Using that now.
* Decompile .elf files with: `/opt/riscv32i/bin/riscv32-unknown-elf-objdump --disassemble-all ./basic.elf  > basic.elf.disasm`

* Inside Docker container:
```bash
cd /project/top_tcm_axi/tb
make clean
make
make run

# Run a specific .elf file.
./build/test.x -f ../../isa_sim/images/basic.elf
```

```
./build/test.x --help

        SystemC 2.3.3-Accellera --- Nov  1 2024 03:34:48
        Copyright (c) 1996-2018 by all Contributors,
        ALL RIGHTS RESERVED

Info: (I702) default timescale unit used for tracing: 1 ns (sysc_wave.vcd)
./build/test.x: invalid option -- '-'
./build/test.x: invalid option -- 'h'
Usage:
-f filename.elf = Executable to load (ELF)
-t [0/1]        = Enable program trace
-v 0xX          = Trace Mask
-c nnnn         = Max instructions to execute
-r 0xnnnn       = Stop at PC address
-e 0xnnnn       = Trace from PC address
-b 0xnnnn       = Memory base address (for binary loads)
-s nnnn         = Memory size (for binary loads)
-p dumpfile.bin = Post simulation memory dump file
-j sym_name     = Symbol for memory dump start
-k sym_name     = Symbol for memory dump end
TB: Aborted at 10 ns

# ./build/test.x -f ../../isa_sim/images/basic.elf -t 1

        SystemC 2.3.3-Accellera --- Nov  1 2024 03:34:48
        Copyright (c) 1996-2018 by all Contributors,
        ALL RIGHTS RESERVED

Info: (I702) default timescale unit used for tracing: 1 ns (sysc_wave.vcd)
Memory: 0x2000 - 0x3cd3 (Size=7KB) [.text]
Memory: 0x3cd4 - 0x3ce7 (Size=0KB) [.data]
Memory: 0x3ce8 - 0x4d07 (Size=4KB) [.bss]
Starting from 0x00002000

Test:
1. Initialised data
2. Multiply
3. Divide
4. Shift left
5. Shift right
6. Shift right arithmetic
7. Signed comparision
8. Word access
9. Byte access
10. Comparision
TB: Aborted at 109020 ns
```

* Finally got ultraembedded-riscv working with linker script and gcc so we can run arbitrary code. Demo examples in `02-trial-gcc`.

* Next steps: Get GPT to create C code to test it. Assert that it works as-is now. Then, get GPT to start injecting the vulnerability.

## 2024-11-01

### Create Vulnerability Injection Payload

> What is a good sequence of RISC-V instructions to run to illustrate that a remote code execution vulnerability is being executed, without being malicious?

> Help me write RISC-V assembly which will call the following C function on loop, with the argument containing the ASCII value of "X".
```c
static inline void sim_putc(int ch)
{
    const unsigned int arg = CSR_SIM_CTRL_PUTC | (ch & 0xFF);
    asm volatile ("csrw dscratch,%0": : "r" (arg));
}
```

* Created the payload we'll try to inject. We're going to inject it as hex so it's covert and easy to inject (e.g., using a keyboard).
```
# `isa_sim/images/vuln_demo_1/injection_demo_payload_1.s`
hexdump -C payload.bin
00000000  b7 02 00 01 13 03 80 05  13 73 f3 0f b3 e2 62 00  |.........s....b.|
00000010  73 90 22 7b 6f f0 df ff                           |s."{o...|

# Simply:
b7020001130380051373f30fb3e262007390227b6ff0dfff
```

* 24 bytes of instructions at 4 bytes (32 bits) per instruction is 6 instructions. Very simple demo.

* Now, create C code which writes that to an array using Store Byte instructions. Easy.

### Verilog Modification

* Start branch `03-modify-verilog`.

* Tough finding the place to insert the finite state machine. Try breaking it up.

* Modifying scope a bit. New base prompt:

> I want to modify the ultraembedded-riscv project (written in Verilog) to insert an optimization-of-sorts that listens for a specific sequence of "STORE BYTE (SB)" instructions to be executed (which store the ASCII text `OPTIMIZ[`). When this happens, I want the address of the next byte in memory past that to be stored to a `optimization_start_memory_address` register. Then, continue executing store instructions as they come in. In the stores, when the ASCII byte "]" gets stored, record the address of the "]" character into a memory called `optimization_end_memory_address`. Important optimization bytes will be stored in memory between those two addresses stored in registers which will be used later. 

> I want to modify the ultraembedded-riscv project (written in Verilog) to insert an optimization-of-sorts. We've already inserted some of the optimization, and there is now a `optimization_start_memory_address` output from the `riscv_exec` module. Now, I want to pass this value to the place where the program counter is updated with branches. When `optimize_state == 5'd8`, I want the processor to jump-and-link (jal) to the `optimization_start_memory_address` and start executing from there, until it reaches the `optimization_end_memory_address`. Then, it should jump back to the original program counter and continue executing as normal.

## 2024-11-02

* Worked on Verilog modifications a bit, especially using Aider.
* Seeing that the code output often makes no sense, and it has trouble tracking inputs/outputs of interconnected modules.

## 2024-11-03

* Working more mostly on Verilog modification.

* Alternative huge pivot idea: Could try to make it so that the processor tries hacks that make the testbenches still pass, but find cases where the result of executing instructions is different. Limit changes to basically random changes to the code.

* Just learned about `lowRISC-ibex`, which may be a better core to mod.

### Verilog Modification

* With ChatGPT and Aider, worked to get the bugs out, update the state machine a bit, and inject the payload.
* Biggest bug was that the payload had the wrong byte ordering. When executed, it caused the core to crash.

* Next design step: Obfuscate the inserted code.
* Next design step: Demo on FPGA, maybe.

## 2024-11-06

* Finishing everything up. Document it all.

```
~/ultraembedded-riscv-csaw-2024 (03-modify-verilog)> docker run -it --rm --user (id -u):(id -g) -v (pwd):/project riscv_build

cd top_tcm_axi/tb


```

* Aider Chat demo:

```bash
# Install Aider. Using Aider 0.60.1.
pip install aider

aider ~/openai_env --model azure/gpt-4o # --model azure/gpt-35-turbo

```

To run the `linux.elf` example, you may have to comment out this assertion line in `testbench.h`.

```c
// sc_assert(base >= 0x00000000 && ((base + size) < (0x00000000 + (64 * 1024))));
```
