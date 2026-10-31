"""Export the compact manuscript as A4 two-column PDF without training models.

Install reportlab into .tools/pdf_export; matplotlib is used for two equations.
Run: py kredit/build_minipaper_pdf.py
"""
from pathlib import Path
import html
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.tools/pdf_export'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, NextPageTemplate, FrameBreak,
    Paragraph, Spacer, Image, Table, TableStyle, KeepTogether,
)

SOURCE = ROOT / 'kredit/paper/paper_minipaper_en.md'
OUTPUT = ROOT / 'output/pdf/paper_minipaper_en.pdf'
CACHE = ROOT / 'tmp/minipaper_export'
CACHE.mkdir(parents=True, exist_ok=True)
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
for name, filename in [('TNR', 'times.ttf'), ('TNR-Bold', 'timesbd.ttf'),
                       ('TNR-Italic', 'timesi.ttf'), ('TNR-BoldItalic', 'timesbi.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(Path('C:/Windows/Fonts') / filename)))
pdfmetrics.registerFontFamily('TNR', normal='TNR', bold='TNR-Bold',
                              italic='TNR-Italic', boldItalic='TNR-BoldItalic')
W, H = A4
MARGIN, GAP = 43, 16
COL = (W - 2*MARGIN - GAP) / 2
styles = {
    'body': ParagraphStyle('body', fontName='TNR', fontSize=10, leading=11.7,
                           alignment=TA_JUSTIFY, spaceAfter=5),
    'heading': ParagraphStyle('heading', fontName='TNR-Bold', fontSize=10,
                              leading=12, spaceBefore=8, spaceAfter=5, keepWithNext=True),
    'sub': ParagraphStyle('sub', fontName='TNR-Italic', fontSize=10,
                          leading=12, spaceBefore=5, spaceAfter=4, keepWithNext=True),
    'caption': ParagraphStyle('caption', fontName='TNR', fontSize=8.5,
                              leading=10, spaceAfter=6),
    'cell': ParagraphStyle('cell', fontName='TNR', fontSize=8, leading=9.5),
    'ref': ParagraphStyle('ref', fontName='TNR', fontSize=8.5, leading=10,
                          spaceAfter=4, wordWrap='LTR'),
    'title': ParagraphStyle('title', fontName='TNR-Bold', fontSize=17,
                            leading=20, alignment=TA_CENTER, spaceAfter=9),
    'authors': ParagraphStyle('authors', fontName='TNR', fontSize=9,
                              leading=12, alignment=TA_CENTER),
}


def inline(text):
    # Keep bibliography links clickable without printing Markdown syntax.
    links = []
    def link(match):
        links.append((match[1], match[2]))
        return f'LINKTOKEN{len(links)-1}END'
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link, text)
    text = html.escape(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*([^*]+)\*', r'<i>\1</i>', text)
    text = text.replace('`', '')
    for i, (label, url) in enumerate(links):
        text = text.replace(f'LINKTOKEN{i}END',
                            f'<link href="{html.escape(url, quote=True)}">{html.escape(label)}</link>')
    return text


def para(text, style='body'):
    return Paragraph(inline(text), styles[style])


def figure(path):
    with PILImage.open(path) as im:
        width, height = im.size
    return Image(str(path), width=COL, height=COL*height/width)


def equation(text, number):
    text = ''.join(text.splitlines()).replace(r'\setminus', r'\backslash')
    fig = plt.figure(figsize=(7, 0.9))
    fig.text(.02, .45, '$'+text+'$', fontsize=16, va='center')
    path = CACHE / f'equation_{number}.png'
    fig.savefig(path, dpi=240, bbox_inches='tight', pad_inches=.03)
    plt.close(fig)
    img = figure(path)
    return KeepTogether([img, Spacer(1, 5)])


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('TNR', 8)
    canvas.drawCentredString(W/2, 24, str(doc.page))
    canvas.restoreState()


def build():
    text = SOURCE.read_text(encoding='utf-8')
    title = text.splitlines()[0].removeprefix('# ')
    author_text = text.split('## Abstract')[0].split('\n\n')[1:5]
    doc = BaseDocTemplate(str(OUTPUT), pagesize=A4, title=title,
                          author='; '.join(author_text), leftMargin=MARGIN,
                          rightMargin=MARGIN, topMargin=36, bottomMargin=36)
    def cols(top):
        return [Frame(MARGIN, 36, COL, top-36, leftPadding=0, rightPadding=0,
                      topPadding=0, bottomPadding=0, id='left'),
                Frame(MARGIN+COL+GAP, 36, COL, top-36, leftPadding=0,
                      rightPadding=0, topPadding=0, bottomPadding=0, id='right')]
    # Title occupies a full-width frame; reading then follows left/right columns.
    title_frame = Frame(MARGIN, H-145, W-2*MARGIN, 110, leftPadding=0,
                        rightPadding=0, topPadding=0, bottomPadding=0, id='title')
    doc.addPageTemplates([
        PageTemplate(id='first', frames=[title_frame]+cols(H-155), onPage=footer),
        PageTemplate(id='article', frames=cols(H-36), onPage=footer),
    ])
    story = [Paragraph(html.escape(title), styles['title']),
             Paragraph('<br/>'.join(html.escape(a) for a in author_text), styles['authors']),
             NextPageTemplate('article'), FrameBreak()]
    blocks = [b.strip() for b in re.split(r'\n\s*\n', text.split('## Abstract', 1)[1]) if b.strip()]
    story.append(para('Abstract', 'heading'))
    eq_num = 0
    skip = False
    for index, block in enumerate(blocks):
        if skip:
            skip = False
            continue
        block = block.strip()
        if not block:
            continue
        if block.startswith('$$'):
            eq_num += 1
            story.append(equation(block.strip('$').strip(), eq_num))
        elif block.startswith('!['):
            path = SOURCE.parent / re.search(r'\]\(([^)]+)\)', block)[1]
            if index+1 < len(blocks) and blocks[index+1].startswith('**Figure'):
                story.append(KeepTogether([figure(path), para(blocks[index+1], 'caption')]))
                skip = True
            else:
                story.append(figure(path))
        elif block.startswith('|'):
            rows = [line.strip().strip('|').split('|') for line in block.splitlines()]
            rows = [r for r in rows if not all(re.fullmatch(r'\s*:?-+:?\s*', c) for c in r)]
            widths = [COL*.40]+[COL*.60/(len(rows[0])-1)]*(len(rows[0])-1)
            cells = [[para(c.strip(), 'cell') for c in row] for row in rows]
            table = Table(cells, colWidths=widths, repeatRows=1, hAlign='LEFT')
            table.setStyle(TableStyle([
                ('VALIGN',(0,0),(-1,-1),'TOP'), ('LINEABOVE',(0,0),(-1,0),.6,colors.black),
                ('LINEBELOW',(0,0),(-1,0),.4,colors.black),
                ('LINEBELOW',(0,-1),(-1,-1),.6,colors.black),
                ('LEFTPADDING',(0,0),(-1,-1),3), ('RIGHTPADDING',(0,0),(-1,-1),3),
            ]))
            story.extend([table, Spacer(1, 6)])
        elif block.startswith('### '):
            story.append(para(block[4:], 'sub'))
        elif block.startswith('## '):
            story.append(para(block[3:], 'heading'))
        else:
            style = 'ref' if re.match(r'^\[\d+\]', block) else 'caption' if block.startswith(('**Figure', '**Table')) else 'body'
            item = para(' '.join(block.splitlines()), style)
            if block.startswith('**Table'):
                item.keepWithNext = True
            story.append(item)
    doc.build(story)
    print(OUTPUT)


if __name__ == '__main__':
    build()
