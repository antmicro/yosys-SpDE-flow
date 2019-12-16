# Helper files and scripts for working with Yosys and SpDE software

This repository contains useful files, mini-guides and scripts for Yosys and SpDE software.

## Requirements

The `verilogs-to-edifs-yosys.sh` file requires `fd` tool to process files.

## Generating EDIF files

In order to generate EDIF files for example Verilogs for QuickLogic with Yosys you need to copy the `qlogic-verilogs` directory to the root directory of the built Yosys project, and the `verilogs-to-edifs-yosys.sh` script.
After this, just run the script.
It will generate `qlogic-edifs` directory with appropriate EDIF files.
