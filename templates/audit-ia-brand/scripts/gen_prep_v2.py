from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    Table, TableStyle, PageBreak
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import Flowable
import os

HOT_PINK   = colors.HexColor("#FF2D8A")
DEEP_PINK  = colors.HexColor("#C4005D")
BLACK      = colors.HexColor("#0F0F0F")
DARK_GREY  = colors.HexColor("#2D2028")
MID_GREY   = colors.HexColor("#8A7A84")
LIGHT_GREY = colors.HexColor("#C8BEC5")
CREAM      = colors.HexColor("#FFF0F7")
LIGHT_PINK = colors.HexColor("#FFE0F0")

W, H = A4
OUTPUT = "/mnt/user-data/outputs/AngryDollz_PrepCall.pdf"

# ── PAGE BG ───────────────────────────────────────────────────────────────────
def page_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.white)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    canvas.setFillColor(HOT_PINK)
    canvas.rect(0, 0, 3*mm, H, fill=1, stroke=0)
    canvas.setFillColor(BLACK)
    canvas.rect(0, H - 20*mm, W, 20*mm, fill=1, stroke=0)
    # subtle pink dot pattern top right
    canvas.setFillColor(HOT_PINK)
    canvas.setFillAlpha(0.06)
    for i in range(5):
        for j in range(3):
            canvas.circle(W - 15*mm - i*8*mm, H - 5*mm - j*8*mm, 2*mm, fill=1, stroke=0)
    canvas.setFillAlpha(1)
    canvas.restoreState()

# ── STYLES ────────────────────────────────────────────────────────────────────
def S(name, **kw):
    d = dict(fontName="Helvetica", fontSize=10, leading=15,
             textColor=BLACK, spaceAfter=0, spaceBefore=0, alignment=TA_LEFT)
    d.update(kw)
    return ParagraphStyle(name, **d)

sHEADER_BRAND = S("hb", fontName="Helvetica-Bold", fontSize=11,
                  textColor=HOT_PINK, letterSpacing=2.5)
sHEADER_RIGHT = S("hr", fontName="Helvetica", fontSize=8.5,
                  textColor=LIGHT_GREY, alignment=2)
sEYEBROW      = S("eb", fontName="Helvetica-Bold", fontSize=7.5,
                  textColor=HOT_PINK, letterSpacing=2.5, spaceAfter=2)
sINTRO        = S("ib", fontName="Helvetica", fontSize=10, leading=16,
                  textColor=DARK_GREY)
sSECTION      = S("sc", fontName="Helvetica-Bold", fontSize=7.5,
                  textColor=MID_GREY, letterSpacing=2, spaceAfter=2)
sFOOTER       = S("ft", fontName="Helvetica", fontSize=7.5,
                  textColor=LIGHT_GREY, alignment=TA_CENTER)

# ── QUESTION CARD ─────────────────────────────────────────────────────────────
class QCard(Flowable):
    def __init__(self, num, question, hint, tag=None, accent=None):
        super().__init__()
        self.num = num
        self.question = question
        self.hint = hint
        self.tag = tag
        self.accent = accent or HOT_PINK

    def wrap(self, aw, ah):
        self._w = aw
        # Estimate height based on text length
        q_lines = max(1, len(self.question) // 62)
        h_lines = max(1, len(self.hint) // 78) if self.hint else 0
        self.height = (10 + q_lines * 13 + h_lines * 11 + 10) * mm / 3.78
        self.height = max(15*mm, min(self.height, 24*mm))
        return (self._w, self.height)

    def draw(self):
        c = self.canv
        w, h = self._w, self.height
        c.saveState()

        # Background
        c.setFillColor(CREAM)
        c.roundRect(0, 0, w, h, 4, fill=1, stroke=0)

        # Left accent
        c.setFillColor(self.accent)
        c.roundRect(0, 0, 3.5, h, 2, fill=1, stroke=0)

        # Tag pill (top right)
        if self.tag:
            tag_w = len(self.tag) * 5.5 + 10
            c.setFillColor(self.accent)
            c.roundRect(w - tag_w - 6, h - 14, tag_w, 11, 3, fill=1, stroke=0)
            c.setFillColor(colors.white)
            c.setFont("Helvetica-Bold", 6.5)
            c.drawString(w - tag_w - 1, h - 10, self.tag.upper())

        # Number
        c.setFillColor(self.accent)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(10, h - 16, self.num)

        # Question
        c.setFillColor(BLACK)
        c.setFont("Helvetica-Bold", 10.5)
        # Manual word wrap at ~58 chars
        words = self.question.split()
        lines = []
        cur = ""
        for word in words:
            if len(cur) + len(word) < 58:
                cur = (cur + " " + word).strip()
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)

        q_start_y = h - 14
        for i, line in enumerate(lines):
            c.drawString(34, q_start_y - i * 13, line)

        # Hint
        if self.hint:
            hint_y = q_start_y - len(lines) * 13 - 2
            c.setFillColor(MID_GREY)
            c.setFont("Helvetica-Oblique", 8.5)
            # Word wrap hint
            hwords = self.hint.split()
            hline = ""
            hlines = []
            for word in hwords:
                if len(hline) + len(word) < 72:
                    hline = (hline + " " + word).strip()
                else:
                    hlines.append(hline)
                    hline = word
            hlines.append(hline)
            for j, hl in enumerate(hlines):
                c.drawString(10, hint_y - j * 11, hl)

        c.restoreState()


class SectionLabel(Flowable):
    """Pink pill label for a question group"""
    def __init__(self, text):
        super().__init__()
        self.text = text

    def wrap(self, aw, ah):
        self._w = aw
        self.height = 8*mm
        return (self._w, self.height)

    def draw(self):
        c = self.canv
        c.saveState()
        label_w = len(self.text) * 5.8 + 14
        c.setFillColor(BLACK)
        c.roundRect(0, 1.5*mm, label_w, 5*mm, 3, fill=1, stroke=0)
        c.setFillColor(HOT_PINK)
        c.setFont("Helvetica-Bold", 7)
        c.drawString(7, 3*mm, self.text.upper())
        c.restoreState()


class TeaserBox(Flowable):
    def __init__(self):
        super().__init__()

    def wrap(self, aw, ah):
        self._w = aw
        self.height = 16*mm
        return (self._w, self.height)

    def draw(self):
        c = self.canv
        w, h = self._w, self.height
        c.saveState()
        c.setFillColor(BLACK)
        c.roundRect(0, 0, w, h, 5, fill=1, stroke=0)
        # Pink left band
        c.setFillColor(HOT_PINK)
        c.roundRect(0, 0, 4, h, 2, fill=1, stroke=0)
        c.setFillColor(HOT_PINK)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(12, h - 9, "WHAT'S WAITING FOR YOU AFTER OUR CALL")
        c.setFillColor(LIGHT_GREY)
        c.setFont("Helvetica", 9)
        c.drawString(12, h - 21, "A full AI brand audit, a 25-prompt pack written for Angry Dollz,")
        c.drawString(12, h - 32, "and a concrete 30/90-day action plan. All ready to hand over.")
        c.restoreState()


# ── BUILD ─────────────────────────────────────────────────────────────────────
def build():
    story = []
    story.append(Spacer(1, 5*mm))

    # Header
    h_tbl = Table([[
        Paragraph("ANGRY DOLLZ", sHEADER_BRAND),
        Paragraph("Florian Dierckx  ·  AI & Brand Consultant", sHEADER_RIGHT)
    ]], colWidths=[85*mm, W - 43*mm - 85*mm])
    h_tbl.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(h_tbl)
    story.append(Spacer(1, 2*mm))
    story.append(HRFlowable(color=HOT_PINK, thickness=1.5, width="100%"))
    story.append(Spacer(1, 3*mm))

    # Eyebrow + intro
    story.append(Paragraph("BEFORE OUR CALL", sEYEBROW))
    story.append(Spacer(1, 1.5*mm))
    story.append(Paragraph(
        "A few questions to have in the back of your mind before we talk. No need to write anything — "
        "just having thought about them means we can go straight to the good stuff.",
        sINTRO))
    story.append(Spacer(1, 3*mm))
    story.append(HRFlowable(color=colors.HexColor("#EEE6EB"), thickness=0.5, width="100%"))
    story.append(Spacer(1, 4*mm))

    # ── BLOCK 1: YOUR AUDIENCE ────────────────────────────────────────────────
    story.append(Spacer(1, 0*mm))
    story.append(SectionLabel("Your Audience"))
    story.append(Spacer(1, 1.5*mm))

    story.append(QCard("01",
        "Who actually buys from you vs who just follows you?",
        "Age range, where they train, what they care about beyond fitness.",
        tag="Audience"))
    story.append(Spacer(1, 1.5*mm))

    story.append(QCard("02",
        "Which platform drives the most actual sales for you right now?",
        "Instagram, TikTok, word of mouth, DMs directly?",
        tag="Channels"))
    story.append(Spacer(1, 2.5*mm))

    # ── BLOCK 2: CONTENT & OPERATIONS ────────────────────────────────────────
    story.append(Spacer(1, 0*mm))
    story.append(SectionLabel("Content & Operations"))
    story.append(Spacer(1, 1.5*mm))

    story.append(QCard("03",
        "How many hours a week goes to content — roughly?",
        "Writing captions, editing, posting, coming up with ideas, replying to comments.",
        tag="Time"))
    story.append(Spacer(1, 1.5*mm))

    story.append(QCard("04",
        "Are you posting Reels or TikToks consistently, or mainly static posts?",
        "Video is where the algorithm is in 2026 — I want to know where you're at with it.",
        tag="Video",
        accent=DEEP_PINK))
    story.append(Spacer(1, 1.5*mm))

    story.append(QCard("05",
        "What's the top DM question you answer every single week?",
        "The one you could answer in your sleep.",
        tag="DMs"))
    story.append(Spacer(1, 2.5*mm))

    # ── BLOCK 3: BUSINESS & REVENUE ──────────────────────────────────────────
    story.append(Spacer(1, 0*mm))
    story.append(SectionLabel("Business & Revenue"))
    story.append(Spacer(1, 1.5*mm))

    story.append(QCard("06",
        "Do you have an email list? If yes — what do you currently do with it?",
        "Even 'I have one but never use it' is useful — no judgment.",
        tag="Email",
        accent=DEEP_PINK))
    story.append(Spacer(1, 1.5*mm))

    story.append(QCard("07",
        "What does a drop look like for you in terms of prep time and revenue?",
        "Roughly — I want to understand the cycle and what a good drop vs average drop looks like.",
        tag="Drops"))
    story.append(Spacer(1, 2.5*mm))

    # ── BLOCK 4: VISION ───────────────────────────────────────────────────────
    story.append(Spacer(1, 0*mm))
    story.append(SectionLabel("Vision"))
    story.append(Spacer(1, 1.5*mm))

    story.append(QCard("08",
        "What would 'this is working really well' look like for you in 6 months?",
        "Revenue, time, audience size, vibe — whatever feels most meaningful to you.",
        tag="Goals",
        accent=DEEP_PINK))
    story.append(Spacer(1, 1.5*mm))

    story.append(QCard("09",
        "Is there anything you've already tried and dropped — tools, strategies, ideas?",
        "Important so we don't waste time recommending what's already been ruled out.",
        tag="Context"))
    story.append(Spacer(1, 2*mm))

    story.append(HRFlowable(color=colors.HexColor("#EEE6EB"), thickness=0.5, width="100%"))
    story.append(Spacer(1, 2*mm))

    # Teaser
    story.append(TeaserBox())
    story.append(Spacer(1, 3*mm))

    # Footer
    story.append(HRFlowable(color=colors.HexColor("#EEE6EB"), thickness=0.5, width="100%"))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        "Florian Dierckx  ·  AI & Brand Consultant  ·  dierckx.florian@gmail.com",
        sFOOTER))

    return story

def main():
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    doc = SimpleDocTemplate(OUTPUT, pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=20*mm, bottomMargin=8*mm)
    doc.build(build(), onFirstPage=page_bg, onLaterPages=page_bg)
    from pypdf import PdfReader
    n = len(PdfReader(OUTPUT).pages)
    print(f"PrepCall v2: {n} page(s) -> {OUTPUT}")

main()
