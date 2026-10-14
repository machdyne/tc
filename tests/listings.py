#!/usr/bin/env python3
#
# listings.py -- every code listing in the book is a tested file.
#
# A fenced block whose info string names one of the tested languages
# (basic, scheme, c, verilog, asm) must appear, line for line, inside some
# file of that language under tests/. That is what keeps the book and
# its tests from drifting apart between rebuilds: a listing edited in a
# chapter and not in its test fails here, before anything is run.
#
# Blocks with any other info string (text, or none) are illustrations,
# terminal sessions or diagrams, and are not checked.
#
# Usage: tests/listings.py CHAPTER_DIR TEST_DIR

import os
import re
import sys

LANGS = {
    'basic': ('.bas',),
    'scheme': ('.scm',),
    'c': ('.c', '.h'),
    'verilog': ('.v',),
    'asm': ('.S',),
}


def blocks(path):
    """Yield (line_number, info, lines) for each fenced block."""
    with open(path, encoding='utf-8') as f:
        lines = f.read().split('\n')
    i = 0
    while i < len(lines):
        m = re.match(r'^(```+|~~~+)\s*([\w+-]*)', lines[i])
        if not m:
            i += 1
            continue
        fence, info, start = m.group(1), m.group(2).lower(), i
        body = []
        i += 1
        while i < len(lines) and not lines[i].startswith(fence):
            body.append(lines[i])
            i += 1
        i += 1
        yield start + 1, info, body


def norm(lines):
    return [l.rstrip() for l in lines]


def contains(hay, needle):
    n = len(needle)
    return any(hay[k:k + n] == needle for k in range(len(hay) - n + 1))


def main():
    chapters, tests = sys.argv[1], sys.argv[2]

    corpus = {lang: [] for lang in LANGS}
    for lang, exts in LANGS.items():
        d = os.path.join(tests, lang)
        if not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            if name.endswith(exts):
                with open(os.path.join(d, name), encoding='utf-8') as f:
                    corpus[lang].append(norm(f.read().split('\n')))

    checked = bad = 0
    for name in sorted(os.listdir(chapters)):
        if not name.endswith('.md'):
            continue
        path = os.path.join(chapters, name)
        for line, info, body in blocks(path):
            if info not in LANGS:
                continue
            checked += 1
            want = norm(body)
            if not any(contains(f, want) for f in corpus[info]):
                bad += 1
                print('%s:%d: %s listing not found in tests/%s/'
                      % (path, line, info, info))

    print('listings: %d checked, %d not found' % (checked, bad))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
