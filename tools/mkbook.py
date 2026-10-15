#!/usr/bin/env python3
#
# mkbook.py -- assemble the chapter sources into one Markdown file that
# sw/apps/read can actually display.
#
# The old route was chapters/*.md -> pandoc -> *.tex -> pandoc -> tc.md.
# That is a round trip through a print-oriented AST, and everything the
# print path adds on the way through comes back out as Markdown the
# reader has to cope with: fenced divs, {#anchor} attributes, simple
# tables, and syntax highlighting turned into inline colour spans that
# destroy code entirely. The chapters are Markdown to begin with, so
# this copies them instead of translating them, and generates only the
# parts that genuinely have to be generated: the front pages and the
# table of contents.
#
# The rule this whole file follows: chapter body text is copied BYTE FOR
# BYTE. Nothing reflows it, nothing re-aligns tables, nothing re-indents
# lists. The one exception is ASCII transliteration (--ascii, on by
# default), which is a per-character substitution and is reported.
#
# What the output targets is Zeitlos:sw/apps/read/md.c. See md.h for the
# supported subset. The constraints that shaped the code below:
#
#   - Anchors resolve by slugifying heading TEXT at click time, with no
#     de-duplication (read.c goto_anchor). Two headings that slug the
#     same are indistinguishable and the first one always wins, so
#     collisions are reported rather than silently suffixed -- a
#     "#foo-1" would just fail to resolve.
#   - Table rows render VERBATIM in a fixed-width font (md.c MD_TABLE),
#     so the source's own column padding IS the layout.
#   - List nesting is `indent / 2` (md.c), so the contents list is
#     indented two spaces per level, not four. Four would also risk the
#     indented-code branch.
#   - z_font_5x8 covers 0x20-0x7f only (sw/common/zfont_data.c), so
#     anything else is transliterated.
#
# Usage:
#   tools/mkbook.py --tex tc.tex --chapters chapters -o dist/tc.md
#   tools/mkbook.py --check-only          lint the sources, write nothing

import argparse
import datetime
import os
import re
import sys

MD_LINE_MAX = 1024          # md.h
DEFAULT_COLS = 67           # code: what fits the 13.5 cm print edition
TABLE_COLS = 78             # tables: what fits the reader window


# ---------------------------------------------------------------------
# ports of md.c / read.c
#
# These are transcriptions, not reimplementations. If md.c changes,
# change these to match -- the whole value of this file is that its
# idea of a heading and the reader's idea of a heading are the same.
# ---------------------------------------------------------------------

def slugify(s):
    """read.c slugify(): lowercase, spaces to hyphens, drop the rest.

    Note what it does NOT do: collapse runs of hyphens, trim leading or
    trailing ones, or de-duplicate. "Binary & Other Number Systems"
    becomes "binary--other-number-systems", with two hyphens where the
    ampersand was dropped between two spaces.
    """
    out = []
    for c in s:
        if 'A' <= c <= 'Z':
            c = c.lower()
        if ('a' <= c <= 'z') or ('0' <= c <= '9') or c == '-':
            out.append(c)
        elif c == ' ':
            out.append('-')
    return ''.join(out)


def is_space(c):
    return c in (' ', '\t')


def is_word(c):
    return c.isascii() and (c.isalnum() or c == '_')


def inline_strip(s):
    """md.c inline_pass(), text output only (spans discarded).

    Needed because a heading's anchor is the slug of its RENDERED text,
    after inline syntax has been removed. `Ohm's Law` and Ohm's Law slug
    identically, and the tool has to know that.
    """
    out = []
    i, n = 0, len(s)

    while i < n:
        c = s[i]

        # `code`
        if c == '`':
            j = i + 1
            while j < n and s[j] != '`':
                j += 1
            if j < n:
                out.append(s[i + 1:j])
                i = j + 1
                continue
            out.append(c)
            i += 1
            continue

        # ![alt](src) is [alt](src) minus the bang
        if c == '!' and i + 1 < n and s[i + 1] == '[':
            i += 1
            continue

        # [text](target)
        if c == '[':
            close, depth = i + 1, 1
            while close < n and depth:
                if s[close] == '[':
                    depth += 1
                elif s[close] == ']':
                    depth -= 1
                if depth:
                    close += 1
            if close + 1 < n and s[close] == ']' and s[close + 1] == '(':
                tstart = close + 2
                tend, pd = tstart, 1
                while tend < n and pd:
                    if s[tend] == '(':
                        pd += 1
                    elif s[tend] == ')':
                        pd -= 1
                    if pd:
                        tend += 1
                if tend < n and s[tend] == ')':
                    # md.c copies the link text raw, without recursing.
                    out.append(s[i + 1:close])
                    i = tend + 1
                    continue
            out.append(c)
            i += 1
            continue

        # emphasis: markers dropped, text kept
        if c == '*' or c == '_':
            run2 = (i + 1 < n and s[i + 1] == c)
            after = (s[i + 2] if i + 2 < n else '') if run2 else \
                    (s[i + 1] if i + 1 < n else '')
            before = s[i - 1] if i > 0 else ' '

            # an underscore inside a word is literal: snake_case survives
            if c == '_' and is_word(before) and after and is_word(after):
                out.append(c)
                i += 1
                continue

            if after and not is_space(after):
                i += 2 if run2 else 1
                continue
            if not is_space(before):
                i += 2 if run2 else 1
                continue

            out.append(c)
            i += 1
            continue

        # bare HTML tag, only if it closes on this line
        if c == '<':
            j = i + 1
            if j < n and (s[j] == '/' or s[j].isascii() and s[j].isalpha()):
                while j < n and s[j] != '>':
                    j += 1
                if j < n and s[j] == '>':
                    i = j + 1
                    continue
            out.append(c)
            i += 1
            continue

        # backslash escape
        if c == '\\' and i + 1 < n:
            out.append(s[i + 1])
            i += 2
            continue

        out.append(c)
        i += 1

    return ''.join(out)


def all_of(s, c, minimum):
    """md.c all_of(): only `c` and spaces, at least `minimum` of them."""
    n = 0
    for ch in s:
        if ch == c:
            n += 1
        elif not is_space(ch):
            return False
    return n >= minimum


def looks_like_list(s):
    i = 0
    while i < len(s) and is_space(s[i]):
        i += 1
    rest = s[i:]
    if re.match(r'[-*+][ \t]', rest):
        return True
    return bool(re.match(r'\d+[.)][ \t]', rest))


# ---------------------------------------------------------------------
# block scanner
#
# A cut-down md_parse: enough to know, for any line, whether it is a
# heading and what block context it sits in. It tracks fences, front
# matter and indented code exactly as md.c does, so a '#' inside a code
# block is not mistaken for a heading -- the bug that would otherwise
# put shell comments in the table of contents.
# ---------------------------------------------------------------------

class Block:
    HEADING = 'heading'
    CODE = 'code'
    TABLE = 'table'
    FENCE = 'fence'
    FRONT = 'front'
    RULE = 'rule'
    QUOTE = 'quote'
    LIST = 'list'
    PARA = 'para'
    BLANK = 'blank'


def scan(lines):
    """Classify each line. Yields (index, kind, level, text).

    `text` is the rendered text for headings, and the raw line
    otherwise. `level` is the heading level or 0.
    """
    in_fence = False
    fence_char = ''
    fence_len = 0
    in_front = False
    seen_any = False
    in_list = False

    i = 0
    while i < len(lines):
        src = lines[i]
        nxt = lines[i + 1] if i + 1 < len(lines) else None

        fi = 0
        while fi < len(src) and is_space(src[fi]):
            fi += 1
        head = src[fi:]

        # fenced code first: inside a fence nothing else is markup
        if in_fence:
            if head[:1] == fence_char:
                m = re.match(re.escape(fence_char) + '+', head)
                if m and len(m.group(0)) >= fence_len:
                    in_fence = False
                    yield i, Block.FENCE, 0, src
                    i += 1
                    continue
            yield i, Block.CODE, 0, src
            i += 1
            continue

        if head[:1] in ('`', '~'):
            m = re.match(r'(`+|~+)', head)
            if m and len(m.group(0)) >= 3:
                in_fence = True
                fence_char = head[0]
                fence_len = len(m.group(0))
                seen_any = True
                yield i, Block.FENCE, 0, src
                i += 1
                continue

        # front matter, only at the very top of the file
        if in_front:
            if all_of(src, '-', 3):
                in_front = False
            yield i, Block.FRONT, 0, src
            i += 1
            continue
        if not seen_any and all_of(src, '-', 3):
            in_front = True
            yield i, Block.FRONT, 0, src
            i += 1
            continue

        if not head:
            yield i, Block.BLANK, 0, src
            i += 1
            continue

        seen_any = True

        # indented code, unless it is a nested list item
        if fi >= 4 and not (in_list and looks_like_list(src)):
            yield i, Block.CODE, 0, src
            i += 1
            continue

        # ATX heading
        if head.startswith('#'):
            m = re.match(r'(#{1,6})([ \t]|$)', head)
            if m:
                n = len(m.group(1))
                t = head[n:].lstrip(' \t')
                t = t.rstrip('# \t')
                in_list = False
                yield i, Block.HEADING, n, inline_strip(t)
                i += 1
                continue

        if all_of(src, '-', 3) or all_of(src, '*', 3) or all_of(src, '_', 3):
            in_list = False
            yield i, Block.RULE, 0, src
            i += 1
            continue

        if head.startswith('>'):
            in_list = False
            yield i, Block.QUOTE, 0, src
            i += 1
            continue

        if head.startswith('|'):
            in_list = False
            yield i, Block.TABLE, 0, src
            i += 1
            continue

        if re.match(r'[-*+][ \t]', head) or re.match(r'\d+[.)][ \t]', head):
            in_list = True
            yield i, Block.LIST, 0, src
            i += 1
            continue

        if fi == 0:
            in_list = False

        # setext heading: this line plus an underline below it
        if nxt is not None:
            ni = 0
            while ni < len(nxt) and is_space(nxt[ni]):
                ni += 1
            if nxt[ni:] and (all_of(nxt, '=', 1) or all_of(nxt, '-', 1)):
                lvl = 1 if nxt[ni] == '=' else 2
                yield i, Block.HEADING, lvl, inline_strip(src[fi:])
                i += 2          # the underline is consumed
                continue

        yield i, Block.PARA, 0, src
        i += 1


# ---------------------------------------------------------------------
# ASCII transliteration
#
# z_font_5x8 is { 5, 8, 0x20, 0x7f, ... } -- printable ASCII and
# nothing else. A UTF-8 character is several bytes and each one lands
# outside the glyph range, so a curly apostrophe does not render as a
# straight one, it renders as two or three blanks in the middle of a
# word. Substituting here keeps the chapter sources free to use proper
# typography.
# ---------------------------------------------------------------------

TRANSLIT = {
    '\u2018': "'", '\u2019': "'", '\u201a': "'", '\u201b': "'",
    '\u201c': '"', '\u201d': '"', '\u201e': '"',
    '\u2013': '-', '\u2014': '--', '\u2015': '--', '\u2212': '-',
    '\u2026': '...', '\u2022': '*', '\u00b7': '*',
    '\u2192': '->', '\u2190': '<-', '\u2194': '<->',
    '\u21d2': '=>', '\u21d0': '<=',
    '\u00d7': 'x', '\u00f7': '/', '\u00b1': '+/-',
    '\u2260': '!=', '\u2264': '<=', '\u2265': '>=', '\u2248': '~=',
    '\u00a9': '(c)', '\u00ae': '(R)', '\u2122': '(TM)',
    '\u00b0': ' deg', '\u00b5': 'u', '\u03bc': 'u',
    '\u03a9': 'Ohm', '\u2126': 'Ohm',
    '\u00bd': '1/2', '\u00bc': '1/4', '\u00be': '3/4',
    '\u00a0': ' ', '\u2009': ' ', '\u202f': ' ', '\u200b': '',
    # German names (Zwoelf, Koelsch): the usual two-letter spellings,
    # which read correctly where the umlaut cannot be drawn.
    '\u00e4': 'ae', '\u00f6': 'oe', '\u00fc': 'ue', '\u00df': 'ss',
    '\u00c4': 'Ae', '\u00d6': 'Oe', '\u00dc': 'Ue',
    '\ufeff': '',
}


def to_ascii(text, report):
    """Substitute non-ASCII characters, recording anything unmapped."""
    out = []
    for ch in text:
        if ord(ch) < 128:
            out.append(ch)
        elif ch in TRANSLIT:
            out.append(TRANSLIT[ch])
        else:
            report.setdefault(ch, 0)
            report[ch] += 1
            out.append('?')
    return ''.join(out)


# ---------------------------------------------------------------------
# tc.tex
# ---------------------------------------------------------------------

def chapter_order(tex_path):
    """Chapter order from the \\input{} lines, which is where it lives.

    Reading it from tc.tex rather than globbing means the PDF and the
    Markdown cannot drift into different orders, and adding a chapter
    stays a one-line edit in one file.
    """
    with open(tex_path, encoding='utf-8') as f:
        tex = f.read()
    names = []
    for m in re.finditer(r'^[ \t]*\\input\{([^}]+)\}', tex, re.M):
        name = m.group(1).strip()
        if name.endswith('.tex'):
            name = name[:-4]
        names.append(name)
    return names


# LaTeX we understand in the title page. Anything else is stripped to
# its argument and reported, so an unrecognised macro degrades to its
# text instead of appearing raw in the output.
TEX_DROP = re.compile(
    r'\\(?:vspace\*?|hspace\*?)\{[^}]*\}'
    r'|\\(?:vfill|hfill|tcversobreak|tcimprint|centering|newpage|clearpage|par|noindent|bigskip'
    r'|medskip|smallskip)\b'
    r'|\\(?:Huge|huge|LARGE|Large|large|normalsize|small|footnotesize'
    r'|scriptsize|tiny|bfseries|itshape|rmfamily|sffamily|ttfamily)\b'
    r'|\\color\{[^}]*\}'
)

TEX_CHARS = {
    r'\&': '&', r'\%': '%', r'\_': '_', r'\#': '#', r'\$': '$',
    r'\{': '{', r'\}': '}', r'\ ': ' ', r'\\': '\n',
    r'\textbackslash': '\\', r'\textasciitilde': '~',
    r'\ldots': '...', r'\dots': '...',
}


def tex_inline(s, today, unknown):
    """Convert one run of title-page LaTeX to Markdown."""
    s = s.replace('\\today', today)

    # Size and weight switches go FIRST. They take no argument, so
    # "{\Large\textit{X}}" would otherwise have its \textit unwrapped
    # into "{\LargeX}" and the switch would stop being recognisable.
    s = TEX_DROP.sub('', s)

    # argument-taking macros we keep the content of
    s = re.sub(r'\\texttt\{([^{}]*)\}', r'`\1`', s)
    s = re.sub(r'\\(?:textit|emph|textsl)\{([^{}]*)\}', r'\1', s)
    s = re.sub(r'\\textbf\{([^{}]*)\}', r'\1', s)
    s = re.sub(r'\\url\{([^{}]*)\}', r'<\1>', s)
    s = re.sub(r'\\href\{([^{}]*)\}\{([^{}]*)\}', r'[\2](\1)', s)

    s = TEX_DROP.sub('', s)

    for k, v in TEX_CHARS.items():
        s = s.replace(k, v)

    for m in re.finditer(r'\\([a-zA-Z]+)', s):
        unknown.add(m.group(1))
    s = re.sub(r'\\[a-zA-Z]+\*?', '', s)

    s = s.replace('{', '').replace('}', '')
    s = re.sub(r'[ \t]+', ' ', s)
    return s.strip()


def front_pages(tex_path, today, warn):
    """Build the front pages from the titlepage environment.

    Deliberately narrow: it reads one environment out of tc.tex and
    converts the handful of macros that appear in it. A title page that
    outgrows that should become a hand-written front.md instead
    (--front), which this will use in preference if it exists.
    """
    with open(tex_path, encoding='utf-8') as f:
        tex = f.read()

    m = re.search(r'\\begin\{titlepage\}(.*?)\\end\{titlepage\}', tex, re.S)
    if not m:
        warn('no \\begin{titlepage} in %s; front pages omitted' % tex_path)
        return []

    unknown = set()
    body = m.group(1)

    # Each brace group at the top level of a title page is one visual
    # line; anything outside them is loose text. Splitting on blank
    # lines and on \\ keeps that structure without needing a real
    # LaTeX parser.
    chunks = []
    for raw in re.split(r'\n\s*\n', body):
        txt = tex_inline(raw, today, unknown)
        for part in txt.split('\n'):
            part = part.strip()
            if part:
                chunks.append(part)

    if unknown:
        warn('title page: unhandled LaTeX macros dropped: %s'
             % ', '.join('\\' + u for u in sorted(unknown)))

    if not chunks:
        return []

    # The first chunk is the title; the rest are paragraphs. The title
    # is NOT a heading -- it would land in the contents list under
    # itself. A rule separates it from the contents instead.
    out = ['# ' + chunks[0], '']
    for c in chunks[1:]:
        out.append(c)
        out.append('')
    return out


# ---------------------------------------------------------------------
# contents
# ---------------------------------------------------------------------

def build_toc(headings, depth, title):
    """A nested list of [text](#slug) links.

    Two spaces per level because md.c computes list depth as indent/2,
    and because four spaces is close enough to the indented-code rule
    to be worth avoiding.
    """
    out = ['## ' + title, '']
    base = min(h[1] for h in headings) if headings else 1

    for text, level, slug, _ in headings:
        if level - base >= depth:
            continue
        indent = '  ' * (level - base)
        # Brackets in the label would close the link early.
        label = text.replace('[', '(').replace(']', ')')
        out.append('%s- [%s](#%s)' % (indent, label, slug))

    out.append('')
    return out


# ---------------------------------------------------------------------
# lint
# ---------------------------------------------------------------------

def lint(path, lines, cols, problems):
    """Checks against what md.c will actually do with these lines."""

    def bad(n, msg):
        problems.append('%s:%d: %s' % (path, n + 1, msg))

    for i, kind, level, text in scan(lines):
        src = lines[i]

        if len(src) > MD_LINE_MAX - 1:
            bad(i, 'line is %d chars, truncated at MD_LINE_MAX (%d)'
                % (len(src), MD_LINE_MAX))

        # Code and tables are never wrapped by the reader, so an
        # over-wide one is cut off at the window edge rather than
        # flowing. Prose is fine at any width. Code is held to the
        # narrower budget because it does not wrap in the 13.5 cm print
        # edition either; tables do, so they only need to fit the reader.
        limit = cols if kind == Block.CODE else TABLE_COLS
        if kind in (Block.CODE, Block.TABLE) and len(src.rstrip()) > limit:
            bad(i, '%s line is %d cols, over the %d-col budget'
                % (kind, len(src.rstrip()), limit))

        if kind in (Block.CODE, Block.FENCE, Block.FRONT):
            continue

        if src.lstrip().startswith(':::'):
            bad(i, 'fenced div -- md.c has no rule for it, renders literally')
        if re.search(r'\{#[-\w]+\}', src):
            bad(i, 'attribute block -- renders literally')
        if re.search(r'\[[^\]]*\]\[[^\]]*\]', src):
            bad(i, 'reference-style link -- unsupported, renders literally')
        if re.match(r'^\[[^\]]+\]:\s', src):
            bad(i, 'link definition -- unsupported, renders literally')
        if re.search(r'\[\^[^\]]+\]', src):
            bad(i, 'footnote -- unsupported, renders literally')
        if '![' in src:
            bad(i, 'image -- only its alt text will appear')

        if '\t' in src:
            bad(i, 'tab -- indent width becomes ambiguous, use spaces')

    # a pipe table's rows should agree on column count, because they
    # are drawn verbatim and a short row simply looks broken
    tbl_cols = 0
    for i, kind, level, text in scan(lines):
        if kind == Block.TABLE:
            n = lines[i].strip().strip('|').count('|') + 1
            if not tbl_cols:
                tbl_cols = n
            elif n != tbl_cols:
                bad(i, 'table row has %d columns, header has %d'
                    % (n, tbl_cols))
        else:
            tbl_cols = 0


# ---------------------------------------------------------------------
# main
# ---------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description='Assemble chapters into one reader-compatible Markdown '
                    'file.')
    ap.add_argument('--tex', default='tc.tex',
                    help='LaTeX file the chapter order comes from')
    ap.add_argument('--chapters', default='chapters',
                    help='directory holding the chapter sources')
    ap.add_argument('--front', default='front.md',
                    help='optional hand-written front pages, used instead '
                         'of the titlepage in --tex if present')
    ap.add_argument('-o', '--output', default='dist/tc.md')
    ap.add_argument('--toc-depth', type=int, default=3,
                    help='heading levels in the contents (default 3)')
    ap.add_argument('--toc-title', default='Contents')
    ap.add_argument('--no-toc', action='store_true')
    ap.add_argument('--front-matter', action='store_true',
                    help='emit a YAML block. OFF by default: read.c cannot '
                         'scroll back up into the MD_SKIP lines it becomes, '
                         'so line 0 is unreachable once you have scrolled '
                         'down. render_test MODE=scroll reports it.')
    ap.add_argument('--cols', type=int, default=DEFAULT_COLS,
                    help='width budget for code lines')
    ap.add_argument('--no-ascii', action='store_true',
                    help='keep non-ASCII characters (they will not render)')
    ap.add_argument('--check-only', action='store_true',
                    help='lint and report, write nothing')
    ap.add_argument('--strict', action='store_true',
                    help='exit non-zero if anything is reported')
    ap.add_argument('--date', default=None,
                    help='date for \\today (default: today)')
    args = ap.parse_args()

    warnings = []
    problems = []

    def warn(msg):
        warnings.append(msg)

    today = args.date or datetime.date.today().strftime('%B %d, %Y')

    names = chapter_order(args.tex)
    if not names:
        sys.stderr.write('mkbook: no \\input{} lines in %s\n' % args.tex)
        return 2

    # -- read and lint the chapters --

    chapters = []
    for name in names:
        p = os.path.join(args.chapters, name + '.md')
        if not os.path.exists(p):
            sys.stderr.write('mkbook: %s: no such file\n' % p)
            return 2
        with open(p, encoding='utf-8') as f:
            text = f.read()
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        lines = text.split('\n')
        while lines and not lines[-1].strip():
            lines.pop()
        lint(p, lines, args.cols, problems)
        chapters.append((p, lines))

    # -- collect headings, in output order --

    headings = []
    for p, lines in chapters:
        for i, kind, level, text in scan(lines):
            if kind == Block.HEADING:
                headings.append((text, level, slugify(text), '%s:%d'
                                 % (p, i + 1)))

    # Colliding slugs are a real defect, not a cosmetic one: read.c
    # walks the document and stops at the FIRST heading whose slug
    # matches, so every link to the later one goes to the earlier one.
    # There is no suffix that would help, because the reader would not
    # resolve it. The heading has to be renamed.
    seen = {}
    for text, level, slug, where in headings:
        if slug in seen:
            problems.append(
                '%s: heading "%s" slugs to #%s, same as "%s" at %s -- '
                'links reach only the first' %
                (where, text, slug, seen[slug][0], seen[slug][1]))
        else:
            seen[slug] = (text, where)

    # A cross-reference to a heading that does not exist gets a "Not
    # found" dialog on the device and nothing else, so it is worth
    # catching here rather than on hardware. Only in-document anchors
    # are checkable; a path or an http target is read.c's business.
    for p, lines in chapters:
        for i, kind, level, text in scan(lines):
            if kind in (Block.CODE, Block.FENCE, Block.FRONT):
                continue
            for m in re.finditer(r'\]\(#([^)\s]*)\)', lines[i]):
                if m.group(1) not in seen:
                    problems.append('%s:%d: link to #%s matches no heading'
                                    % (p, i + 1, m.group(1)))

    # -- assemble --

    out = []

    if args.front_matter:
        # md.c treats a --- block at the very top as front matter and
        # emits MD_SKIP for every line of it, so this is invisible in
        # the reader while remaining available to anything else.
        #
        # It is also, today, a way to break scrolling: read.c's
        # positions are block-aligned and it will not step back into a
        # run of MD_SKIP, so scrolling down from the top and back up
        # lands below line 0 and never returns. The existing
        # pandoc-generated dist/tc.md has the same defect -- eight
        # failed round trips under `make render MODE=scroll`. Hence
        # opt-in.
        out += [
            '---',
            'title: Timeless Computing',
            'generator: tools/mkbook.py',
            'date: ' + today,
            '---',
            '',
        ]

    if os.path.exists(args.front):
        with open(args.front, encoding='utf-8') as f:
            out += f.read().replace('\r\n', '\n').rstrip('\n').split('\n')
        out.append('')
    else:
        out += front_pages(args.tex, today, warn)

    if not args.no_toc and headings:
        out += build_toc(headings, args.toc_depth, args.toc_title)

    for p, lines in chapters:
        # A chapter starts with its own '# Heading'. The blank line
        # before it is what keeps md_continues() from joining it to
        # whatever the previous chapter ended with.
        if out and out[-1].strip():
            out.append('')
        out += lines

    text = '\n'.join(out).rstrip('\n') + '\n'

    if not args.no_ascii:
        report = {}
        text = to_ascii(text, report)
        if report:
            warn('no ASCII substitution for: %s (replaced with "?"); '
                 'add them to TRANSLIT' %
                 ', '.join('%r (x%d)' % (c, n) for c, n in
                           sorted(report.items())))

    # -- report --

    for w in warnings:
        sys.stderr.write('mkbook: warning: %s\n' % w)
    for p in problems:
        sys.stderr.write('mkbook: %s\n' % p)

    if args.check_only:
        sys.stderr.write('mkbook: %d chapters, %d headings, %d problems\n'
                         % (len(chapters), len(headings), len(problems)))
        return 1 if (problems and args.strict) else 0

    d = os.path.dirname(args.output)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(text)

    sys.stderr.write('mkbook: wrote %s -- %d lines, %d chapters, '
                     '%d headings, %d problems\n'
                     % (args.output, text.count('\n'), len(chapters),
                        len(headings), len(problems)))

    return 1 if ((problems or warnings) and args.strict) else 0


if __name__ == '__main__':
    sys.exit(main())
