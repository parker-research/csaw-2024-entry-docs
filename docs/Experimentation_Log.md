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
