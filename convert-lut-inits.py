#!/usr/bin/env python3

import argparse
from pathlib import Path

def convert_lut(luttype, val):
    # if luttype in (1, 2):
    if "'" not in val:
        return str(format(int(val), 'x')).upper()
    else:
        return str(val.split("'h")[1]).upper()
    # elif luttype == 3:
    #     raise NotImplementedError()
    # elif luttype == 4:
    #     raise NotImplementedError()
    # else:
    #     raise NotImplementedError()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input",
                        help="EDIF file containing the design",
                        type=Path)
    parser.add_argument("output",
                        help="Output EDIF file",
                        type=Path)

    args = parser.parse_args()

    luttype = -1

    with open(args.input, 'r') as infile:
        with open(args.output, 'w') as outfile:
            lines = []
            for line in infile:
                if '(instance ' in line:
                    luttype = -1
                elif '(cellRef LUT' in line:
                    s = '(cellRef LUT'
                    numloc = line.find(s) + len(s)
                    luttype = int(line[numloc:].split(' ')[0])
                elif '(property INIT' in line and luttype > 0:
                    intpre = '(integer '
                    initdef = line.find(intpre)
                    if initdef == -1:
                        intpre = '(string "'
                    initdef = line.find(intpre)
                    initdefdel = '")' if intpre == '(string "' else ')'
                    initdefend = line.find(initdefdel, initdef)
                    num = line[initdef + len(intpre):initdefend]
                    newval = convert_lut(luttype, num)
                    line = line.replace(line[initdef:initdefend + len(initdefdel)], '(string "{}")'.format(newval))
                lines.append(line)
            outfile.writelines(lines)


