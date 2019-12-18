#!/bin/bash

mkdir -p ./qlogic-edifs
mkdir -p ./qlogic-edifs-sdpe
fd -e v --full-path './qlogic-verilogs/' -x ./yosys -p "read_verilog {}; synth_quicklogic -edif qlogic-edifs/{/.}.edf"
fd -e edf --full-path './qlogic-edifs/' -x python ./convert-lut-inits.py {} qlogic-edifs-sdpe/{/.}.edf
