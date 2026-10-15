#!/usr/bin/env python3
#
# screentex.py -- tc.tex as the screen edition sees it, for pandoc.
#
# tc.tex chooses between the screen and print editions with
# \ifdefined\tcprint ... \else ... \fi. LaTeX evaluates that; pandoc's
# LaTeX reader does not, and takes the first branch, the print one, with
# warnings about missing files and macros defined twice. This writes a
# copy with each such block replaced by its \else part (or nothing), so
# that the HTML and text editions are built from the screen edition.
#
# Usage: tools/screentex.py tc.tex OUT

import sys

START = r'\ifdefined\tcprint'


def screen(src):
    out = []
    i = 0
    while True:
        j = src.find(START, i)
        if j < 0:
            out.append(src[i:])
            return ''.join(out)
        out.append(src[i:j])
        k = j + len(START)
        depth, els, end = 1, None, None
        p = k
        while p < len(src):
            if src.startswith(r'\ifdefined', p) or src.startswith(r'\ifnum', p):
                depth += 1
            elif src.startswith(r'\else', p) and depth == 1:
                els = p
            elif src.startswith(r'\fi', p) and not src[p + 3:p + 4].isalpha():
                depth -= 1
                if depth == 0:
                    end = p
                    break
            p += 1
        if end is None:
            sys.exit('screentex: unterminated ' + START)
        if els is not None:
            out.append(src[els + len(r'\else'):end])
        i = end + len(r'\fi')


if __name__ == '__main__':
    with open(sys.argv[1], encoding='utf-8') as f:
        text = screen(f.read())
    with open(sys.argv[2], 'w', encoding='utf-8') as f:
        f.write(text)
