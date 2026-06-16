import sys
sys.path.insert(0, '/home/claude')
import importlib
import fixed_content
importlib.reload(fixed_content)
C = fixed_content.AUDIT_CONTENT

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    PageBreak, Table, TableStyle, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import Flowable
import os

HOT_PINK   = colors.HexColor("#FF2D8A")
DEEP_PINK  = colors.HexColor("#C4005D")
BLACK      = colors.HexColor("#0F0F0F")
LIGHT_GREY = colors.HexColor("#E8E0E5")
MID_GREY   = colors.HexColor("#8A7A84")
DARK_GREY  = colors.HexColor("#2D2028")
CREAM      = colors.HexColor("#FFF0F7")
W, H = A4
OUTPUT = "/mnt/user-data/outputs/AngryDollz_AI_Audit_v2.pdf"

def cover_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BLACK)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.setFillColor(HOT_PINK)
    p = canvas.beginPath()
    p.moveTo(0, H * 0.42); p.lineTo(W * 0.55, H * 0.42)
    p.lineTo(W, H * 0.35); p.lineTo(W, H * 0.32)
    p.lineTo(W * 0.55, H * 0.39); p.lineTo(0, H * 0.39)
    p.close(); canvas.drawPath(p, fill=1, stroke=0)
    canvas.restoreState()

def interior_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.white)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.setFillColor(HOT_PINK)
    canvas.rect(0, 0, 3*mm, H, fill=1, stroke=0)
    if doc.page > 1:
        canvas.setFillColor(MID_GREY); canvas.setFont("Helvetica", 8)
        canvas.drawRightString(W - 15*mm, 10*mm, f"{doc.page}")
        canvas.setFillColor(HOT_PINK)
        canvas.drawString(15*mm, 10*mm, "ANGRY DOLLZ  ·  AI BRAND AUDIT")
    canvas.restoreState()

def section_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.HexColor('#3D1E2E')); canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.setFillColor(HOT_PINK); canvas.rect(0, 0, W, 6*mm, fill=1, stroke=0)
    canvas.setFillColor(MID_GREY); canvas.setFont("Helvetica", 8)
    canvas.drawRightString(W - 15*mm, 10*mm, f"{doc.page}")
    canvas.restoreState()

SECTION_PAGES = {4, 8, 12, 16, 20, 24, 28}

def page_template(canvas, doc):
    if doc.page == 1: cover_bg(canvas, doc)
    else: interior_bg(canvas, doc)

def S(name, **kw):
    d = dict(fontName="Helvetica", fontSize=10, leading=15, textColor=BLACK,
             spaceAfter=6, spaceBefore=0, alignment=TA_LEFT)
    d.update(kw); return ParagraphStyle(name, **d)

sCOVER_TAG   = S("ctag", fontName="Helvetica", fontSize=9, textColor=HOT_PINK, letterSpacing=3, spaceAfter=4)
sCOVER_TITLE = S("ctit", fontName="Helvetica-Bold", fontSize=38, textColor=colors.white, leading=44, spaceAfter=6)
sCOVER_SUB   = S("csub", fontName="Helvetica", fontSize=13, textColor=LIGHT_GREY, leading=19, spaceAfter=0)
sCOVER_CRED  = S("cred", fontName="Helvetica", fontSize=9, textColor=MID_GREY)
sCOVER_DATE  = S("cdat", fontName="Helvetica-Bold", fontSize=9, textColor=HOT_PINK)
sSEC_NUM     = S("snum", fontName="Helvetica-Bold", fontSize=52, textColor=HOT_PINK, leading=56, spaceAfter=2)
sSEC_TITLE   = S("stit", fontName="Helvetica-Bold", fontSize=26, textColor=colors.HexColor("#FFFFFF"), leading=32, spaceAfter=10)
sSEC_DESC    = S("sdsc", fontName="Helvetica-Bold", fontSize=13, textColor=colors.HexColor("#FFFFFF"), leading=20)
sH1          = S("h1",   fontName="Helvetica-Bold", fontSize=19, textColor=BLACK, leading=25, spaceAfter=4, spaceBefore=4)
sH2          = S("h2",   fontName="Helvetica-Bold", fontSize=12, textColor=HOT_PINK, leading=17, spaceAfter=3, spaceBefore=6)
sH3          = S("h3",   fontName="Helvetica-Bold", fontSize=10, textColor=BLACK, leading=15, spaceAfter=3, spaceBefore=4)
sBODY        = S("bod",  fontName="Helvetica", fontSize=9.5, leading=15, textColor=DARK_GREY, spaceAfter=7, alignment=TA_JUSTIFY)
sBUL         = S("bul",  fontName="Helvetica", fontSize=9.5, leading=15, textColor=DARK_GREY, spaceAfter=4, leftIndent=6)
sLBL         = S("lbl",  fontName="Helvetica-Bold", fontSize=7.5, textColor=HOT_PINK, letterSpacing=2.5, spaceAfter=2, spaceBefore=8)
sCAPT        = S("cap",  fontName="Helvetica-Oblique", fontSize=8, textColor=MID_GREY, leading=12, spaceAfter=4)
sTOC_T       = S("tott", fontName="Helvetica-Bold", fontSize=16, textColor=BLACK, spaceAfter=10)
sTOC_I       = S("toti", fontName="Helvetica", fontSize=9.5, textColor=DARK_GREY, leading=15, spaceAfter=2)
sFOOT        = S("foot", fontName="Helvetica", fontSize=7.5, textColor=MID_GREY, alignment=TA_CENTER)

class PinkBox(Flowable):
    def __init__(self, title, body, bg=None, accent=None):
        super().__init__()
        self.title = title; self.body = body
        self.bg = bg or CREAM; self.accent = accent or HOT_PINK
    def wrap(self, aw, ah):
        self._w = aw
        lines = len(self.body)//80 + self.body.count('\n') + 3
        self.height = max(26*mm, lines*4.8*mm + 14*mm)
        return (self._w, self.height)
    def draw(self):
        c = self.canv; w, h = self._w, self.height
        c.saveState()
        c.setFillColor(self.bg); c.roundRect(0,0,w,h,4,fill=1,stroke=0)
        c.setFillColor(self.accent); c.roundRect(0,0,4,h,2,fill=1,stroke=0)
        c.setFillColor(self.accent); c.setFont("Helvetica-Bold",8.5)
        c.drawString(10, h-12, self.title.upper())
        c.setFillColor(DARK_GREY); c.setFont("Helvetica",9)
        txt = c.beginText(10, h-24); txt.setLeading(13.5)
        for line in self.body.split('\n'):
            words = line.split(); cur=""
            for w2 in words:
                if len(cur)+len(w2)<92: cur=(cur+" "+w2).strip()
                else: txt.textLine(cur); cur=w2
            txt.textLine(cur)
        c.drawText(txt); c.restoreState()

class ScoreBar(Flowable):
    def __init__(self, label, score):
        super().__init__(); self.label=label; self.score=score; self.height=11*mm
    def wrap(self, aw, ah):
        self._w=aw; return (self._w, self.height)
    def draw(self):
        c=self.canv; w=self._w
        c.setFont("Helvetica",8.5); c.setFillColor(DARK_GREY)
        c.drawString(0, self.height-7, self.label)
        c.setFont("Helvetica-Bold",8.5); c.setFillColor(HOT_PINK)
        c.drawRightString(w, self.height-7, f"{self.score}/10")
        by=self.height-15; bh=5
        c.setFillColor(LIGHT_GREY); c.roundRect(0,by,w,bh,2,fill=1,stroke=0)
        fw=(self.score/10)*w
        col=HOT_PINK if self.score>=7 else (colors.HexColor("#F4A41C") if self.score>=5 else colors.HexColor("#E05555"))
        c.setFillColor(col); c.roundRect(0,by,fw,bh,2,fill=1,stroke=0)

class DarkBox(Flowable):
    def __init__(self, headline, body):
        super().__init__(); self.headline=headline; self.body=body
    def wrap(self, aw, ah):
        self._w=aw
        lines=len(self.body)//85+self.body.count('\n')+2
        self.height=max(28*mm, lines*4.8*mm+16*mm)
        return (self._w, self.height)
    def draw(self):
        c=self.canv; w,h=self._w,self.height
        c.saveState()
        c.setFillColor(DARK_GREY); c.roundRect(0,0,w,h,5,fill=1,stroke=0)
        c.setFillColor(HOT_PINK); c.setFont("Helvetica-Bold",11)
        c.drawString(12, h-16, self.headline)
        c.setFillColor(LIGHT_GREY); c.setFont("Helvetica",9)
        txt=c.beginText(12, h-30); txt.setLeading(13.5)
        for line in self.body.split('\n'):
            words=line.split(); cur=""
            for word in words:
                if len(cur)+len(word)<88: cur=(cur+" "+word).strip()
                else: txt.textLine(cur); cur=word
            txt.textLine(cur)
        c.drawText(txt); c.restoreState()

class DarkPageBg(Flowable):
    """Fills the entire page with a dark background. Place as first item after PageBreak."""
    def __init__(self, color=None):
        super().__init__()
        self.color = color or colors.HexColor("#3D1E2E")

    def wrap(self, aw, ah):
        self._aw = aw
        return (aw, 0)

    def draw(self):
        c = self.canv
        c.saveState()
        c.setFillColor(self.color)
        page_w, page_h = c._pagesize
        c.rect(-20*mm, -page_h, page_w + 40*mm, page_h * 3, fill=1, stroke=0)
        c.setFillColor(HOT_PINK)
        c.rect(-20*mm, -18*mm, page_w + 40*mm, 6*mm, fill=1, stroke=0)
        c.restoreState()


def hr(color=LIGHT_GREY, thick=0.5):
    return HRFlowable(color=color, thickness=thick, width="100%", spaceAfter=6, spaceBefore=4)
def pink_hr():
    return HRFlowable(color=HOT_PINK, thickness=1.5, width="100%", spaceAfter=8, spaceBefore=4)
def bul(text):
    return Paragraph(f"<font color='#FF2D8A'>+</font>  {text}", sBUL)

def sec_div(num, title, desc):
    return [PageBreak(), DarkPageBg(), Spacer(1,50*mm),
            Paragraph(f"0{num}", sSEC_NUM), Paragraph(title, sSEC_TITLE),
            Spacer(1,4*mm), HRFlowable(color=HOT_PINK,thickness=2,width="100%"),
            Spacer(1,6*mm), Paragraph(desc, sSEC_DESC), PageBreak()]

def week_block(title, days, tasks, outcome):
    tbl = Table([[
        Paragraph(title, S("wt", fontName="Helvetica-Bold", fontSize=10.5, textColor=colors.white)),
        Paragraph(days,  S("wd", fontName="Helvetica", fontSize=8.5, textColor=HOT_PINK, alignment=0))
    ]], colWidths=[110*mm, W-43*mm-110*mm])
    tbl.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),DARK_GREY),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('LEFTPADDING',(0,0),(0,-1),8),('RIGHTPADDING',(-1,0),(-1,-1),8),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ]))
    items = [tbl, Spacer(1,2*mm)]
    for i,t in enumerate(tasks,1):
        items.append(Paragraph(f"<b>{i}.</b>  {t}", sBUL))
    items += [Spacer(1,2*mm), PinkBox("OUTCOME", outcome), Spacer(1,6*mm)]
    return KeepTogether(items)

def build():
    story = []

    # COVER
    story += [Spacer(1,30*mm),
              Paragraph("AI BRAND AUDIT", sCOVER_TAG), Spacer(1,6*mm),
              Paragraph("Angry\nDollz", sCOVER_TITLE), Spacer(1,4*mm),
              Paragraph(C["cover_subtitle"], sCOVER_SUB),
              Spacer(1,50*mm),
              HRFlowable(color=HOT_PINK,thickness=1,width="100%"), Spacer(1,3*mm),
              Paragraph(C["cover_credit1"], sCOVER_CRED),
              Paragraph("JUNE 2026  ·  FLORIAN DIERCKX, AI CONSULTANT", sCOVER_DATE),
              PageBreak()]

    # P2: BEFORE WE START
    story += [Spacer(1,8*mm), Paragraph("Before We Start", sH1), pink_hr(),
              Spacer(1,3*mm), Paragraph(C["before_we_start_subhead"], sH2),
              Spacer(1,2*mm), Paragraph(C["before_p1"], sBODY),
              Paragraph(C["before_p2"], sBODY), Spacer(1,3*mm),
              PinkBox("THE CORE PRINCIPLE", C["core_principle_box"]),
              Spacer(1,5*mm), Paragraph(C["before_p3"], sBODY), PageBreak()]

    # P3: TOC
    story += [Spacer(1,8*mm), Paragraph("What's Inside", sTOC_T), pink_hr(), Spacer(1,4*mm)]
    for num, title, desc in C["toc_items"]:
        row = Table([[
            Paragraph(f"<b><font color='#FF2D8A'>{num}</font></b>", S("tn", fontName="Helvetica-Bold", fontSize=10)),
            Paragraph(f"<b>{title}</b>  <font size='8' color='#8A7A84'>{desc}</font>", sTOC_I)
        ]], colWidths=[16*mm, W-43*mm-16*mm])
        row.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),
            ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
            ('BOTTOMPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),0)]))
        story += [row, hr()]
    story.append(PageBreak())

    # SECTION 01: AUDIT
    for fl in sec_div(1, "Brand &\nPresence Audit", C["sec1_desc"]): story.append(fl)
    story += [Spacer(1,8*mm), Paragraph("Audit Overview", sH1), pink_hr(),
              Paragraph("THE SCORES", sLBL), Spacer(1,2*mm)]
    for label, score in [
        ("Visual identity & aesthetic coherence", 8),
        ("Instagram content consistency", 5),
        ("Website (Wix) conversion", 4),
        ("Email list & retention", 2),
        ("AI readiness (tools + mindset)", 4),
    ]:
        story += [ScoreBar(label, score), Spacer(1,3*mm)]
    story += [Spacer(1,3*mm), Paragraph("WHAT THESE SCORES MEAN", sLBL),
              Paragraph(C["scores_meaning"], sBODY),
              Spacer(1,2*mm), Paragraph("WHAT'S WORKING", sH2)]
    for pt in C["whats_working"]: story.append(bul(pt))
    story += [Spacer(1,3*mm), Paragraph("WHERE THE GAPS ARE", sH2)]
    for pt in C["gaps"]: story.append(bul(pt))
    story += [Spacer(1,4*mm), Paragraph(C["gaps_closer"], sBODY), PageBreak()]

    # SECTION 02: PAIN POINTS
    for fl in sec_div(2, "The 4 Pain\nPoints", C["sec2_desc"]): story.append(fl)
    story += [Spacer(1,8*mm), Paragraph("Where Your Week Goes", sH1), pink_hr()]
    pains = [
        (C["pain1_title"], C["pain1_body"], C["pain1_fix"]),
        (C["pain2_title"], C["pain2_body"], C["pain2_fix"]),
        (C["pain3_title"], C["pain3_body"], C["pain3_fix"]),
        (C["pain4_title"], C["pain4_body"], C["pain4_fix"]),
    ]
    for title, body, fix in pains:
        story.append(KeepTogether([
            Paragraph(title, sH2), Paragraph(body, sBODY),
            PinkBox("THE FIX", fix), Spacer(1,6*mm)
        ]))
    story.append(PageBreak())

    # SECTION 03: TOOLS
    for fl in sec_div(3, "AI Tools That\nFit Your Brand", C["sec3_desc"]): story.append(fl)
    story += [Spacer(1,8*mm), Paragraph("Your AI Stack", sH1), pink_hr(),
              Paragraph(C["tools_intro"], sBODY), Spacer(1,4*mm)]
    tools = [
        ("CONTENT & COPY", "ChatGPT or Claude", "Captions, email drafts, product descriptions, DM templates",
         C["tool_chatgpt_desc"], C["tool_chatgpt_cost"]),
        ("VISUALS", "Midjourney or Flux", "AI-generated visuals for in-between content",
         C["tool_midjourney_desc"], C["tool_midjourney_cost"]),
        ("EMAIL", "MailerLite", "Email list, automations, welcome sequences",
         C["tool_mailerlite_desc"], C["tool_mailerlite_cost"]),
        ("SITE", "Wix Chat or Tidio", "FAQ automation on your site",
         C["tool_wixchat_desc"], C["tool_wixchat_cost"]),
    ]
    for tag, name, use, desc, cost in tools:
        story.append(KeepTogether([
            Paragraph(tag, sLBL),
            Paragraph(f"<b>{name}</b>", sH3),
            Paragraph(f"<i>Use for: {use}</i>", sCAPT),
            Paragraph(desc, sBODY),
            PinkBox("COST & ACCESS", cost, bg=colors.HexColor("#FFF0F7"), accent=DEEP_PINK),
            Spacer(1,6*mm)
        ]))
    story.append(PageBreak())

    # SECTION 04: 30-DAY PLAN
    for fl in sec_div(4, "Your 30-Day\nAction Plan", C["sec4_desc"]): story.append(fl)
    story += [Spacer(1,8*mm), Paragraph("30-Day Action Plan", sH1), pink_hr(),
              PinkBox("HOW TO READ THIS PLAN", C["plan_how_to_read"]), Spacer(1,5*mm)]
    weeks = [
        (C["week1_title"], "Days 1-7",  C["week1_tasks"], C["week1_outcome"]),
        (C["week2_title"], "Days 8-14", C["week2_tasks"], C["week2_outcome"]),
        (C["week3_title"], "Days 15-21",C["week3_tasks"], C["week3_outcome"]),
        (C["week4_title"], "Days 22-30",C["week4_tasks"], C["week4_outcome"]),
    ]
    for t, d, tasks, outcome in weeks:
        story.append(week_block(t, d, tasks, outcome))
    story.append(PageBreak())

    # SECTION 05: 90-DAY VISION
    for fl in sec_div(5, "Your 90-Day\nVision", C["sec5_desc"]): story.append(fl)
    story += [Spacer(1,8*mm), Paragraph("90-Day Vision", sH1), pink_hr(),
              Paragraph(C["vision_intro"], sBODY), Spacer(1,4*mm)]
    for title, body in [
        (C["month1_title"], C["month1_body"]),
        (C["month2_title"], C["month2_body"]),
        (C["month3_title"], C["month3_body"]),
    ]:
        story.append(KeepTogether([
            Paragraph(title, sH2), Paragraph(body, sBODY), hr(), Spacer(1,2*mm)
        ]))
    story += [Spacer(1,4*mm), DarkBox("The number that matters", C["vision_cta"]), PageBreak()]

    # SECTION 06: LEARNING AI
    for fl in sec_div(6, "Learning AI\nYour Way", C["sec6_desc"]): story.append(fl)
    story += [Spacer(1,8*mm), Paragraph("Learning AI as a Founder", sH1), pink_hr(),
              Paragraph(C["learning_intro"], sBODY), Spacer(1,3*mm),
              Paragraph("THE HONEST PICTURE", sH2),
              Paragraph(C["ai_good_title"], sH3)]
    for pt in C["ai_good"]: story.append(bul(pt))
    story += [Spacer(1,3*mm), Paragraph(C["ai_bad_title"], sH3)]
    for pt in C["ai_bad"]: story.append(bul(pt))
    story += [Spacer(1,4*mm), Paragraph("HOW TO GET BETTER AT AI FAST", sH2)]
    for i, (title, body) in enumerate(C["learning_steps"], 1):
        story.append(KeepTogether([
            Paragraph(f"<b>0{i}. {title}</b>", sH3),
            Paragraph(body, sBODY), Spacer(1,2*mm)
        ]))
    story += [Spacer(1,4*mm), PinkBox("YOUR STARTING POINT", C["starting_point_box"]), PageBreak()]

    # SECTION 07: PROMPT PREVIEW
    for fl in sec_div(7, "Prompt Pack\nPreview", C["sec7_desc"]): story.append(fl)
    story += [Spacer(1,8*mm), Paragraph("5 Prompts to Start Today", sH1), pink_hr(),
              Paragraph(C["prompts_intro"], sBODY), Spacer(1,4*mm)]

    previews = [
        ("CAPTION: PRODUCT DROP",
         "You write Instagram captions for Angry Dollz, a UK brand selling bikinis, pole dance and "
         "aerial activewear, and bodybuilding stage wear. The brand is Y2K-inspired, alternative, confident, "
         "and slightly edgy. The audience is women who train hard and have a strong personal aesthetic.\n\n"
         "Write 3 caption options for a post showing [product name]. Include: one punchy opener under 10 words, "
         "2-3 lines of body copy, 5 relevant hashtags. Tone: fierce and direct. No filler."),
        ("CAPTION: LIFESTYLE / BETWEEN DROPS",
         "You write Instagram captions for Angry Dollz. Same brand context as above.\n\n"
         "Write a caption for a behind-the-scenes or lifestyle post. No product to sell. "
         "The post shows: [describe the image briefly]. Keep it under 80 words. "
         "End with a question or statement that invites a reaction."),
        ("EMAIL: WELCOME (EMAIL 1 OF 3)",
         "Write the first welcome email for the Angry Dollz email list. "
         "The subscriber signed up for early drop access and 10% off their first order.\n\n"
         "Include: subject line, personal welcome from Danielle, what they can expect, "
         "discount code [CODE], one soft CTA. Tone: warm, personal, like a text from the founder. Under 180 words."),
        ("PRODUCT DESCRIPTION",
         "Write a product description for Angry Dollz. The product is: [product name and key details].\n\n"
         "Tone: confident, slightly provocative. The buyer knows what she wants. "
         "Length: 60-80 words. Include one line about sizing and one about the look. "
         "No phrases like 'perfect for any occasion.'"),
        ("FAQ: DM RESPONSE TEMPLATE",
         "You answer customer DMs for Angry Dollz. The brand is direct and warm.\n\n"
         "Write a short DM reply for this question: [paste the question]. "
         "Keep it under 3 sentences. Sound like a real person. "
         "If you need specific details to answer, ask one clear question."),
    ]

    class DarkPromptBox(Flowable):
        def __init__(self, title, body):
            super().__init__(); self.title=title; self.body=body
        def wrap(self, aw, ah):
            self._w=aw
            lines=self.body.count('\n')+len(self.body)//75+3
            self.height=max(28*mm, lines*4.8*mm+18*mm)
            return (self._w, self.height)
        def draw(self):
            c=self.canv; w,h=self._w,self.height
            c.saveState()
            c.setFillColor(DARK_GREY); c.roundRect(0,0,w,h,5,fill=1,stroke=0)
            c.setFillColor(HOT_PINK); c.roundRect(0,h-8*mm,w,8*mm+5,5,fill=1,stroke=0)
            c.rect(0,h-8*mm,w,8*mm,fill=1,stroke=0)
            c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8)
            c.drawString(10, h-5.5*mm, self.title.upper())
            c.setFillColor(LIGHT_GREY); c.setFont("Helvetica",8.5)
            txt=c.beginText(10, h-12*mm); txt.setLeading(13)
            for line in self.body.split('\n'):
                words=line.split(); cur=""
                for word in words:
                    if len(cur)+len(word)<92: cur=(cur+" "+word).strip()
                    else: txt.textLine(cur); cur=word
                txt.textLine(cur)
            c.drawText(txt); c.restoreState()

    for tag_text, prompt_text in previews:
        story.append(KeepTogether([
            Paragraph(tag_text, sLBL), Spacer(1,2*mm),
            DarkPromptBox("COPY THIS PROMPT", prompt_text), Spacer(1,6*mm)
        ]))

    story += [Spacer(1,4*mm),
              DarkBox("Want the full Prompt Pack?",
                "The complete Angry Dollz Prompt Pack has 25 prompts covering all Instagram content types, "
                "the full 3-email welcome sequence, seasonal campaigns, Story scripts, and visual generation "
                "prompts with exact Midjourney parameters calibrated to your brand palette."),
              PageBreak()]

    # CLOSING
    story += [Spacer(1,18*mm), Paragraph("What Happens Next", sH1), pink_hr(),
              Paragraph(C["closing_p1"], sBODY), Spacer(1,4*mm)]
    for timing, action in C["closing_next_steps"]:
        row = Table([[
            Paragraph(timing, S("ns_t", fontName="Helvetica-Bold", fontSize=8.5, textColor=HOT_PINK)),
            Paragraph(action, S("ns_b", fontName="Helvetica", fontSize=9.5, textColor=DARK_GREY, leading=14))
        ]], colWidths=[28*mm, W-43*mm-28*mm])
        row.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),
            ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
            ('BOTTOMPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),0)]))
        story.append(row)
    story += [Spacer(1,6*mm), PinkBox("ONE THING", C["one_thing_box"]),
              Spacer(1,10*mm), hr(color=HOT_PINK), Spacer(1,4*mm),
              Paragraph("Florian Dierckx  ·  AI & Growth Consultant  ·  dierckx.florian@gmail.com", sFOOT),
              Paragraph("Prepared for Danielle / Angry Dollz  ·  June 2026", sFOOT)]
    return story

def main():
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    doc = SimpleDocTemplate(OUTPUT, pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm, topMargin=18*mm, bottomMargin=18*mm)
    doc.build(build(), onFirstPage=page_template, onLaterPages=page_template)
    from pypdf import PdfReader
    n = len(PdfReader(OUTPUT).pages)
    print(f"Audit v2: {n} pages -> {OUTPUT}")

main()
