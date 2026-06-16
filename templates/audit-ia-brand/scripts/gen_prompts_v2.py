import sys
sys.path.insert(0, '/home/claude')
import importlib, fixed_content
importlib.reload(fixed_content)
PC = fixed_content.PROMPT_CONTENT

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
OUTPUT = "/mnt/user-data/outputs/AngryDollz_Prompt_Pack_v2.pdf"

def cover_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BLACK); canvas.rect(0,0,W,H,fill=1,stroke=0)
    canvas.setFillColor(HOT_PINK); canvas.rect(0, H*0.12, W, 5, fill=1, stroke=0)
    canvas.setFillColor(DEEP_PINK); canvas.setFillAlpha(0.12)
    canvas.rect(W*0.6, 0, W*0.4, H, fill=1, stroke=0)
    canvas.setFillAlpha(1); canvas.restoreState()

def interior_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.white); canvas.rect(0,0,W,H,fill=1,stroke=0)
    canvas.setFillColor(HOT_PINK); canvas.rect(0,0,3*mm,H,fill=1,stroke=0)
    if doc.page > 1:
        canvas.setFillColor(MID_GREY); canvas.setFont("Helvetica",8)
        canvas.drawRightString(W-15*mm, 10*mm, f"{doc.page}")
        canvas.setFillColor(HOT_PINK)
        canvas.drawString(15*mm, 10*mm, "ANGRY DOLLZ  ·  PROMPT PACK")
    canvas.restoreState()

def section_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(DARK_GREY); canvas.rect(0,0,W,H,fill=1,stroke=0)
    canvas.setFillColor(HOT_PINK); canvas.rect(0,0,W,6*mm,fill=1,stroke=0)
    canvas.setFillColor(MID_GREY); canvas.setFont("Helvetica",8)
    canvas.drawRightString(W-15*mm, 10*mm, f"{doc.page}")
    canvas.restoreState()

SEC_PAGES = set()

def page_template(canvas, doc):
    if doc.page == 1: cover_bg(canvas, doc)
    elif doc.page in SEC_PAGES: section_bg(canvas, doc)
    else: interior_bg(canvas, doc)

def S(name, **kw):
    d = dict(fontName="Helvetica", fontSize=10, leading=15, textColor=BLACK,
             spaceAfter=6, spaceBefore=0, alignment=TA_LEFT)
    d.update(kw); return ParagraphStyle(name, **d)

sCOV_EYE  = S("ce", fontName="Helvetica", fontSize=9, textColor=HOT_PINK, letterSpacing=3, spaceAfter=4)
sCOV_TIT  = S("ct", fontName="Helvetica-Bold", fontSize=44, textColor=colors.white, leading=50, spaceAfter=6)
sCOV_SUB  = S("cs", fontName="Helvetica", fontSize=12, textColor=LIGHT_GREY, leading=19)
sCOV_FOOT = S("cf", fontName="Helvetica", fontSize=8, textColor=MID_GREY)
sCOV_FTP  = S("cfp", fontName="Helvetica-Bold", fontSize=8, textColor=HOT_PINK)
sSEC_NUM  = S("sn", fontName="Helvetica-Bold", fontSize=52, textColor=HOT_PINK, leading=56)
sSEC_TIT  = S("st", fontName="Helvetica-Bold", fontSize=24, textColor=colors.white, leading=30, spaceAfter=8)
sSEC_DSC  = S("sd", fontName="Helvetica", fontSize=11, textColor=LIGHT_GREY, leading=18)
sH1       = S("h1", fontName="Helvetica-Bold", fontSize=18, textColor=BLACK, leading=24, spaceAfter=4, spaceBefore=4)
sH2       = S("h2", fontName="Helvetica-Bold", fontSize=11, textColor=HOT_PINK, leading=16, spaceAfter=3, spaceBefore=6)
sH3       = S("h3", fontName="Helvetica-Bold", fontSize=10, textColor=BLACK, leading=15, spaceAfter=2, spaceBefore=4)
sBODY     = S("b",  fontName="Helvetica", fontSize=9.5, leading=15, textColor=DARK_GREY, spaceAfter=6, alignment=TA_JUSTIFY)
sBUL      = S("bu", fontName="Helvetica", fontSize=9.5, leading=15, textColor=DARK_GREY, spaceAfter=4, leftIndent=6)
sLBL      = S("lb", fontName="Helvetica-Bold", fontSize=7.5, textColor=HOT_PINK, letterSpacing=2.5, spaceAfter=2, spaceBefore=8)
sCAPT     = S("ca", fontName="Helvetica-Oblique", fontSize=8, textColor=MID_GREY, leading=12, spaceAfter=4)
sTOC_T    = S("tt", fontName="Helvetica-Bold", fontSize=15, textColor=BLACK, spaceAfter=10)
sTOC_I    = S("ti", fontName="Helvetica", fontSize=9.5, textColor=DARK_GREY, leading=15, spaceAfter=2)
sFOOT     = S("ft", fontName="Helvetica", fontSize=7.5, textColor=MID_GREY, alignment=TA_CENTER)

class PromptBox(Flowable):
    def __init__(self, prompt_text):
        super().__init__(); self.prompt_text = prompt_text
    def wrap(self, aw, ah):
        self._w=aw
        lines=self.prompt_text.count('\n')+len(self.prompt_text)//75+3
        self.height=max(25*mm, lines*4.8*mm+14*mm)
        return (self._w, self.height)
    def draw(self):
        c=self.canv; w,h=self._w,self.height
        c.saveState()
        c.setFillColor(DARK_GREY); c.roundRect(0,0,w,h,5,fill=1,stroke=0)
        c.setFillColor(HOT_PINK); c.roundRect(0,h-8*mm,w,8*mm+5,5,fill=1,stroke=0)
        c.rect(0,h-8*mm,w,8*mm,fill=1,stroke=0)
        c.setFillColor(colors.white); c.setFont("Helvetica-Bold",8)
        c.drawString(10, h-5.5*mm, "COPY THIS PROMPT")
        c.setFillColor(LIGHT_GREY); c.setFont("Helvetica",8.5)
        txt=c.beginText(10, h-12*mm); txt.setLeading(13)
        for line in self.prompt_text.split('\n'):
            words=line.split(); cur=""
            for word in words:
                if len(cur)+len(word)<92: cur=(cur+" "+word).strip()
                else: txt.textLine(cur); cur=word
            txt.textLine(cur)
        c.drawText(txt); c.restoreState()

class HintBox(Flowable):
    def __init__(self, text):
        super().__init__(); self.text=text
    def wrap(self, aw, ah):
        self._w=aw
        lines=len(self.text)//80+self.text.count('\n')+1
        self.height=max(14*mm, lines*4.5*mm+8*mm)
        return (self._w, self.height)
    def draw(self):
        c=self.canv; w,h=self._w,self.height
        c.saveState()
        c.setFillColor(CREAM); c.roundRect(0,0,w,h,4,fill=1,stroke=0)
        c.setFillColor(HOT_PINK); c.roundRect(0,0,4,h,2,fill=1,stroke=0)
        c.setFont("Helvetica-Bold",7.5); c.setFillColor(HOT_PINK)
        c.drawString(10, h-7, "PROMPT TIP")
        c.setFillColor(DARK_GREY); c.setFont("Helvetica",8.5)
        txt=c.beginText(10, h-17); txt.setLeading(13)
        for line in self.text.split('\n'):
            words=line.split(); cur=""
            for word in words:
                if len(cur)+len(word)<90: cur=(cur+" "+word).strip()
                else: txt.textLine(cur); cur=word
            txt.textLine(cur)
        c.drawText(txt); c.restoreState()

def hr(color=LIGHT_GREY, thick=0.5):
    return HRFlowable(color=color, thickness=thick, width="100%", spaceAfter=6, spaceBefore=4)
def pink_hr():
    return HRFlowable(color=HOT_PINK, thickness=1.5, width="100%", spaceAfter=8, spaceBefore=4)

def sec_div(num, title, desc):
    return [PageBreak(), Spacer(1,50*mm),
            Paragraph(f"0{num}", sSEC_NUM), Paragraph(title, sSEC_TIT),
            Spacer(1,4*mm), HRFlowable(color=HOT_PINK,thickness=2,width="100%"),
            Spacer(1,6*mm), Paragraph(desc, sSEC_DSC), PageBreak()]

def entry(num, cat, use_when, prompt_text, hint=None):
    items = [
        Paragraph(cat, sLBL),
        Paragraph(f"<b>Prompt #{num}</b>", S("pn", fontName="Helvetica-Bold", fontSize=10, textColor=BLACK, spaceAfter=2)),
        Paragraph(f"Use when: {use_when}", sCAPT),
        Spacer(1,2*mm), PromptBox(prompt_text),
    ]
    if hint: items += [Spacer(1,2*mm), HintBox(hint)]
    items.append(Spacer(1,7*mm))
    return KeepTogether(items)

def build():
    story = []

    # COVER
    story += [Spacer(1,22*mm), Paragraph("ANGRY DOLLZ", sCOV_EYE), Spacer(1,4*mm),
              Paragraph("AI\nPrompt\nPack", sCOV_TIT), Spacer(1,5*mm),
              Paragraph(PC["cover_subtitle"], sCOV_SUB),
              Spacer(1,42*mm), HRFlowable(color=HOT_PINK,thickness=1,width="100%"),
              Spacer(1,3*mm), Paragraph("Prepared for Danielle  ·  Angry Dollz  ·  June 2026", sCOV_FOOT),
              Paragraph("FLORIAN DIERCKX, AI CONSULTANT", sCOV_FTP), PageBreak()]

    # HOW TO USE
    story += [Spacer(1,8*mm), Paragraph("How to Use This Pack", sH1), pink_hr(),
              Paragraph(PC["how_to_intro"], sBODY), Spacer(1,2*mm)]
    for title, body in [
        (PC["rule1_title"], PC["rule1_body"]),
        (PC["rule2_title"], PC["rule2_body"]),
        (PC["rule3_title"], PC["rule3_body"]),
    ]:
        story.append(Paragraph(f"<b>{title}</b>  {body}", sBODY))
    story += [Spacer(1,4*mm), HintBox(PC["save_tip"]), PageBreak()]

    # TOC
    story += [Spacer(1,8*mm), Paragraph("Contents", sTOC_T), pink_hr(), Spacer(1,4*mm)]
    toc = [
        ("01", "Brand Foundation", "The context prompt to paste at the start of every session."),
        ("02", "Instagram: Product Content", "Drop announcements, product features, launch posts."),
        ("03", "Instagram: Lifestyle & Between Drops", "Mood content, BTS, community posts."),
        ("04", "Instagram: Stories & Engagement", "Polls, questions, DM bait, Story sequences."),
        ("05", "Email Marketing", "Welcome sequence (3 emails), drop announcements."),
        ("06", "Product Descriptions", "For site listings, Instagram shop, and DM responses."),
        ("07", "Customer DMs & FAQ", "Templates for the questions that come in every week."),
        ("08", "AI Visuals", "Midjourney and Flux prompts calibrated to your aesthetic."),
    ]
    for num, title, desc in toc:
        row = Table([[
            Paragraph(f"<b><font color='#FF2D8A'>{num}</font></b>", S("tn", fontName="Helvetica-Bold", fontSize=10)),
            Paragraph(f"<b>{title}</b>  <font size='8' color='#8A7A84'>{desc}</font>", sTOC_I)
        ]], colWidths=[16*mm, W-43*mm-16*mm])
        row.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),
            ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
            ('BOTTOMPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),0)]))
        story += [row, hr()]
    story.append(PageBreak())

    # SECTION 01: BRAND FOUNDATION
    for fl in sec_div(1, "Brand\nFoundation", "Paste this at the start of every AI session. It sets the foundation for every other prompt."): story.append(fl)
    story += [Spacer(1,8*mm), Paragraph("Brand Context Block", sH1), pink_hr(),
              Paragraph(PC["brand_context_intro"], sBODY), Spacer(1,4*mm),
              entry("01", "BRAND FOUNDATION", "At the start of every new chat session",
                "You are a copywriter and creative strategist for Angry Dollz, a UK-based brand "
                "selling bikinis, pole dance and aerial activewear, and bodybuilding stage wear.\n\n"
                "Brand personality: Y2K-inspired, alternative, confident, slightly edgy. "
                "Strong visual identity, loyal niche audience.\n\n"
                "Audience: Women who train hard (pole, aerial, bodybuilding, fitness), have a strong personal "
                "aesthetic, and want nothing to do with generic sportswear. Age roughly 20-35.\n\n"
                "Tone: Direct, fierce, no filler, no corporate language. Short sentences. Confident. "
                "Sometimes playful, never cutesy.\n\n"
                "Brand colours: Hot pink, black, chrome. Aesthetic: Y2K, alternative, performance art.\n\n"
                "Founder: Danielle runs the brand personally. Custom orders are a core offering. "
                "The brand voice sometimes uses first person.\n\n"
                "Keep all outputs consistent with this context unless told otherwise.",
                hint="Save this as a 'system prompt' in Claude, or as a pinned note in ChatGPT. "
                    "You won't need to paste it again until you start a new session."),
              PageBreak()]

    # SECTION 02: PRODUCT CONTENT
    for fl in sec_div(2, "Instagram\nProduct Content", "Drop announcements, product features, launch content. The core of your Instagram."): story.append(fl)
    story += [Spacer(1,8*mm), Paragraph("Instagram: Product Posts", sH1), pink_hr(),
              entry("02", "INSTAGRAM: PRODUCT DROP", "When launching a new product or collection",
                "Write 3 caption options for an Instagram post announcing [product name]. "
                "The post shows [describe the image: model wearing it, flat lay, etc.].\n\n"
                "Each caption: hook under 10 words (no 'introducing' or 'we're excited'), "
                "2-3 lines of body copy, CTA (link in bio, DM to order), 5-7 hashtags.\n\n"
                "One fierce option, one slightly softer, one playful.",
                hint="For the hook: think about what the buyer feels, not what the product is. "
                    "'Your pole bag was getting jealous' beats 'New grip gloves available now.'"),
              entry("03", "INSTAGRAM: PRODUCT FEATURE", "When highlighting a specific detail or quality",
                "Write a caption for a close-up shot of [product name] showing [specific detail: material, hardware, stitching].\n\n"
                "Tone: 'this is why the quality matters' without being boring about it. Confident. Under 80 words. "
                "Include 4-5 hashtags.",
                hint="Detail shots work well as Reels. Consider pairing with a 5-second video zoom."),
              entry("04", "INSTAGRAM: CUSTOM ORDER PROMO", "To drive DMs for custom orders",
                "Write a caption encouraging custom orders for Angry Dollz. "
                "Mention that [what you can customise: colour, sizing, design].\n\n"
                "Tone: exclusive, personal. Frame it as the better choice. "
                "Clear DM CTA. Under 100 words. 5 hashtags.",
                hint="Try: 'Tell me what you want and I'll make it happen' or 'DM the word CUSTOM to start.'"),
              PageBreak()]

    # SECTION 03: LIFESTYLE
    for fl in sec_div(3, "Instagram\nBetween Drops", "The content that keeps you visible and builds the tribe between launches."): story.append(fl)
    story += [Spacer(1,8*mm), Paragraph("Instagram: Lifestyle Content", sH1), pink_hr(),
              Paragraph(PC["lifestyle_intro"], sBODY), Spacer(1,3*mm),
              entry("05", "INSTAGRAM: BEHIND THE SCENES", "For process, making-of, or founder content",
                "Write a caption for a behind-the-scenes post. The image shows: [describe briefly].\n\n"
                "Tone: insider, personal, real. Like a text to a friend who's also a customer. "
                "Under 70 words. Optional: end with a question to drive comments. 4-5 hashtags.",
                hint="BTS content with a small honest moment tends to outperform polished posts. "
                    "Tell the AI if there's a funny or real detail to include."),
              entry("06", "INSTAGRAM: COMMUNITY REPOST", "When reposting a customer wearing Angry Dollz",
                "Write a caption for a repost of a customer photo showing [product name]. Handle: [@ handle].\n\n"
                "Tone: proud, genuine. Say something specific about the look or energy, not just 'love seeing "
                "our pieces on you'. Under 60 words. Tag them. 4 hashtags.",
                hint="Ask the customer's permission before reposting. Screenshot their comment or DM as confirmation."),
              entry("07", "INSTAGRAM: MOOD POST", "For aesthetic posts with no product to sell",
                "Write a caption for a mood post: no product, just aesthetic. "
                "The image shows: [describe the vibe: colour palette, setting, feeling].\n\n"
                "Under 50 words. Poetic is fine. 4-5 hashtags that fit the aesthetic.",
                hint="Use community tags here: #polelife #aerialarts #alternativegirls. "
                    "These posts get saves and follows from new people discovering the brand."),
              entry("08", "INSTAGRAM: TRAINING MOTIVATION", "For the fitness side of the audience",
                "Write a short motivational caption for a training post (pole, aerial, bodybuilding, lifting). "
                "The image shows: [describe].\n\n"
                "Tone: real, not fitness-bro, not a generic gym quote. Acknowledge training is hard "
                "without being preachy. Under 60 words. 5 hashtags mixing fitness and alternative culture.",
                hint="Avoid: 'no days off', 'be the best version of yourself', grind culture language. "
                    "The Angry Dollz audience is past that."),
              PageBreak()]

    # SECTION 04: STORIES
    for fl in sec_div(4, "Instagram\nStories", "Fast, engaging, conversation-starting. Stories are where the relationship lives."): story.append(fl)
    story += [Spacer(1,8*mm), Paragraph("Instagram: Stories", sH1), pink_hr(),
              entry("09", "STORIES: POLL / QUESTION", "To drive engagement and algorithm signals",
                "Give me 5 Instagram Story poll ideas for Angry Dollz. "
                "Each should feel like something Danielle would actually ask, not a brand survey.\n\n"
                "Themes: sizing debates, training style, aesthetic preferences, upcoming product decisions. "
                "Each option under 30 characters.",
                hint="Polls that feel like personal decisions outperform market research questions. "
                    "'Which colourway should I make next?' beats 'What product do you want us to add?'"),
              entry("10", "STORIES: DROP COUNTDOWN", "In the 48 hours before a new product launches",
                "Write a 3-Story sequence for the 48 hours before [product name] launches. "
                "Story 1: teaser (no reveal). Story 2: closer hint (24 hours out). Story 3: launch.\n\n"
                "Each Story: text overlay under 15 words, suggested sticker (countdown timer, poll, question box). "
                "Tone builds from mysterious to excited.",
                hint="Add a countdown sticker to Story 3. Instagram notifies followers when it hits zero."),
              entry("11", "STORIES: DM BAIT", "To fill your DMs with warm leads",
                "Write 3 Story text options designed to get people to DM Angry Dollz. "
                "Context: [what you want them to DM about: sizing, custom, waitlist].\n\n"
                "Each option: personal, low-barrier. No 'click here', no 'fill out the form'. "
                "Just: here's a reason to talk to me, here's exactly what to say.",
                hint="'DM me the word [X] and I'll send you...' outperforms 'DM for more info'. "
                    "Give them the exact word to type."),
              PageBreak()]

    # SECTION 05: EMAIL
    for fl in sec_div(5, "Email\nMarketing", "The welcome sequence and drop campaign templates."): story.append(fl)
    story += [Spacer(1,8*mm), Paragraph("Email: Full Sequence", sH1), pink_hr(),
              Paragraph(PC["email_intro"], sBODY), Spacer(1,3*mm),
              entry("12", "EMAIL: WELCOME 1 OF 3", "Sent immediately when someone joins the list",
                "Write welcome email 1 of 3 for Angry Dollz. "
                "The subscriber signed up for early drop access and 10% off their first order.\n\n"
                "Include: subject line, personal welcome from Danielle, what to expect (early access, BTS, no spam), "
                "discount code [CODE], one soft CTA. Tone: warm, like a text from the founder. Under 180 words.",
                hint="Subject lines that work: '[first name], welcome to the circle' or a short statement "
                    "that reads nothing like a promo email."),
              entry("13", "EMAIL: WELCOME 2 OF 3", "Sent 2-3 days after Email 1",
                "Write welcome email 2 of 3 for Angry Dollz. The subscriber has been on the list 3 days.\n\n"
                "This email: introduces the brand story in 2-3 sentences (personal, not corporate), "
                "mentions the custom order option, includes one soft nudge on discount code [CODE]. "
                "Tone: getting-to-know-you. Under 150 words.",
                hint="Mentioning custom orders early filters for your best customers."),
              entry("14", "EMAIL: WELCOME 3 OF 3", "Sent 5-7 days after Email 1",
                "Write welcome email 3 of 3 for Angry Dollz. The subscriber has been on the list about a week.\n\n"
                "Make the discount expiry feel real (7 days left, no pressure), preview what's coming next, "
                "invite them to reply with questions or custom enquiries. "
                "End with a genuine sign-off from Danielle. Under 140 words.",
                hint="Email 3 reply rates are typically the highest in a welcome sequence. "
                    "A reply from a new subscriber is worth responding to personally."),
              entry("15", "EMAIL: DROP ANNOUNCEMENT", "For any product launch",
                "Write a launch email for [product name] dropping on [date].\n\n"
                "Subject line: urgent, not gimmicky. 2-3 lines on the product. "
                "Early access note for email subscribers. Clear CTA button text.\n\n"
                "Tone: excited but not desperate. Like texting your most loyal customers. Under 160 words.",
                hint="Best send times: Tuesday-Thursday, 10am or 7pm UK."),
              PageBreak()]

    # SECTION 06: PRODUCT DESCRIPTIONS
    for fl in sec_div(6, "Product\nDescriptions", "For your Wix shop, Instagram shop, and DM responses."): story.append(fl)
    story += [Spacer(1,8*mm), Paragraph("Product Descriptions", sH1), pink_hr(),
              entry("16", "PRODUCT: STANDARD DESCRIPTION", "For any listing on your site or shop",
                "Write a product description for: [product name].\n\n"
                "Include: [material/fabric], [available sizes], [key features], [best use: pole, stage, beach].\n\n"
                "Structure: opening line with attitude (not just facts), 2 feature bullets, "
                "one sizing note, one care instruction.\n\n"
                "Tone: confident, buyer-focused. Under 90 words.",
                hint="Feature bullets should explain why it matters. 'Adjustable straps that actually stay in place "
                    "mid-set' beats 'adjustable straps'."),
              entry("17", "PRODUCT: CUSTOM ORDER PAGE", "For the custom order page or DM process description",
                "Write the custom order page copy for Angry Dollz.\n\n"
                "Cover: what can be customised, how to order, approximate lead time, why custom is worth it.\n\n"
                "Tone: exclusive and personal. Like a craftsperson explaining their process. Under 150 words.",
                hint="Lead with the feeling, then the logistics. 'Made for you, not a shelf' beats a list of options."),
              PageBreak()]

    # SECTION 07: DMs & FAQ
    for fl in sec_div(7, "Customer DMs\n& FAQ", "The answers that are always the same. Set them up once."): story.append(fl)
    story += [Spacer(1,8*mm), Paragraph("DM & FAQ Templates", sH1), pink_hr(),
              Paragraph(PC["faq_intro"], sBODY), Spacer(1,3*mm),
              entry("18", "FAQ: SIZING", "For every 'what size should I order?' DM",
                "Write 3 sizing FAQ responses for Angry Dollz:\n"
                "One for someone who usually wears [UK/US size].\n"
                "One for someone who's between sizes.\n"
                "One for a custom size enquiry.\n\n"
                "Each: human (not policy-ish), ask 1 clarifying question if needed, under 3 sentences.",
                hint="Save the most common response as an Instagram Quick Reply under Settings."),
              entry("19", "FAQ: RETURNS / EXCHANGES", "For return or exchange questions",
                "Write 2 returns/exchange responses:\n"
                "One for a customer asking about returns policy before buying.\n"
                "One for a customer who bought and wants to exchange.\n\n"
                "Tone: direct and fair. Under 3 sentences each.\n"
                "Note: add your actual returns policy before using."),
              entry("20", "FAQ: SHIPPING & DELIVERY", "For delivery timeline questions",
                "Write a DM template for shipping questions. Include: standard UK delivery [X days], "
                "international delivery [X days], one line about tracking.\n\n"
                "Short and human. Under 60 words."),
              entry("21", "FAQ: CUSTOM ORDER PROCESS", "For 'how does custom work?' DMs",
                "Write a DM template explaining the Angry Dollz custom order process. "
                "Cover: how to start, what info is needed (sizing, colours, occasion), lead time, payment.\n\n"
                "Tone: excited to work with them. Under 100 words.",
                hint="Respond to custom enquiries personally when you can. Use this as a starting point."),
              PageBreak()]

    # SECTION 08: AI VISUALS
    for fl in sec_div(8, "AI Visual\nPrompts", "Midjourney and Flux prompts calibrated to the Angry Dollz aesthetic."): story.append(fl)
    story += [Spacer(1,8*mm), Paragraph("AI Visuals: Brand-Tuned Prompts", sH1), pink_hr(),
              Paragraph(PC["visuals_intro"], sBODY), Spacer(1,3*mm),
              entry("22", "AI VISUAL: PRODUCT MOOD", "Atmospheric product content without a shooting day",
                "Close-up shot of [describe product] in hot pink and black colourway, "
                "studio lighting with chrome reflections, Y2K aesthetic, editorial fashion photography, "
                "sharp focus on fabric detail, dark background, high contrast, "
                "alternative fashion brand campaign --ar 4:5 --style raw --stylize 80",
                hint="Change --ar 4:5 to --ar 1:1 for square or --ar 9:16 for Stories."),
              entry("23", "AI VISUAL: LIFESTYLE EDITORIAL", "Aspirational lifestyle content",
                "Editorial photography of a woman in [describe: pole dance wear, stage wear], "
                "alternative fashion aesthetic, Y2K inspired, hot pink accents, black background, "
                "chrome metallic details, confident pose, professional studio lighting, "
                "high fashion editorial style adapted for alternative subculture "
                "--ar 4:5 --style raw --stylize 100",
                hint="Describe the energy and aesthetic rather than a specific person."),
              entry("24", "AI VISUAL: FLAT LAY", "Minimal product shots and shop listings",
                "Flat lay product shot of [describe item] on a matte black surface, "
                "styled with chrome accessories and hot pink elements, "
                "overhead shot, studio lighting, clean and editorial, "
                "Y2K alternative fashion aesthetic, no people "
                "--ar 1:1 --style raw",
                hint="Flat lays convert well on Instagram Shop and website listings."),
              entry("25", "AI VISUAL: PERFORMANCE / MOVEMENT", "Aerial, pole, or bodybuilding content",
                "Action shot of an aerial or pole artist in performance, "
                "wearing high-fashion activewear in black and hot pink, "
                "dramatic studio lighting with chrome reflections, "
                "movement blur on limbs, sharp focus on costume, "
                "alternative aesthetic, performance art photography, "
                "dark atmospheric background --ar 4:5 --style raw --stylize 90",
                hint="Tag relevant community accounts when posting. These tend to get strong saves from the pole community."),
              PageBreak()]

    # CLOSING
    story += [Spacer(1,15*mm), Paragraph("That's the Pack", sH1), pink_hr(),
              Paragraph(PC["closing_p1"], sBODY),
              Spacer(1,4*mm), HintBox(PC["closing_tip"]),
              Spacer(1,8*mm), HRFlowable(color=HOT_PINK,thickness=1,width="100%"),
              Spacer(1,4*mm),
              Paragraph("Florian Dierckx  ·  AI & Growth Consultant  ·  dierckx.florian@gmail.com", sFOOT),
              Paragraph("Prepared for Danielle / Angry Dollz  ·  June 2026  ·  All prompts written for this brand.", sFOOT)]

    return story

def main():
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    doc = SimpleDocTemplate(OUTPUT, pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm, topMargin=18*mm, bottomMargin=18*mm)
    doc.build(build(), onFirstPage=page_template, onLaterPages=page_template)
    from pypdf import PdfReader
    n = len(PdfReader(OUTPUT).pages)
    print(f"Prompt Pack v2: {n} pages -> {OUTPUT}")

main()
