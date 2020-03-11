#!/usr/bin/env python3

import argparse
from pathlib import Path
import re


def convert_lut_init_to_hex(val: str) -> str:
    """Converts EDIF decimal and hexadecimal notation to hexadecimal for SpDE.

    Args:
        val (str): value in decimal or hexadecimal notation (i.e. ``16'hABCD``)

    Returns:
        str: string containing only hexadecimal number, without ``0x`` prefix
            (i.e. "ABCD")
    """
    if "'" not in val:
        return str(format(int(val), 'x')).upper()
    else:
        return str(val.split("'h")[1]).upper()


def find_closing_bracket(line: str, openbracketid: int) -> int:
    """Returns the index of the closing bracket for a given opening bracket.

    Looks for the closing bracket in string for an opening bracket that is
    pointed by the ``openbracketid``.

    Args:
        line (str) : a single line from the EDIF file
        openbracketid (int): the index of the opening bracket for which the
            closing bracket should be found

    Returns:
        int: index for the closing bracket or -1 if not found
    """
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


def fix_array_line(line: str, arraysizes: dict) -> str:
    """Converts array notation from Yosys EDIF to notation acceptable by SpDE.

    Arrays in EDIF file from Yosys are declared in a form::

        (array (rename EDIF_ARR_NAME "verilog_name(maxid:minid)")") WIDTH)

    and the members of array are accessed with::

        (member EDIF_ARR_NAME MEMBER_ID)

    This format is unacceptable for SpDE - it accepts only wires, so this
    function converts every declaration and member access with wire-based
    implementation.

    Args:
        line (str) : a single line from the EDIF file
        arraysizes (dict): a dict mapping array name to its size. It is a
            helper argument that stores the sizes from arrays from declaration
            so they can be used in index recalculation in converting member
            accesses

    Yields:
        str: Function yields lines that are produced during conversion of
            declarations and accesses
    """
    arrayregex = r'\(array\s*\(rename\s*(?P<name>[A-Za-z_$][A-Za-z0-9_$]*)\s*\"(?P<verilogname>[A-Za-z_$][A-Za-z0-9_$]*)\s*\((?P<left>[0-9]+)\s*:\s*(?P<right>[0-9]+)\s*\)\"\)\s*(?P<edifsize>[0-9]+)\s*\)'  # noqa: E501
    arrayid = line.find('(array ')
    if arrayid != -1:
        # extract whole array declaration
        closing = find_closing_bracket(line, arrayid) + 1
        tocut = line[arrayid:closing]
        arraydef = re.match(arrayregex, tocut)
        if not arraydef:
            raise Exception(
                    'Array declaration format not supported:  '.format(tocut))
        left = int(arraydef.group('left'))
        right = int(arraydef.group('right'))
        numelements = (left if left > right else right) + 1
        variable_base = arraydef.group('name')
        orig_var = arraydef.group('verilogname')
        if variable_base in arraysizes:
            raise Exception(
                    'There is already an array with name "{}" declared'.format(
                        variable_base))
        arraysizes[variable_base] = numelements
        if left == right == 0:
            entrydef = '(rename {} "{}({})")'.format(
                    variable_base,
                    orig_var,
                    0)
            newline = line.replace(tocut, entrydef)
            yield newline
        else:
            for i in range(numelements):
                entrydef = '(rename {}_{}_ "{}({})")'.format(
                        variable_base,
                        i,
                        orig_var,
                        i)
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
            entrydef = '{}_{}_'.format(
                    variable_base,
                    arraysizes[variable_base] - index - 1)
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
        # since definition of the LUT cells are multi-line, this needs to
        # be handled this way
        for line in infile:
            if '(instance ' in line:  # new instance in EDIF
                luttype = -1
            elif '(cellRef LUT' in line:
                s = '(cellRef LUT'  # the new instance is LUT
                numloc = line.find(s) + len(s)
                luttype = int(line[numloc:].split(' ')[0])
            elif '(property INIT' in line and luttype > 0:
                intpre = '(integer '  # look for integer field for INIT
                initdef = line.find(intpre)
                if initdef == -1:  # otherwise look for string field
                    intpre = '(string "'
                initdef = line.find(intpre)
                # remove the ending characters for field
                initdefdel = '")' if intpre == '(string "' else ')'
                initdefend = line.find(initdefdel, initdef)
                # extract the number in decimal or hexadecimal notation
                num = line[initdef + len(intpre):initdefend]
                # compute pure hexadecimal notation
                newval = convert_lut_init_to_hex(num)
                # add updated LUT INIT value
                line = line.replace(
                        line[initdef:initdefend + len(initdefdel)],
                        '(string "{}")'.format(newval))
            lutlines.append(line)

    lines = []

    arraysizes = {}

    for line in lutlines:
        for newline in fix_array_line(line, arraysizes):
            lines.append(newline)

    with open(args.output, 'w') as outfile:
        outfile.writelines(lines)
