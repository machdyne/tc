#!/usr/bin/env python3
#
# mkcover.py -- build the cover files from cover/cover.svg.
#
# The artwork is drawn once, at A2, in cover/cover.svg (Inkscape; the
# lettering is set in Lato, which must be installed for rendering).
# This tool places it on pages of other sizes and renders them to PDF
# with rsvg-convert:
#
#   screen   the front cover alone, at the height of a Letter page, used
#            as the first page of dist/tc.pdf
#
#   front    the front cover at the print trim size plus bleed, for a
#            web shop or a paperback; see --trim and --bleed
#
#   wrap     the whole cover of the printed book, back + spine + front,
#            as one sheet. Its dimensions depend on the binding, the
#            page count and the paper, and come from the printer's
#            cover calculator: --width and --height (including the
#            edge), --spine, --wrap, the edge outside the visible board
#            on the top, bottom and outer sides, and --hinge, the fold
#            beside the spine. In BoD's terms for a hardcover: total
#            width and height including edge, book spine width,
#            top/bottom/outside impact edge, and fold width within U1/U4
#
# Usage:
#   tools/mkcover.py screen -o build/cover-front.pdf
#   tools/mkcover.py front  -o dist/tc-cover-front.pdf
#   tools/mkcover.py wrap   -o dist/tc-cover-wrap.pdf \
#       --width 330 --height 251 --spine 18 --wrap 18 [--barcode FILE]
#
# The author's name is set here (AUTHOR); the edition is read from the
# title page in tc.tex, so that it is changed in one place.
#
# All dimensions are in millimetres.

import argparse
import base64
import textwrap
import io
import os
import re
import subprocess
import sys
import shutil
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'cover', 'cover.svg')

PAGE_W, PAGE_H = 420.0, 594.0       # the artwork's page, in its own units

# Colour of the artwork's background at its edges, used to extend it
# across the back and the spine.
BACKGROUND = '#dcdfe1'
INK = '#000000'

TITLE = 'Timeless Computing'
AUTHOR = 'Clio Grai'
TEX = os.path.join(HERE, '..', 'tc.tex')


def edition():
    """The edition, as the title page in tc.tex states it, so that it
    is set in one place: '2026 Edition'."""
    with open(TEX, encoding='utf-8') as f:
        m = re.search(r'(\d{4} Edition)', f.read())
    return m.group(1) if m else ''


def byline():
    """Author and edition, below the ground line of the artwork, in
    the artwork's own units."""
    return ('<text x="%g" y="545" font-family="Lato" font-weight="700" '
            'font-size="16" fill="%s" text-anchor="middle">%s</text>'
            '<text x="%g" y="568" font-family="Lato" font-size="9.5" '
            'fill="%s" text-anchor="middle">%s</text>'
            % (PAGE_W / 2, INK, AUTHOR, PAGE_W / 2, INK, edition()))

# The back-cover text, kept in one file so that the cover, the README
# and the publisher's listing say the same thing. Paragraphs are
# separated by blank lines.
BLURB = os.path.join(HERE, '..', 'cover', 'blurb.txt')


def text_width(font, text, size):
    """The width of text set in font at size, in the units of size."""
    return font.getlength(text) * size / 1000.0


def fill(para, size, width):
    """Break a paragraph into lines no wider than width, measuring the
    words in Lato; without the font, estimate half the size a letter."""
    try:
        from PIL import ImageFont
        path = subprocess.run(['fc-match', '-f', '%{file}', 'Lato:regular'],
                              capture_output=True, text=True).stdout
        font = ImageFont.truetype(path, 1000)
        measure = lambda t: text_width(font, t, size)
    except Exception:
        return textwrap.wrap(para, int(width / (0.5 * size)))
    lines, cur = [], ''
    for word in para.split():
        trial = word if not cur else cur + ' ' + word
        if cur and measure(trial) > width:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def blurb():
    with open(BLURB, encoding='utf-8') as f:
        return [' '.join(p.split()) for p in f.read().split('\n\n')
                if p.strip()]


IMAGE_RE = re.compile(r'<image\b[^>]*?/>', re.S)


def attr(tag, name):
    m = re.search(r'\s%s="([^"]*)"' % re.escape(name), tag)
    return m.group(1) if m else None


def artwork(extend=None, jpeg=False):
    """The artwork's content: everything inside the root <svg> element
    except Inkscape's editor state, which is meaningless when nested.

    extend: (left, right, top, bottom), page units by which to widen
    the background picture, by stretching its edge pixels outward. The picture's
    shading then continues smoothly beyond the page, onto the spine and
    the back, with no seam where it ends.

    jpeg: re-encode the picture as JPEG, for the screen edition, where
    a smaller file matters more than the last detail."""
    with open(SRC, encoding='utf-8') as f:
        s = f.read()
    body = s[s.index('>', s.index('<svg')) + 1:s.rindex('</svg>')]
    body = re.sub(r'<sodipodi:namedview.*?(/>|</sodipodi:namedview>)', '',
                  body, flags=re.S)
    body = re.sub(r'<metadata.*?</metadata>', '', body, flags=re.S)
    if not (extend or jpeg):
        return body

    from PIL import Image

    tag = IMAGE_RE.search(body).group(0)
    href = attr(tag, 'xlink:href') or attr(tag, 'href')
    data = base64.b64decode(re.sub(r'\s', '', href.split(',', 1)[1]))
    im = Image.open(io.BytesIO(data)).convert('RGB')
    x, y = float(attr(tag, 'x')), float(attr(tag, 'y'))
    w, h = float(attr(tag, 'width')), float(attr(tag, 'height'))

    if extend:
        # The outermost pixels of the picture are not reliable (the
        # corner one is visibly off), so the edges are taken from just
        # inside them.
        pw, ph = im.size
        c = 2
        im = im.crop((c, c, pw - c, ph - c))
        x, y = x + c * w / pw, y + c * h / ph
        w, h = w * (pw - 2 * c) / pw, h * (ph - 2 * c) / ph
        pw, ph = im.size
        l, r, t, b = [max(1, int(round(e * k)))
                      for e, k in zip(extend, (pw / w, pw / w, ph / h, ph / h))]
        big = Image.new('RGB', (l + pw + r, t + ph + b))
        big.paste(im, (l, t))
        # edges: stretch the outermost column or row of pixels
        big.paste(im.crop((0, 0, 1, ph)).resize((l, ph)), (0, t))
        big.paste(im.crop((pw - 1, 0, pw, ph)).resize((r, ph)), (l + pw, t))
        bw = big.size[0]
        big.paste(big.crop((0, t, bw, t + 1)).resize((bw, t)), (0, 0))
        big.paste(big.crop((0, t + ph - 1, bw, t + ph)).resize((bw, b)),
                  (0, t + ph))
        im = big
        x, y = x - l * w / pw, y - t * h / ph
        w, h = w * im.size[0] / pw, h * im.size[1] / ph

    buf = io.BytesIO()
    if jpeg:
        if im.size[0] > 1200:
            im = im.resize((1200, round(im.size[1] * 1200 / im.size[0])),
                           Image.LANCZOS)
        im.save(buf, 'JPEG', quality=85)
        mime = 'image/jpeg'
    else:
        im.save(buf, 'PNG', optimize=True)
        mime = 'image/png'
    href = 'data:%s;base64,%s' % (mime, base64.b64encode(buf.getvalue())
                                  .decode('ascii'))
    new = ('<image x="%g" y="%g" width="%g" height="%g" '
           'preserveAspectRatio="none" xlink:href="%s"/>'
           % (x, y, w, h, href))
    return body.replace(tag, new)


def nested(x, y, w, h, content, overflow='hidden'):
    """The artwork scaled so that its whole page fits the box x, y, w,
    h, centred. Where the box is taller or wider than the page, the
    artwork's own background fills the difference if overflow is
    visible and the picture has been extended."""
    return ('<svg x="%g" y="%g" width="%g" height="%g" viewBox="0 0 %g %g" '
            'preserveAspectRatio="xMidYMid meet" overflow="%s">%s</svg>'
            % (x, y, w, h, PAGE_W, PAGE_H, overflow, content))


def document(w, h, content):
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<svg xmlns="http://www.w3.org/2000/svg" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
            'xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/'
            'sodipodi-0.dtd" '
            'width="%gmm" height="%gmm" viewBox="0 0 %g %g">\n'
            '<rect x="0" y="0" width="%g" height="%g" fill="%s"/>\n'
            '%s\n</svg>\n' % (w, h, w, h, w, h, BACKGROUND, content))



def need(tool, package):
    """Stop with a clear message if an external program is missing."""
    if not shutil.which(tool):
        sys.exit('mkcover: %s not found; install %s' % (tool, package))

def render(svg, out, zoom=None):
    d = os.path.dirname(out)
    if d:
        os.makedirs(d, exist_ok=True)
    with tempfile.NamedTemporaryFile('w', suffix='.svg', delete=False,
                                     encoding='utf-8') as f:
        f.write(svg)
        tmp = f.name
    try:
        need('rsvg-convert', 'librsvg (librsvg2-bin on Debian and Ubuntu)')
        cmd = ['rsvg-convert', '-f', 'pdf', '-o', out]
        if zoom:
            cmd += ['-z', '%g' % zoom]
        subprocess.run(cmd + [tmp], check=True)
    finally:
        os.unlink(tmp)


def screen(args):
    # The artwork's own page, at the height of a Letter page.
    render(document(PAGE_W, PAGE_H,
                    nested(0, 0, PAGE_W, PAGE_H,
                           artwork(jpeg=True) + byline())),
           args.output, zoom=279.4 / PAGE_H)


def front(args):
    tw, th = args.trim
    b = args.bleed
    render(document(tw + 2 * b, th + 2 * b,
                    nested(b, b, tw, th,
                           artwork(extend=(60, 60, 60, 60)) + byline(),
                           overflow='visible')),
           args.output)


# Lato's capital height, as a fraction of its size (1433 / 2000 units).
LATO_CAP = 0.7165


def wrap(args):
    W, H, S, M = args.width, args.height, args.spine, args.wrap
    G = args.hinge                        # fold beside the spine
    panel = (W - S) / 2.0                 # back or front, wrap included
    sx = panel                            # left edge of the spine
    fx = panel + S                        # left edge of the front panel

    # The visible front board: the panel less the wrap on its outer
    # edge, top and bottom, and less the hinge where the cover folds
    # beside the spine. The artwork is fitted to it, so that the
    # lettering stays clear of both folds, and its background, extended,
    # runs on across the wrap, the hinge, the spine and the back.
    vx, vy = fx + G, M
    vw, vh = panel - M - G, H - 2 * M

    # How far, in the artwork's own units, its background must reach
    # beyond its page to cover the whole sheet, plus a little to spare.
    k = min(vw / PAGE_W, vh / PAGE_H)          # mm per unit
    ox = vx + (vw - PAGE_W * k) / 2            # page origin on the sheet
    oy = vy + (vh - PAGE_H * k) / 2
    extend = (ox / k + 20, (W - ox) / k - PAGE_W + 20,
              oy / k + 20, (H - oy) / k - PAGE_H + 20)

    parts = []
    parts.append(nested(vx, vy, vw, vh, artwork(extend=extend) + byline(),
                        overflow='visible'))

    # Spine: title and author, reading from top to bottom, as is usual
    # for English-language books.
    # The capitals are centred across the spine. The baseline is placed
    # by hand, half the cap height off centre, because SVG renderers do
    # not all honour dominant-baseline on rotated text.
    size = min(S * 0.45, 9.0)
    for text, y, anchor, weight, scale in (
            (TITLE, M + 15, 'start', 900, 1.0),
            (AUTHOR, H - M - 15, 'end', 700, 0.75)):
        base = sx + S / 2.0 - LATO_CAP * size * scale / 2.0
        parts.append('<text transform="translate(%g,%g) rotate(90)" '
                     'font-family="Lato" font-weight="%d" font-size="%g" '
                     'fill="%s" text-anchor="%s">%s</text>'
                     % (base, y, weight, size * scale, INK, anchor, text))

    # Back: the description, set on the visible back board. Lines are
    # broken by the measured width of the words in Lato.
    fs, lead = 3.9, 5.6
    bx = M + 12
    by = M + 30
    width = panel - M - G - 24
    lines, y = [], by
    for para in blurb():
        for line in fill(para, fs, width):
            lines.append('<tspan x="%g" y="%g">%s</tspan>'
                         % (bx, y, line.replace('&', '&amp;')))
            y += lead
        y += lead * 0.6
    parts.append('<text font-family="Lato" font-size="%g" fill="%s">%s'
                 '</text>' % (fs, INK, ''.join(lines)))

    # Back: the ISBN barcode from the printer, at the lower right of
    # the visible back board, on a light ground so that it scans:
    # white by default, or --barcode-bg, a pale colour (scanners use
    # red light, so red, orange and brown grounds read as bars).
    if args.barcode:
        bw, bh = 45.0, 28.0
        x = panel - G - 10 - bw
        y = H - M - 12 - bh
        bg = args.barcode_bg
        white = bg.lower() in ('#fff', '#ffffff', 'white')
        r_ = args.barcode_radius
        if bg.lower() != 'none':    # none: straight on the artwork
            parts.append('<rect x="%g" y="%g" width="%g" height="%g" '
                         'rx="%g" fill="%s"/>'
                         % (x - 2, y - 2, bw + 4, bh + 4, r_, bg))
        uri = data_uri(args.barcode) if white else \
            transparent_uri(args.barcode)
        parts.append('<image x="%g" y="%g" width="%g" height="%g" '
                     'preserveAspectRatio="xMidYMid meet" xlink:href="%s"/>'
                     % (x, y, bw, bh, uri))

    render(document(W, H, '\n'.join(parts)), args.output)


def transparent_uri(path):
    """A raster barcode with its white made transparent, so that it can
    lie on a coloured ground: black where the bars are, clear elsewhere."""
    ext = os.path.splitext(path)[1].lower()
    if ext not in ('.png', '.jpg', '.jpeg'):
        return data_uri(path)       # vector barcodes are usually clear
    from PIL import Image, ImageOps
    import io
    grey = Image.open(path).convert('L')
    out = Image.new('LA', grey.size, 0)
    out.putalpha(ImageOps.invert(grey))
    buf = io.BytesIO()
    out.save(buf, 'PNG')
    return 'data:image/png;base64,' + \
        base64.b64encode(buf.getvalue()).decode('ascii')


def data_uri(path):
    """An image file as a data: URI. A PDF (as printers often supply
    barcodes) is converted to SVG first, keeping it vector."""
    ext = os.path.splitext(path)[1].lower()
    if ext == '.pdf':
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, 'barcode.svg')
            need('pdftocairo', 'poppler (poppler-utils on Debian and Ubuntu)')
            subprocess.run(['pdftocairo', '-svg', path, out], check=True)
            with open(out, 'rb') as f:
                data, mime = f.read(), 'image/svg+xml'
    else:
        mime = {'.svg': 'image/svg+xml', '.png': 'image/png',
                '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg'}.get(ext)
        if not mime:
            sys.exit('mkcover: barcode must be PDF, SVG, PNG or JPEG')
        with open(path, 'rb') as f:
            data = f.read()
    return 'data:%s;base64,%s' % (mime, base64.b64encode(data).decode('ascii'))


def mm_pair(s):
    w, h = s.lower().split('x')
    return float(w), float(h)


def main():
    ap = argparse.ArgumentParser(description='Build the cover files.')
    ap.add_argument('kind', choices=['screen', 'front', 'wrap'])
    ap.add_argument('-o', '--output', required=True)
    ap.add_argument('--trim', type=mm_pair, default=(135, 215),
                    help='front: trim size, WxH mm (default 135x215)')
    ap.add_argument('--bleed', type=float, default=5,
                    help='front: bleed on each edge, mm (default 5, as BoD asks)')
    ap.add_argument('--width', type=float, help='wrap: total width, mm')
    ap.add_argument('--height', type=float, help='wrap: total height, mm')
    ap.add_argument('--spine', type=float, help='wrap: spine width, mm')
    ap.add_argument('--wrap', type=float,
                    help='wrap: margin outside the visible board, mm')
    ap.add_argument('--hinge', type=float, default=0,
                    help='wrap: width of the fold beside the spine on each '
                         'board, kept clear of text, mm (default 0)')
    ap.add_argument('--barcode',
                    help='wrap: the ISBN barcode file (PDF, SVG, PNG, JPEG)')
    ap.add_argument('--barcode-bg', default='#ffffff',
                    help='wrap: the colour behind the barcode, kept pale, or none '
                    'to print it straight on a pale part of the artwork')
    ap.add_argument('--barcode-radius', type=float, default=0,
                    help='wrap: corner radius of the barcode ground, mm')
    args = ap.parse_args()

    if args.kind == 'wrap' and None in (args.width, args.height,
                                        args.spine, args.wrap):
        ap.error('wrap needs --width, --height, --spine and --wrap, '
                 'from the printer\'s cover template')

    {'screen': screen, 'front': front, 'wrap': wrap}[args.kind](args)
    return 0


if __name__ == '__main__':
    sys.exit(main())
