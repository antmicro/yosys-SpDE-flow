#!/bin/bash

YOSYS=${1%} # Yosys executable
DIR=${2%} # Directory with Verilog files
OUT=${3%} # Output file name

$YOSYS -p "read_verilog $DIR/*; synth_quicklogic -flatten -edif design.edif"
python yosys_spde_flow/postprocess_yosys_edif.py design.edif $OUT
