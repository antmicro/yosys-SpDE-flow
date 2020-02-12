#!/bin/bash

SCRIPTDIR=$(dirname "$(realpath $0)")

YOSYS_EXEC=${1%/} # Yosys executable
VERILOG_INPUTS=${2%/} # directory with verilogs to process
YOSYS_EDIFS_DIR=${3%/} # directory in which the EDIFS produced by Yosys should be stored
SPDE_EDIFS_DIR=${4%/} # directory in which the EDIFS produced by Python script for SpDE should be stored

TO_SPDE_CONVERT_SCRIPT=$SCRIPTDIR/yosys-spde-flow/postprocess-yosys-edif.py

rm -rf $YOSYS_EDIFS_DIR/*.edf
rm -rf $SPDE_EDIFS_DIR/*.edf

mkdir -p $YOSYS_EDIFS_DIR
mkdir -p $SPDE_EDIFS_DIR
fd -e v --full-path $VERILOG_INPUTS/ -x $YOSYS_EXEC -p "read_verilog {}; synth_quicklogic -flatten -edif $YOSYS_EDIFS_DIR/{/.}.edf"
fd -e edf --full-path $YOSYS_EDIFS_DIR -x python $TO_SPDE_CONVERT_SCRIPT {} $SPDE_EDIFS_DIR/{/.}.edf
