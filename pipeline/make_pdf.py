import re
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch

src=open('/workspace/leptomeningeal/REPORT.md').read().split('\n')
ss=getSampleStyleSheet()
body=ParagraphStyle('b',parent=ss['BodyText'],fontSize=9,leading=12)
quote=ParagraphStyle('q',parent=body,leftIndent=12,textColor=colors.HexColor('#7a2f00'),backColor=colors.HexColor('#fff5e6'),borderPadding=4)
cell=ParagraphStyle('c',parent=body,fontSize=6,leading=7.5)
hdr=ParagraphStyle('h',parent=cell,fontName='Helvetica-Bold')
H={1:ParagraphStyle('h1',parent=ss['Heading1'],fontSize=16),2:ParagraphStyle('h2',parent=ss['Heading2'],fontSize=12),3:ParagraphStyle('h3',parent=ss['Heading3'],fontSize=10)}

def inline(t):
    t=t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    t=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',t)
    t=re.sub(r'`(.+?)`',r'<font face="Courier">\1</font>',t)
    return t

flow=[]; i=0; W=10.0*inch
while i<len(src):
    ln=src[i]
    if ln.startswith('|'):
        rows=[]
        while i<len(src) and src[i].startswith('|'):
            cells=[c.strip() for c in src[i].strip().strip('|').split('|')]
            if not set(''.join(cells))<=set('-: '): rows.append(cells)
            i+=1
        n=max(len(r) for r in rows)
        data=[[Paragraph(inline(c),hdr if ri==0 else cell) for c in r+['']*(n-len(r))] for ri,r in enumerate(rows)]
        t=Table(data,colWidths=[W/n]*n,repeatRows=1)
        t.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.25,colors.grey),
            ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e8eef7')),
            ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),2),('RIGHTPADDING',(0,0),(-1,-1),2)]))
        flow+=[t,Spacer(1,10)]; continue
    if ln.startswith('#'):
        lvl=len(ln)-len(ln.lstrip('#'))
        flow+=[Paragraph(inline(ln.lstrip('# ')),H.get(min(lvl,3)))]
    elif ln.startswith('>'):
        buf=[]
        while i<len(src) and src[i].startswith('>'):
            buf.append(src[i].lstrip('> ').strip()); i+=1
        flow+=[Paragraph(inline('<br/>'.join(x for x in buf if x)),quote),Spacer(1,8)]; continue
    elif ln.strip()=='---':
        flow+=[Spacer(1,8)]
    elif ln.strip():
        flow+=[Paragraph(inline(ln.strip()),body),Spacer(1,4)]
    i+=1

def foot(c,d):
    c.setFont('Helvetica-Oblique',7); c.setFillColor(colors.grey)
    c.drawString(0.5*inch,0.35*inch,'Model scores are hypotheses only — not clinical proof of efficacy or safety.')
    c.drawRightString(10.5*inch,0.35*inch,'LMD report 2026-10-15 — page %d'%c.getPageNumber())

SimpleDocTemplate('/workspace/leptomeningeal/LMD_report_2026-10-15.pdf',pagesize=landscape(letter),
    leftMargin=0.5*inch,rightMargin=0.5*inch,topMargin=0.5*inch,bottomMargin=0.55*inch,
    title='Leptomeningeal disease — evidence-first pipeline report').build(flow,onFirstPage=foot,onLaterPages=foot)
print('ok')
