# Tool for converting Yosys EDIF files to SpDE-compliant format

Copyright (c) 2020-2021 [Antmicro](https://www.antmicro.com)

This repository contains script for converting EDIF files generated by [Yosys](http://www.clifford.at/yosys/about.html) tool to format that is compatible with the [SpDE](https://www.quicklogic.com/products/fpga/fpga-development-tools/) software.
In addition, it contains some examples of Verilog designs for QuickLogic QLAL4S3B FPGA, and example scripts for generating EDIF files for SpDE.

The EDIF files generated by Yosys have the values for LUT `INIT` tables represented as decimal integer or hexadecimal values in Verilog format (i.e. `"12'hCAB"`).
SpDE only accepts the hexadecimal values in string, (i.e. `"CAB"`).
What is more, Yosys introduces arrays that are not supported by SpDE for blackbox ports.
The `postprocess-yosys-edif.py` script converts all values for `INIT` tables to hexadecimal values, and replaces arrays by wires.

## Requirements

* Python 3.7 or higher,
* [fd tool](https://github.com/sharkdp/fd) (a nice alternative to `find`, required by the `verilogs-to-edifs-yosys.sh` script),
* Yosys from [Antmicro's fork](https://github.com/antmicro/yosys), checked out to `quicklogic` branch:
  ```
  git clone https://github.com/antmicro/yosys.git -b quicklogic quicklogic-yosys
  ```

## Usage

To install the `yosys_spde_flow` package, run:
```
sudo pip3 install git+https://github.com/antmicro/yosys-SpDE-flow.git
```

To process the EDIF file generated by Yosys, run:
```
python3 -m yosys_spde_flow.postprocess_yosys_edif in.edf out.edf
```

## Synthesizing basic designs for SpDE with `verilogs-to-edifs-yosys.sh`

First of all, generate the EDIF file with Yosys:

```
read_verilog top.v
synth_quicklogic -flatten -edif top-tmp.edf
```

`NOTE:` It is important to flatten the design for SpDE, especially complex ones.
Without flattening, Yosys can create lots of VCC and GND blocks, which may result in SpDE fatal error.

After generating EDIF file with Yosys, i.e. `top.edf`, you can convert it to SpDE format with a following command:

```
python postprocess-yosys-edif.py top.edf top-spde.edf
```

You can also use the `verilogs-to-edifs-yosys.sh` script so it performs all the steps for you.
This script generates both Yosys EDIFs and SpDE EDIFs for every Verilog file in the input directory.
The example call is following:
```
./verilogs-to-edifs-yosys.sh /path/to/quicklogic-yosys/yosys ./qlogic-verilogs ./yosys-edifs ./spde-edifs
```

* The first parameter is the path to the built Yosys binary with QuickLogic support.
* The second argument is the directory with Verilog files to process,
* The third argument is a directory that will contain EDIF files generated by Yosys.
  This directory will be CLEARED and CREATED again.
* The fourth argument is a directory that will contain EDIF files generated by `postprocess-yosys-edif.py` script.
  Those files can be opened by SpDE.
  This directory will also be CLEARED and CREATED again.

After generating the EDIF file with Python script, you should be able to load the design (you may only need to retarget it to desired device).

