#!/bin/bash

mkdir -p ./qlogic-edifs
fd -e v --full-path './qlogic-verilogs/' -x ./yosys -p "read_verilog {}; synth_quicklogic; write_edif qlogic-edifs/{/.}.edf"
