#!/usr/bin/env python3

import argparse
from pathlib import Path

def convert_lut_init_to_hex(luttype, val):
    if "'" not in val:
        return str(format(int(val), 'x')).upper()
    else:
        return str(val.split("'h")[1]).upper()

def find_closing_bracket(line, openbracketid):
    opencount = 0
    finid = openbracketid
    for c in line[openbracketid:]:
        if c == '(':
            opencount += 1
        elif c == ')':
            opencount -= 1
        if opencount == 0:
            return finid
        finid += 1
    return -1

def fix_array_line(line, arraysizes):
    arrayid = line.find('(array ')
    if arrayid != -1:
        closing = find_closing_bracket(line, arrayid) + 1
        tocut = line[arrayid:closing]
        tokens = tocut.split(' ')
        numelements = int(tokens[-1][:-1])
        variable_base = tokens[2]
        orig_var = tokens[3].split('(')[0][1:]
        arraysizes[variable_base] = numelements
        for i in range(numelements):
            entrydef = '(rename {}_{}_ "{}({})")'.format(variable_base, i, orig_var, i)
            newline = line.replace(tocut, entrydef)
            yield newline
    else:
        memberid = line.find('(member ')
        if memberid != -1:
            closing = find_closing_bracket(line, memberid) + 1
            tocut = line[memberid:closing]
            tokens = tocut.split(' ')
            variable_base = tokens[1]
            index = int(tokens[2][:-1])
            entrydef = '{}_{}_'.format(variable_base, arraysizes[variable_base] - index - 1)
            newline = line.replace(tocut, entrydef)
            yield newline
        else:
            yield line


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

    lutlines = []

    with open(args.input, 'r') as infile:
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
                newval = convert_lut_init_to_hex(luttype, num)
                line = line.replace(line[initdef:initdefend + len(initdefdel)], '(string "{}")'.format(newval))
            lutlines.append(line)

    lines = []

    arraysizes = {}

    for line in lutlines:
        for newline in fix_array_line(line, arraysizes):
            lines.append(newline)

    with open(args.output, 'w') as outfile:
        outfile.writelines(lines)
