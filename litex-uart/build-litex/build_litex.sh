#!/bin/bash

LITEX_GEN=${1%} # Path to litex_gen.py script

python $LITEX_GEN --with-uart --uart-no-fifo --no-compile-gateware --no-compile-software
