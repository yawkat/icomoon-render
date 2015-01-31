#!/usr/bin/env python3

import json
import os
import sys
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-o", "--output-dir", dest="output_dir", required=True)

args = parser.parse_args()

with open(os.path.join(os.path.dirname(__file__), "font.json")) as f:
    glyphs = json.load(f)

# assign characters xe600+
char = 0xe600
for glyph in glyphs:
    glyph["char"] = char
    char += 1

svg = os.path.join(args.output_dir, "font.svg")
with open(svg, "w") as f:
    # who needs xml libs anyway?
    f.write((
        '<?xml version="1.0" standalone="no"?>'
        '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd" >'
        '<svg xmlns="http://www.w3.org/2000/svg">'
            '<defs>'
                '<font horiz-adv-x="1024" id="icon_font">'
                    '<font-face ascent="960" descent="-64" units-per-em="1024"/>'
                    '<missing-glyph horiz-adv-x="1024"/>'
    ))
    for glyph in glyphs:
        f.write('<glyph d="%s" unicode="&#x%x;"' % (glyph["path"], glyph["char"]))
        if glyph["width"] != 1:
            f.write(' horiz-adv-x="%d"' % (glyph["width"] * 1024))
        f.write('/>')
    f.write((
                '</font>'
            '</defs>'
        '</svg>'
    ))

ttf = os.path.join(args.output_dir, "font.ttf")
os.system("svg2ttf -c '' '%s' '%s'" % (svg, ttf))

css = os.path.join(args.output_dir, "font.css")
with open(css, "w") as f:
    for glyph in glyphs:
        f.write(".icon-%s:before{content:'\%x'}" % (glyph["name"], glyph["char"]))
