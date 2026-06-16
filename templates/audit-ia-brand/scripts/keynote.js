const pptxgen = require("pptxgenjs");

// ── PALETTE ───────────────────────────────────────────────────────────────────
const C = {
  black:     "0A0A0A",
  darkBg:    "110810",
  cardBg:    "1C1020",
  pink:      "FF2D8A",
  deepPink:  "C4005D",
  chrome:    "D0D5E8",
  white:     "FFFFFF",
  offWhite:  "F0EAF4",
  midGrey:   "8A7A84",
  lightGrey: "C8BEC5",
  cream:     "FFF0F7",
};

// ── HELPERS ───────────────────────────────────────────────────────────────────
const makeShadow = () => ({ type: "outer", color: "000000", blur: 8, offset: 3, angle: 45, opacity: 0.18 });

function darkSlide(slide) {
  slide.background = { color: C.darkBg };
}

function addEyebrow(slide, text, x, y, w = 4) {
  slide.addText(text.toUpperCase(), {
    x, y, w, h: 0.22,
    fontSize: 8, bold: true, color: C.pink,
    charSpacing: 3, margin: 0,
  });
}

function addTitle(slide, text, x, y, w, h, color = C.white, size = 36) {
  slide.addText(text, {
    x, y, w, h,
    fontSize: size, bold: true, color,
    fontFace: "Cambria", margin: 0, valign: "top",
  });
}

function addBody(slide, text, x, y, w, h, color = C.lightGrey, size = 13) {
  slide.addText(text, {
    x, y, w, h,
    fontSize: size, color,
    fontFace: "Calibri", margin: 0, valign: "top",
    wrap: true,
  });
}

function addPinkCard(slide, x, y, w, h, title, body, titleSize = 13) {
  // Card with pink top band
  slide.addShape("rect", {
    x, y, w, h,
    fill: { color: C.cardBg },
    line: { color: C.pink, width: 0.5 },
    shadow: makeShadow(),
  });
  slide.addShape("rect", {
    x, y, w, h: 0.06,
    fill: { color: C.pink },
    line: { color: C.pink, width: 0 },
  });
  slide.addText(title, {
    x: x + 0.15, y: y + 0.12, w: w - 0.3, h: 0.28,
    fontSize: titleSize, bold: true, color: C.white,
    fontFace: "Cambria", margin: 0,
  });
  if (body) {
    slide.addText(body, {
      x: x + 0.15, y: y + 0.44, w: w - 0.3, h: h - 0.55,
      fontSize: 11, color: C.lightGrey,
      fontFace: "Calibri", margin: 0, valign: "top", wrap: true,
    });
  }
}

function addPinkStat(slide, x, y, w, h, number, label) {
  slide.addShape("roundRect", {
    x, y, w, h,
    fill: { color: C.cardBg },
    line: { color: C.pink, width: 1 },
    rectRadius: 0.05,
    shadow: makeShadow(),
  });
  slide.addText(number, {
    x, y: y + 0.08, w, h: h * 0.55,
    fontSize: 32, bold: true, color: C.pink,
    fontFace: "Cambria", align: "center", margin: 0,
  });
  slide.addText(label, {
    x, y: y + h * 0.6, w, h: h * 0.35,
    fontSize: 10, color: C.lightGrey,
    fontFace: "Calibri", align: "center", margin: 0, wrap: true,
  });
}

function addBulletList(slide, items, x, y, w, h, color = C.lightGrey) {
  const textArr = items.map((item, i) => ([
    { text: "→  ", options: { color: C.pink, bold: true } },
    { text: item, options: { color, breakLine: i < items.length - 1 } },
  ])).flat();
  slide.addText(textArr, {
    x, y, w, h,
    fontSize: 12, fontFace: "Calibri",
    margin: 0, valign: "top", paraSpaceAfter: 6,
  });
}

function addPageNum(slide, n) {
  slide.addText(`${n}`, {
    x: 9.5, y: 5.35, w: 0.35, h: 0.2,
    fontSize: 8, color: C.midGrey, align: "right", margin: 0,
  });
}

function pinkDivider(slide, x, y, w = 1.2) {
  slide.addShape("rect", {
    x, y, w, h: 0.03,
    fill: { color: C.pink }, line: { color: C.pink, width: 0 },
  });
}

// ── BUILD ─────────────────────────────────────────────────────────────────────
async function build() {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  pres.title  = "Angry Dollz × AI — Consultation Call";
  pres.author = "Florian Dierckx";

  // ── SLIDE 01: COVER ─────────────────────────────────────────────────────────
  {
    const s = pres.addSlide();
    darkSlide(s);

    // Large background "AD" monogram — subtle
    s.addText("AD", {
      x: 5.5, y: -0.3, w: 5, h: 5,
      fontSize: 220, bold: true, color: C.pink,
      fontFace: "Cambria", align: "center", transparency: 88, margin: 0,
    });

    // Pink accent line
    s.addShape("rect", { x: 0.55, y: 1.2, w: 0.04, h: 3.2, fill: { color: C.pink }, line: { color: C.pink, width: 0 } });

    s.addText("ANGRY DOLLZ", {
      x: 0.75, y: 1.2, w: 7, h: 0.5,
      fontSize: 13, bold: true, color: C.pink,
      charSpacing: 5, fontFace: "Calibri", margin: 0,
    });
    s.addText("AI Growth Strategy", {
      x: 0.75, y: 1.75, w: 8, h: 1.2,
      fontSize: 54, bold: true, color: C.white,
      fontFace: "Cambria", margin: 0,
    });
    s.addText("Consultation Call  ·  June 2026", {
      x: 0.75, y: 3.0, w: 6, h: 0.4,
      fontSize: 14, color: C.midGrey,
      fontFace: "Calibri", margin: 0,
    });

    pinkDivider(s, 0.75, 3.55, 3);

    s.addText("Prepared by Florian Dierckx  ·  AI & Growth Consultant", {
      x: 0.75, y: 3.72, w: 7, h: 0.3,
      fontSize: 11, color: C.midGrey, fontFace: "Calibri", margin: 0,
    });
  }

  // ── SLIDE 02: AGENDA ────────────────────────────────────────────────────────
  {
    const s = pres.addSlide();
    darkSlide(s);
    addPageNum(s, 2);

    addEyebrow(s, "Set the Agenda", 0.5, 0.35);
    addTitle(s, "How We Use This Hour", 0.5, 0.62, 6, 0.9);
    pinkDivider(s, 0.5, 1.55);

    const agenda = [
      ["00:00 – 05:00", "Set the agenda", "Align on the goal for this session."],
      ["00:05 – 00:30", "Discovery", "Your brand, your challenges, your current tools — I listen."],
      ["00:30 – 00:55", "AI Opportunities", "Observations + concrete recommendations, calibrated to what you just told me."],
      ["00:55 – 01:00", "Next steps", "Agreed actions, timeline, and next meeting scheduled before we hang up."],
    ];

    agenda.forEach(([time, title, desc], i) => {
      const y = 1.72 + i * 0.93;
      s.addShape("roundRect", {
        x: 0.5, y, w: 9, h: 0.82,
        fill: { color: C.cardBg }, line: { color: C.pink, width: 0.3 }, rectRadius: 0.06,
      });
      s.addText(time, {
        x: 1.05, y: y + 0.15, w: 1.5, h: 0.25,
        fontSize: 9, color: C.pink, bold: true, fontFace: "Calibri", margin: 0,
      });
      s.addText(title, {
        x: 2.6, y: y + 0.1, w: 3, h: 0.28,
        fontSize: 13, color: C.white, bold: true, fontFace: "Cambria", margin: 0,
      });
      s.addText(desc, {
        x: 2.6, y: y + 0.42, w: 6.7, h: 0.28,
        fontSize: 11, color: C.lightGrey, fontFace: "Calibri", margin: 0,
      });
      // Number circle
      s.addShape("ellipse", {
        x: 0.55, y: y + 0.22, w: 0.38, h: 0.38,
        fill: { color: C.pink }, line: { color: C.pink, width: 0 },
      });
      s.addText(`${i + 1}`, {
        x: 0.55, y: y + 0.22, w: 0.38, h: 0.38,
        fontSize: 11, bold: true, color: C.white,
        fontFace: "Calibri", align: "center", valign: "middle", margin: 0,
      });
    });

    s.addNotes("Set the agenda dès le départ. Dis-lui exactement comment tu veux utiliser l'heure. Ça professionnalise et évite les débordements.");
  }

  // ── SLIDE 03: DISCOVERY INTRO ───────────────────────────────────────────────
  {
    const s = pres.addSlide();
    darkSlide(s);
    addPageNum(s, 3);

    addEyebrow(s, "Discovery Phase", 0.5, 0.35);
    addTitle(s, "Before the Recommendations\nCome the Right Questions", 0.5, 0.62, 7, 1.4);
    pinkDivider(s, 0.5, 2.1);

    addBody(s,
      "Everything I'll show you in the next section was built from what I observed about Angry Dollz. But observations have limits. The next 25 minutes are yours — I want to understand what's actually happening inside the business before I tell you what I think.",
      0.5, 2.25, 6.5, 1.0, C.lightGrey, 13);

    // 5 dimensions grid
    const dims = [
      { label: "Content", desc: "Time, volume, what's working" },
      { label: "Audience", desc: "Who's buying, who's engaging" },
      { label: "Conversion", desc: "Site, DMs, drop revenue" },
      { label: "Operations", desc: "Tools, time, what's painful" },
      { label: "Vision", desc: "Where you want to go in 6 months" },
    ];

    dims.forEach((d, i) => {
      const x = 0.5 + i * 1.82;
      s.addShape("roundRect", {
        x, y: 3.45, w: 1.65, h: 1.6,
        fill: { color: i === 0 ? "2A0E1E" : C.cardBg },
        line: { color: C.pink, width: i === 0 ? 1 : 0.3 },
        rectRadius: 0.07,
      });
      s.addShape("ellipse", {
        x: x + 0.62, y: 3.6, w: 0.4, h: 0.4,
        fill: { color: C.pink }, line: { color: C.pink, width: 0 },
      });
      s.addText(`${i + 1}`, {
        x: x + 0.62, y: 3.6, w: 0.4, h: 0.4,
        fontSize: 12, bold: true, color: C.white,
        align: "center", valign: "middle", margin: 0, fontFace: "Calibri",
      });
      s.addText(d.label, {
        x: x + 0.1, y: 4.12, w: 1.45, h: 0.28,
        fontSize: 12, bold: true, color: C.white,
        align: "center", fontFace: "Cambria", margin: 0,
      });
      s.addText(d.desc, {
        x: x + 0.1, y: 4.44, w: 1.45, h: 0.48,
        fontSize: 9.5, color: C.midGrey,
        align: "center", fontFace: "Calibri", margin: 0, wrap: true,
      });
    });

    s.addNotes("Intro de la phase discovery. Montre cette slide, explique que tu as préparé des observations mais que tu veux d'abord écouter. Les 5 dimensions te servent de guide pour couvrir tous les sujets.");
  }

  // ── SLIDE 04: DISCOVERY — QUESTIONS ────────────────────────────────────────
  {
    const s = pres.addSlide();
    darkSlide(s);
    addPageNum(s, 4);

    addEyebrow(s, "Discovery — Audit Questions", 0.5, 0.35);
    addTitle(s, "25 Minutes of Listening", 0.5, 0.62, 6, 0.7);
    pinkDivider(s, 0.5, 1.35);

    const qs = [
      ["Content & Time", "How many hours a week goes to content right now? What takes the most time?"],
      ["Instagram", "Which posts actually perform for you? What do you post when there's no drop?"],
      ["Email", "Do you have an email list? If yes — what do you do with it? If no — why not yet?"],
      ["DMs", "What are the top 5 questions you get in DMs every week? How long does that take?"],
      ["AI today", "You use ChatGPT — what for exactly? What frustrated you about it?"],
      ["Revenue", "What does a drop look like in revenue terms? What channels drive the most orders?"],
      ["Website", "How do people find your Wix site? Do you know your conversion rate at all?"],
      ["Pain point", "If you could fix one thing about how you run the brand this week — what is it?"],
    ];

    // Two columns
    qs.forEach(([cat, q], i) => {
      const col = i < 4 ? 0 : 1;
      const row = i % 4;
      const x = 0.5 + col * 4.8;
      const y = 1.55 + row * 0.93;

      s.addShape("roundRect", {
        x, y, w: 4.55, h: 0.82,
        fill: { color: C.cardBg }, line: { color: "2A1520", width: 0.5 }, rectRadius: 0.06,
      });
      s.addText(cat.toUpperCase(), {
        x: x + 0.12, y: y + 0.1, w: 4.2, h: 0.2,
        fontSize: 7.5, bold: true, color: C.pink, charSpacing: 2,
        fontFace: "Calibri", margin: 0,
      });
      s.addText(q, {
        x: x + 0.12, y: y + 0.33, w: 4.2, h: 0.42,
        fontSize: 10.5, color: C.lightGrey, fontFace: "Calibri",
        margin: 0, valign: "top", wrap: true,
      });
    });

    s.addNotes("Ces questions sont tes guides — tu n'as pas besoin de toutes les poser dans l'ordre. L'important: laisser Danielle parler, reformuler ('ce que j'entends c'est que...'), noter les chiffres et les douleurs.");
  }

  // ── SLIDE 05: SECTION BREAK — OBSERVATIONS ─────────────────────────────────
  {
    const s = pres.addSlide();
    s.background = { color: C.pink };

    s.addText("Part 02", {
      x: 0.6, y: 1.4, w: 8, h: 0.5,
      fontSize: 14, bold: true, color: "FFFFFF",
      charSpacing: 4, fontFace: "Calibri", margin: 0, transparency: 30,
    });
    s.addText("What I\nObserved", {
      x: 0.6, y: 1.9, w: 9, h: 2.2,
      fontSize: 72, bold: true, color: C.white,
      fontFace: "Cambria", margin: 0,
    });
    s.addText("Brand audit · Instagram · Website · Email · Operations", {
      x: 0.6, y: 4.2, w: 9, h: 0.4,
      fontSize: 13, color: "FFB3D9", fontFace: "Calibri", margin: 0,
    });
  }

  // ── SLIDE 06: BRAND SCORECARD ───────────────────────────────────────────────
  {
    const s = pres.addSlide();
    darkSlide(s);
    addPageNum(s, 6);

    addEyebrow(s, "Brand Audit", 0.5, 0.35);
    addTitle(s, "Where Angry Dollz Stands Today", 0.5, 0.62, 7, 0.7);
    pinkDivider(s, 0.5, 1.35);

    const scores = [
      ["Visual Identity & Aesthetic", 8, "Strong, specific, recognizable. The Y2K aesthetic attracts a real tribe."],
      ["Instagram Consistency",       5, "Drops go hard. The in-between weeks are thin. Algorithm punishes this."],
      ["Website Conversion",          4, "Homepage doesn't answer 'what is this?' fast enough."],
      ["Email List & Retention",      2, "No owned audience yet. Biggest untapped channel."],
      ["AI Readiness",                4, "ChatGPT occasionally. No system behind it yet."],
    ];

    scores.forEach(([label, score, note], i) => {
      const y = 1.65 + i * 0.73;
      s.addText(label, {
        x: 0.5, y, w: 3.2, h: 0.28,
        fontSize: 12, bold: true, color: C.white, fontFace: "Cambria", margin: 0, valign: "middle",
      });
      // Bar bg
      s.addShape("roundRect", {
        x: 3.8, y: y + 0.04, w: 4.2, h: 0.2,
        fill: { color: "2A1520" }, line: { color: "2A1520", width: 0 }, rectRadius: 0.04,
      });
      // Bar fill
      const barColor = score >= 7 ? C.pink : score >= 5 ? "F4A41C" : "884455";
      s.addShape("roundRect", {
        x: 3.8, y: y + 0.04, w: 4.2 * (score / 10), h: 0.2,
        fill: { color: barColor }, line: { color: barColor, width: 0 }, rectRadius: 0.04,
      });
      s.addText(`${score}/10`, {
        x: 8.1, y, w: 0.7, h: 0.28,
        fontSize: 11, bold: true, color: barColor, align: "right",
        fontFace: "Calibri", margin: 0, valign: "middle",
      });
      s.addText(note, {
        x: 0.5, y: y + 0.3, w: 8.3, h: 0.3,
        fontSize: 9.5, color: C.midGrey, fontFace: "Calibri", margin: 0,
      });
    });

    s.addNotes("Utilise ce slide pour poser le contexte de tes observations. Laisse Danielle réagir — elle peut challenger les scores. C'est normal et ça ouvre la conversation.");
  }

  // ── SLIDE 07: WHAT'S WORKING ────────────────────────────────────────────────
  {
    const s = pres.addSlide();
    darkSlide(s);
    addPageNum(s, 7);

    addEyebrow(s, "Observations", 0.5, 0.35);
    addTitle(s, "What's Working in Your Favour", 0.5, 0.62, 7, 0.7);
    pinkDivider(s, 0.5, 1.35);

    const strengths = [
      ["Specific aesthetic = real tribe",
       "The Y2K alternative positioning is specific enough to attract and hold a niche. Most brands are too afraid of this. It's the foundation everything else builds on."],
      ["Custom orders = high-trust signal",
       "Customers who buy custom are choosing you, not a price. That relationship is more valuable than a transaction. It also means your conversion rate on engaged followers is probably higher than average."],
      ["Product coherence",
       "Bikinis + pole + aerial + bodybuilding = one specific woman with a specific lifestyle. That coherence is rare and makes targeting, content, and community much simpler."],
      ["Founder-driven brand",
       "Danielle is the brand. That's a genuine edge in 2026 — people buy from people they feel connected to. AI can amplify this but should never replace it."],
    ];

    strengths.forEach(([title, body], i) => {
      const col = i % 2;
      const row = Math.floor(i / 2);
      const x = 0.5 + col * 4.8;
      const y = 1.55 + row * 1.75;
      addPinkCard(s, x, y, 4.55, 1.55, title, body);
    });

    s.addNotes("Commence toujours par les forces. Ça crée de la confiance et montre que tu as vraiment regardé la marque, pas juste fait un audit générique.");
  }

  // ── SLIDE 08: THE 4 PAIN POINTS ─────────────────────────────────────────────
  {
    const s = pres.addSlide();
    darkSlide(s);
    addPageNum(s, 8);

    addEyebrow(s, "Observations", 0.5, 0.35);
    addTitle(s, "The 4 Pain Points", 0.5, 0.62, 7, 0.7);
    pinkDivider(s, 0.5, 1.35);

    const pains = [
      ["01", "Content creation", "Every post starts from scratch. No system = same effort every week."],
      ["02", "Invisible between drops", "No email list = no owned audience. Algorithm as only channel."],
      ["03", "Calendar gaps", "Shootings cover drops. The weeks between them have nothing."],
      ["04", "FAQ flooding DMs", "Same questions, every week. 2-3 hours on logistics instead of customers."],
    ];

    pains.forEach(([num, title, body], i) => {
      const col = i % 2;
      const row = Math.floor(i / 2);
      const x = 0.5 + col * 4.8;
      const y = 1.55 + row * 1.75;

      s.addShape("roundRect", {
        x, y, w: 4.55, h: 1.55,
        fill: { color: C.cardBg }, line: { color: "441025", width: 0.5 }, rectRadius: 0.07,
        shadow: makeShadow(),
      });
      s.addText(num, {
        x: x + 0.15, y: y + 0.12, w: 0.55, h: 0.55,
        fontSize: 28, bold: true, color: C.pink,
        fontFace: "Cambria", align: "center", valign: "middle", margin: 0,
      });
      s.addText(title, {
        x: x + 0.75, y: y + 0.15, w: 3.6, h: 0.35,
        fontSize: 13, bold: true, color: C.white,
        fontFace: "Cambria", margin: 0, valign: "middle",
      });
      s.addText(body, {
        x: x + 0.15, y: y + 0.65, w: 4.2, h: 0.75,
        fontSize: 11, color: C.lightGrey,
        fontFace: "Calibri", margin: 0, valign: "top", wrap: true,
      });
    });

    s.addNotes("Présente les pain points comme des observations, pas des accusations. 'Ce que j'ai observé de l'extérieur...' — puis laisse-la confirmer ou corriger en temps réel.");
  }

  // ── SLIDE 09: SECTION BREAK — OPPORTUNITIES ────────────────────────────────
  {
    const s = pres.addSlide();
    s.background = { color: C.darkBg };

    // Full-width pink band at bottom
    s.addShape("rect", {
      x: 0, y: 4.8, w: 10, h: 0.825,
      fill: { color: C.pink }, line: { color: C.pink, width: 0 },
    });

    s.addText("Part 03", {
      x: 0.6, y: 1.0, w: 8, h: 0.4,
      fontSize: 12, bold: true, color: C.pink,
      charSpacing: 4, fontFace: "Calibri", margin: 0,
    });
    s.addText("AI Opportunities\nFor Angry Dollz", {
      x: 0.6, y: 1.45, w: 9, h: 2.5,
      fontSize: 58, bold: true, color: C.white,
      fontFace: "Cambria", margin: 0,
    });
    s.addText("4 systems · 4 weeks · built around your voice", {
      x: 0.6, y: 4.87, w: 9, h: 0.4,
      fontSize: 14, bold: true, color: C.darkBg,
      fontFace: "Calibri", margin: 0,
    });
  }

  // ── SLIDE 10: OPPORTUNITY 01 — CAPTIONS ─────────────────────────────────────
  {
    const s = pres.addSlide();
    darkSlide(s);
    addPageNum(s, 10);

    addEyebrow(s, "Opportunity 01", 0.5, 0.35);
    addTitle(s, "Caption System", 0.5, 0.62, 6, 0.7, C.white, 32);
    pinkDivider(s, 0.5, 1.35);

    // Problem → Solution → Impact layout
    const cols = [
      { label: "THE PROBLEM", color: "441025", border: "882244",
        body: "Every caption starts from scratch. Thinking, typing, second-guessing, rewriting. Multiply that by 5 posts a week and it's 3-4 hours gone before a single pixel is posted." },
      { label: "THE SYSTEM", color: "0A1E14", border: C.pink,
        body: "One master prompt, saved on your phone. You paste it, describe the post in 2 sentences, and get 3 caption options in under 2 minutes. You pick one, adjust 20%, post." },
      { label: "THE IMPACT", color: "1A0A1E", border: "8822AA",
        body: "20 minutes for a full week of captions instead of 4 hours. Time saved: ~3-4 hours/week. That's the first thing AI buys back for you." },
    ];

    cols.forEach(({ label, color, border, body }, i) => {
      const x = 0.5 + i * 3.08;
      s.addShape("roundRect", {
        x, y: 1.55, w: 2.9, h: 2.8,
        fill: { color }, line: { color: border, width: 1 }, rectRadius: 0.07,
        shadow: makeShadow(),
      });
      s.addText(label, {
        x: x + 0.15, y: 1.68, w: 2.6, h: 0.25,
        fontSize: 8, bold: true, color: C.pink,
        charSpacing: 2, fontFace: "Calibri", margin: 0,
      });
      s.addText(body, {
        x: x + 0.15, y: 2.0, w: 2.6, h: 2.2,
        fontSize: 11, color: C.lightGrey,
        fontFace: "Calibri", margin: 0, valign: "top", wrap: true,
      });
    });

    // Stat
    s.addShape("roundRect", {
      x: 0.5, y: 4.5, w: 9, h: 0.85,
      fill: { color: C.cardBg }, line: { color: C.pink, width: 0.5 }, rectRadius: 0.06,
    });
    s.addText("→  Your Prompt Pack already includes the Caption Master Prompt — copy it, paste it, you're done.", {
      x: 0.75, y: 4.62, w: 8.5, h: 0.5,
      fontSize: 12, color: C.white, fontFace: "Calibri", margin: 0, valign: "middle",
    });

    s.addNotes("Montre un exemple concret si tu peux. La question à poser: 'Combien de temps tu passes sur une légende aujourd'hui?' — puis présente le système.");
  }

  // ── SLIDE 11: OPPORTUNITY 02 — EMAIL LIST ───────────────────────────────────
  {
    const s = pres.addSlide();
    darkSlide(s);
    addPageNum(s, 11);

    addEyebrow(s, "Opportunity 02", 0.5, 0.35);
    addTitle(s, "Email List — The Channel\nYou Actually Own", 0.5, 0.62, 7, 1.0, C.white, 30);
    pinkDivider(s, 0.5, 1.65);

    addBody(s, "Instagram is rented land. The algorithm controls who sees you. Email is different — you own that list. When you send, they receive.", 0.5, 1.8, 6.5, 0.6);

    // 3 stats
    addPinkStat(s, 0.5,  2.55, 2.8, 1.4, "30-45%", "avg open rate\nniche fashion list");
    addPinkStat(s, 3.6,  2.55, 2.8, 1.4, "£3,375", "per drop at 500 subs\n15% conversion · £45 AOV");
    addPinkStat(s, 6.7,  2.55, 2.8, 1.4, "1 hour", "to set up MailerLite\nand the welcome sequence");

    // How
    s.addShape("roundRect", {
      x: 0.5, y: 4.1, w: 9, h: 1.2,
      fill: { color: C.cardBg }, line: { color: "441025", width: 0.5 }, rectRadius: 0.06,
    });
    s.addText("HOW IT WORKS", {
      x: 0.7, y: 4.2, w: 3, h: 0.25,
      fontSize: 8, bold: true, color: C.pink, charSpacing: 2, fontFace: "Calibri", margin: 0,
    });
    s.addText([
      { text: "Pop-up on Wix  ", options: { color: C.white, bold: true } },
      { text: "→  ", options: { color: C.pink } },
      { text: "Welcome sequence (3 emails, AI-drafted, runs automatically)  ", options: { color: C.lightGrey } },
      { text: "→  ", options: { color: C.pink } },
      { text: "Drop campaigns  ", options: { color: C.lightGrey } },
      { text: "→  ", options: { color: C.pink } },
      { text: "Revenue from your existing audience", options: { color: C.lightGrey } },
    ], {
      x: 0.7, y: 4.5, w: 8.5, h: 0.6,
      fontSize: 11.5, fontFace: "Calibri", margin: 0, valign: "middle",
    });

    s.addNotes("La question à poser avant cette slide: 'Tu as une liste email?' Si oui, qu'est-ce qu'elle en fait. Si non, pourquoi pas encore. Adapte ton pitch en fonction de la réponse.");
  }

  // ── SLIDE 12: OPPORTUNITY 03 — AI VISUALS ──────────────────────────────────
  {
    const s = pres.addSlide();
    darkSlide(s);
    addPageNum(s, 12);

    addEyebrow(s, "Opportunity 03", 0.5, 0.35);
    addTitle(s, "AI Visuals — Filling the\nCalendar Between Drops", 0.5, 0.62, 7, 1.0, C.white, 30);
    pinkDivider(s, 0.5, 1.65);

    addBody(s, "Shootings are the content backbone. But the algorithm rewards 5+ posts per week. AI visuals fill the gaps — they don't replace your photography, they support the schedule.", 0.5, 1.82, 6.5, 0.7);

    // Visual cards
    const types = [
      { title: "Product Mood", desc: "Close-up, studio lighting, chrome reflections. Dark bg. Looks editorial.", tag: "Midjourney" },
      { title: "Lifestyle Editorial", desc: "Energy shot, alternative aesthetic. Shows the world the brand lives in.", tag: "Midjourney" },
      { title: "Flat Lay", desc: "Clean overhead, matte black surface, pink accents. Works for shop listings.", tag: "Flux (free)" },
      { title: "Performance / Movement", desc: "Action blur on limbs, sharp on costume. Resonates with the pole community.", tag: "Midjourney" },
    ];

    types.forEach(({ title, desc, tag }, i) => {
      const x = 0.5 + i * 2.32;
      s.addShape("roundRect", {
        x, y: 2.7, w: 2.15, h: 2.65,
        fill: { color: C.cardBg }, line: { color: "441025", width: 0.3 }, rectRadius: 0.07,
      });
      s.addShape("roundRect", {
        x: x + 0.1, y: 2.82, w: 1.95, h: 0.22,
        fill: { color: C.pink }, line: { color: C.pink, width: 0 }, rectRadius: 0.04,
      });
      s.addText(tag, {
        x: x + 0.1, y: 2.82, w: 1.95, h: 0.22,
        fontSize: 8, bold: true, color: C.white, align: "center", valign: "middle",
        fontFace: "Calibri", margin: 0,
      });
      s.addText(title, {
        x: x + 0.1, y: 3.12, w: 1.95, h: 0.32,
        fontSize: 12, bold: true, color: C.white,
        fontFace: "Cambria", margin: 0,
      });
      s.addText(desc, {
        x: x + 0.1, y: 3.5, w: 1.95, h: 0.75,
        fontSize: 10, color: C.midGrey,
        fontFace: "Calibri", margin: 0, wrap: true,
      });
    });

    s.addShape("roundRect", {
      x: 0.5, y: 5.1, w: 9, h: 0.35,
      fill: { color: "1A0A1E" }, line: { color: C.pink, width: 0.3 }, rectRadius: 0.04,
    });
    s.addText("4 Midjourney prompt templates calibrated to your palette are included in the Prompt Pack.", {
      x: 0.7, y: 5.16, w: 8.5, h: 0.22,
      fontSize: 10.5, color: C.lightGrey, fontFace: "Calibri", margin: 0, valign: "middle",
    });

    s.addNotes("Précise clairement: ces visuels ne remplacent PAS les shootings. Ils remplissent le calendrier entre les drops. L'authenticité de ses photos reste le point fort.");
  }

  // ── SLIDE 13: OPPORTUNITY 04 — FAQ AUTOMATION ──────────────────────────────
  {
    const s = pres.addSlide();
    darkSlide(s);
    addPageNum(s, 13);

    addEyebrow(s, "Opportunity 04", 0.5, 0.35);
    addTitle(s, "Stop Answering the\nSame Question Twice", 0.5, 0.62, 7, 1.0, C.white, 30);
    pinkDivider(s, 0.5, 1.65);

    // FAQ examples
    const faqs = ["What size should I order?", "Do you do custom?", "How long does delivery take?", "Can I return it?", "What's it made from?"];
    s.addText("Questions that come in every week:", {
      x: 0.5, y: 1.85, w: 5, h: 0.3,
      fontSize: 11, color: C.midGrey, fontFace: "Calibri", margin: 0,
    });

    faqs.forEach((q, i) => {
      s.addShape("roundRect", {
        x: 0.5 + i * 1.82, y: 2.25, w: 1.7, h: 0.7,
        fill: { color: C.cardBg }, line: { color: "441025", width: 0.3 }, rectRadius: 0.05,
      });
      s.addText(q, {
        x: 0.6 + i * 1.82, y: 2.3, w: 1.5, h: 0.6,
        fontSize: 10, color: C.lightGrey, fontFace: "Calibri",
        margin: 0, valign: "middle", align: "center", wrap: true,
      });
    });

    s.addText("→", {
      x: 4.55, y: 3.15, w: 1, h: 0.4,
      fontSize: 24, bold: true, color: C.pink, align: "center", margin: 0, fontFace: "Calibri",
    });

    // Solutions
    const sols = [
      { title: "Wix Chat", desc: "Built into your dashboard. Free. Set up FAQ answers once, handles them forever.", time: "30 min setup" },
      { title: "Story Highlight", desc: "Pin a 'FAQ' highlight with saved Stories answering each question. Zero cost.", time: "1 hour" },
      { title: "Quick Replies", desc: "Instagram's built-in feature. Save your 5 most common answers as shortcuts.", time: "10 min" },
    ];

    sols.forEach(({ title, desc, time }, i) => {
      const x = 0.5 + i * 3.08;
      s.addShape("roundRect", {
        x, y: 3.65, w: 2.9, h: 1.65,
        fill: { color: C.cardBg }, line: { color: C.pink, width: 0.5 }, rectRadius: 0.07,
      });
      s.addShape("roundRect", {
        x: x + 1.9, y: 3.72, w: 0.85, h: 0.22,
        fill: { color: C.pink }, line: { color: C.pink, width: 0 }, rectRadius: 0.04,
      });
      s.addText(time, {
        x: x + 1.9, y: 3.72, w: 0.85, h: 0.22,
        fontSize: 7.5, bold: true, color: C.white, align: "center", valign: "middle",
        fontFace: "Calibri", margin: 0,
      });
      s.addText(title, {
        x: x + 0.15, y: 3.72, w: 1.8, h: 0.28,
        fontSize: 13, bold: true, color: C.white, fontFace: "Cambria", margin: 0,
      });
      s.addText(desc, {
        x: x + 0.15, y: 4.08, w: 2.6, h: 1.0,
        fontSize: 10.5, color: C.lightGrey, fontFace: "Calibri",
        margin: 0, valign: "top", wrap: true,
      });
    });

    s.addNotes("Demande-lui combien de DMs répétitifs par semaine. 60-70% de réduction après setup d'un système FAQ basique — chiffre issu des retours de fondateurs e-commerce.");
  }

  // ── SLIDE 14: THE AI STACK ──────────────────────────────────────────────────
  {
    const s = pres.addSlide();
    darkSlide(s);
    addPageNum(s, 14);

    addEyebrow(s, "Recommended Stack", 0.5, 0.35);
    addTitle(s, "4 Tools. 4 Problems Solved.", 0.5, 0.62, 7, 0.7, C.white, 32);
    pinkDivider(s, 0.5, 1.35);

    const tools = [
      { name: "ChatGPT / Claude", use: "Captions · Emails · Product descriptions · DM drafts",
        cost: "Free / $20/mo", cat: "CONTENT & COPY", col: C.pink },
      { name: "Midjourney / Flux", use: "AI visuals for in-between content",
        cost: "Flux free · MJ $10/mo", cat: "VISUALS", col: "8844CC" },
      { name: "MailerLite", use: "Email list · Welcome sequence · Drop campaigns",
        cost: "Free to 1,000 subs", cat: "EMAIL", col: "22AA88" },
      { name: "Wix Chat / Tidio", use: "FAQ automation on your site",
        cost: "Both have free tiers", cat: "SITE", col: "4488CC" },
    ];

    tools.forEach(({ name, use, cost, cat, col }, i) => {
      const y = 1.55 + i * 0.95;
      s.addShape("roundRect", {
        x: 0.5, y, w: 9, h: 0.84,
        fill: { color: C.cardBg }, line: { color: "221020", width: 0.3 }, rectRadius: 0.06,
      });
      // Color dot
      s.addShape("ellipse", {
        x: 0.65, y: y + 0.22, w: 0.4, h: 0.4,
        fill: { color: col }, line: { color: col, width: 0 },
      });
      s.addText(cat, {
        x: 1.2, y: y + 0.12, w: 2, h: 0.22,
        fontSize: 7.5, bold: true, color: col, charSpacing: 2, fontFace: "Calibri", margin: 0,
      });
      s.addText(name, {
        x: 1.2, y: y + 0.36, w: 3.5, h: 0.3,
        fontSize: 13, bold: true, color: C.white, fontFace: "Cambria", margin: 0,
      });
      s.addText(use, {
        x: 4.9, y: y + 0.14, w: 3.2, h: 0.56,
        fontSize: 10.5, color: C.midGrey, fontFace: "Calibri", margin: 0, valign: "middle", wrap: true,
      });
      s.addShape("roundRect", {
        x: 8.2, y: y + 0.2, w: 1.15, h: 0.44,
        fill: { color: "1A0F14" }, line: { color: col, width: 0.5 }, rectRadius: 0.04,
      });
      s.addText(cost, {
        x: 8.2, y: y + 0.2, w: 1.15, h: 0.44,
        fontSize: 8.5, color: C.lightGrey, align: "center", valign: "middle",
        fontFace: "Calibri", margin: 0, wrap: true,
      });
    });

    s.addNotes("Valide avec elle ce qu'elle connaît déjà de cette liste. Ajuste en temps réel si elle a déjà essayé certains outils.");
  }

  // ── SLIDE 15: SECTION BREAK — ACTION PLAN ──────────────────────────────────
  {
    const s = pres.addSlide();
    s.background = { color: C.darkBg };

    s.addShape("rect", {
      x: 0, y: 0, w: 10, h: 0.06,
      fill: { color: C.pink }, line: { color: C.pink, width: 0 },
    });

    s.addText("Part 04", {
      x: 0.6, y: 1.3, w: 8, h: 0.4,
      fontSize: 12, bold: true, color: C.pink,
      charSpacing: 4, fontFace: "Calibri", margin: 0,
    });
    s.addText("The Plan", {
      x: 0.6, y: 1.75, w: 9, h: 1.8,
      fontSize: 88, bold: true, color: C.white,
      fontFace: "Cambria", margin: 0,
    });
    s.addText("30 days · 90 days · one thing at a time", {
      x: 0.6, y: 3.65, w: 7, h: 0.4,
      fontSize: 14, color: C.midGrey, fontFace: "Calibri", margin: 0,
    });

    // decorative number
    s.addText("30", {
      x: 7.0, y: 1.0, w: 3.5, h: 4,
      fontSize: 280, bold: true, color: C.pink,
      fontFace: "Cambria", align: "center", transparency: 90, margin: 0,
    });
  }

  // ── SLIDE 16: 30-DAY PLAN ───────────────────────────────────────────────────
  {
    const s = pres.addSlide();
    darkSlide(s);
    addPageNum(s, 16);

    addEyebrow(s, "Action Plan", 0.5, 0.35);
    addTitle(s, "30 Days · One System Per Week", 0.5, 0.62, 7, 0.7, C.white, 30);
    pinkDivider(s, 0.5, 1.35);

    const weeks = [
      { week: "Week 1", title: "Captions System",   days: "Days 1–7",   action: "Set up ChatGPT or Claude. Copy the Caption prompt. Draft 5 captions. Save the adjusted version.", result: "20 min/week instead of 4 hours" },
      { week: "Week 2", title: "Email List Launch", days: "Days 8–14",  action: "MailerLite setup. Add Wix pop-up. Copy the 3-email welcome sequence. Activate.", result: "List collecting subscribers automatically" },
      { week: "Week 3", title: "AI Visuals Test",   days: "Days 15–21", action: "Sign up for Flux (free). Generate 10 images with the prompt templates. Pick 3-4. Schedule them.", result: "Content bank without a shooting day" },
      { week: "Week 4", title: "FAQ Automation",    days: "Days 22–30", action: "List your 10 most common DM questions. Set up Wix Chat or a Story FAQ highlight.", result: "Repetitive DM volume drops 60-70%" },
    ];

    weeks.forEach(({ week, title, days, action, result }, i) => {
      const y = 1.55 + i * 0.97;
      // Row bg
      s.addShape("roundRect", {
        x: 0.5, y, w: 9, h: 0.86,
        fill: { color: i % 2 === 0 ? C.cardBg : "160D18" },
        line: { color: "221020", width: 0.3 }, rectRadius: 0.05,
      });
      // Week pill
      s.addShape("roundRect", {
        x: 0.62, y: y + 0.22, w: 0.85, h: 0.3,
        fill: { color: C.pink }, line: { color: C.pink, width: 0 }, rectRadius: 0.04,
      });
      s.addText(week, {
        x: 0.62, y: y + 0.22, w: 0.85, h: 0.3,
        fontSize: 8.5, bold: true, color: C.white, align: "center", valign: "middle",
        fontFace: "Calibri", margin: 0,
      });
      s.addText(`${days}  ·  ${title}`, {
        x: 1.6, y: y + 0.12, w: 3.5, h: 0.3,
        fontSize: 13, bold: true, color: C.white, fontFace: "Cambria", margin: 0,
      });
      s.addText(action, {
        x: 1.6, y: y + 0.44, w: 4.8, h: 0.35,
        fontSize: 10, color: C.midGrey, fontFace: "Calibri", margin: 0, wrap: true,
      });
      s.addShape("roundRect", {
        x: 6.6, y: y + 0.18, w: 2.7, h: 0.5,
        fill: { color: "1A0A1E" }, line: { color: "441030", width: 0.5 }, rectRadius: 0.04,
      });
      s.addText(`→  ${result}`, {
        x: 6.7, y: y + 0.18, w: 2.5, h: 0.5,
        fontSize: 9.5, color: C.lightGrey, fontFace: "Calibri",
        margin: 0, valign: "middle", wrap: true,
      });
    });

    s.addNotes("Insiste sur le fait que chaque semaine a UN focus. La tentation de tout faire en même temps est réelle — mais c'est comme ça que rien ne se termine.");
  }

  // ── SLIDE 17: 90-DAY VISION ─────────────────────────────────────────────────
  {
    const s = pres.addSlide();
    darkSlide(s);
    addPageNum(s, 17);

    addEyebrow(s, "Vision", 0.5, 0.35);
    addTitle(s, "Where This Goes in 90 Days", 0.5, 0.62, 7, 0.7, C.white, 30);
    pinkDivider(s, 0.5, 1.35);

    const months = [
      { m: "Month 1", title: "Systems are live",
        body: "4 foundations running: captions, email list, AI visuals, FAQ. Posting 5+ times per week without full days. Email list at 100-300 subs (existing audience). Repetitive DMs down." },
      { m: "Month 2", title: "First email revenue",
        body: "First drop campaign hits the list. At 200 subs and 30% conversion on a £45 AOV, that's £2,700 from email alone. Instagram reach improving 20-40% from consistent posting." },
      { m: "Month 3", title: "Compounding",
        body: "List at 300-600 subs, growing passively. 2 email campaigns per month. 8-12 hours/week reclaimed from admin, repetitive content, and FAQ replies. That time goes to custom orders, shootings, or rest." },
    ];

    months.forEach(({ m, title, body }, i) => {
      const x = 0.5 + i * 3.08;
      s.addShape("roundRect", {
        x, y: 1.55, w: 2.9, h: 2.9,
        fill: { color: C.cardBg }, line: { color: "441025", width: 0.5 }, rectRadius: 0.07,
        shadow: makeShadow(),
      });
      s.addShape("rect", { x, y: 1.55, w: 2.9, h: 0.06, fill: { color: C.pink }, line: { color: C.pink, width: 0 } });
      s.addText(m.toUpperCase(), {
        x: x + 0.15, y: 1.68, w: 2.6, h: 0.2,
        fontSize: 8, bold: true, color: C.pink, charSpacing: 2, fontFace: "Calibri", margin: 0,
      });
      s.addText(title, {
        x: x + 0.15, y: 1.95, w: 2.6, h: 0.4,
        fontSize: 14, bold: true, color: C.white, fontFace: "Cambria", margin: 0,
      });
      s.addText(body, {
        x: x + 0.15, y: 2.42, w: 2.6, h: 1.9,
        fontSize: 10.5, color: C.lightGrey, fontFace: "Calibri",
        margin: 0, valign: "top", wrap: true,
      });
    });

    // Key number
    s.addShape("roundRect", {
      x: 0.5, y: 4.6, w: 9, h: 0.78,
      fill: { color: "1A0414" }, line: { color: C.pink, width: 1 }, rectRadius: 0.07,
    });
    s.addText("£3,375 per drop from email alone — at 500 engaged subscribers, 15% conversion, £45 AOV. Zero extra ad spend.", {
      x: 0.75, y: 4.72, w: 8.5, h: 0.52,
      fontSize: 12, color: C.white, fontFace: "Calibri", margin: 0, valign: "middle",
    });

    s.addNotes("Ce slide est là pour projeter la vision. Ajuste les chiffres en temps réel selon ce que Danielle t'a dit sur son AOV et sa taille d'audience actuelle.");
  }

  // ── SLIDE 18: THE PRINCIPLE ─────────────────────────────────────────────────
  {
    const s = pres.addSlide();
    darkSlide(s);
    addPageNum(s, 18);

    addEyebrow(s, "The Principle", 0.5, 0.35);
    addTitle(s, "What AI Takes.\nWhat Stays Yours.", 0.5, 0.62, 7, 1.2, C.white, 34);
    pinkDivider(s, 0.5, 1.85);

    // Two columns: AI takes vs Danielle keeps
    const keeps = ["Your shooting days", "Your relationship with customers", "Custom order consultations", "Creative direction", "Your voice and your story"];
    const takes = ["Captions (20 min/week)", "Email sequences (runs automatically)", "In-between visual content", "FAQ and sizing replies", "Product description drafts"];

    // Left — stays yours
    s.addShape("roundRect", {
      x: 0.5, y: 2.05, w: 4.2, h: 3.3,
      fill: { color: "0A1E14" }, line: { color: "22AA66", width: 1 }, rectRadius: 0.08,
      shadow: makeShadow(),
    });
    s.addText("STAYS WITH DANIELLE", {
      x: 0.7, y: 2.18, w: 3.8, h: 0.25,
      fontSize: 8, bold: true, color: "22AA66", charSpacing: 2, fontFace: "Calibri", margin: 0,
    });
    keeps.forEach((item, i) => {
      s.addText([
        { text: "✓  ", options: { color: "22AA66", bold: true } },
        { text: item, options: { color: C.white } },
      ], {
        x: 0.7, y: 2.52 + i * 0.5, w: 3.8, h: 0.38,
        fontSize: 12, fontFace: "Calibri", margin: 0,
      });
    });

    // Right — AI takes
    s.addShape("roundRect", {
      x: 5.3, y: 2.05, w: 4.2, h: 3.3,
      fill: { color: C.cardBg }, line: { color: C.pink, width: 1 }, rectRadius: 0.08,
      shadow: makeShadow(),
    });
    s.addText("AI HANDLES", {
      x: 5.5, y: 2.18, w: 3.8, h: 0.25,
      fontSize: 8, bold: true, color: C.pink, charSpacing: 2, fontFace: "Calibri", margin: 0,
    });
    takes.forEach((item, i) => {
      s.addText([
        { text: "→  ", options: { color: C.pink, bold: true } },
        { text: item, options: { color: C.lightGrey } },
      ], {
        x: 5.5, y: 2.52 + i * 0.5, w: 3.8, h: 0.38,
        fontSize: 12, fontFace: "Calibri", margin: 0,
      });
    });

    s.addNotes("Ce slide répond à la vraie peur derrière 'est-ce que l'IA va changer mon brand?' La réponse: non, si c'est bien fait. Le tout c'est de savoir quoi lui donner et quoi garder.");
  }

  // ── SLIDE 19: THE DELIVERABLES ──────────────────────────────────────────────
  {
    const s = pres.addSlide();
    darkSlide(s);
    addPageNum(s, 19);

    addEyebrow(s, "What You're Getting", 0.5, 0.35);
    addTitle(s, "Your AI Starter Kit", 0.5, 0.62, 7, 0.7, C.white, 32);
    pinkDivider(s, 0.5, 1.35);

    const deliverables = [
      { title: "AI Brand Audit",        desc: "32-page analysis: scores, pain points, tools, 30-day plan, 90-day vision, and how to learn AI at your pace.", tag: "PDF · After this call" },
      { title: "AI Prompt Pack",        desc: "25 copy-paste prompts written for Angry Dollz: Instagram, email, products, DMs, and AI visual generation.", tag: "PDF · After this call" },
      { title: "This Presentation",     desc: "The full deck for reference — observations, recommendations, and the plan laid out in one place.", tag: "PPTX · After this call" },
    ];

    deliverables.forEach(({ title, desc, tag }, i) => {
      const y = 1.6 + i * 1.3;
      s.addShape("roundRect", {
        x: 0.5, y, w: 9, h: 1.15,
        fill: { color: C.cardBg }, line: { color: C.pink, width: 0.5 }, rectRadius: 0.07,
        shadow: makeShadow(),
      });
      s.addText(`0${i + 1}`, {
        x: 0.65, y: y + 0.28, w: 0.55, h: 0.55,
        fontSize: 26, bold: true, color: C.pink,
        fontFace: "Cambria", align: "center", valign: "middle", margin: 0,
      });
      s.addText(title, {
        x: 1.35, y: y + 0.12, w: 4.5, h: 0.35,
        fontSize: 15, bold: true, color: C.white, fontFace: "Cambria", margin: 0,
      });
      s.addText(desc, {
        x: 1.35, y: y + 0.5, w: 5.5, h: 0.5,
        fontSize: 10.5, color: C.lightGrey, fontFace: "Calibri",
        margin: 0, valign: "top", wrap: true,
      });
      s.addShape("roundRect", {
        x: 7.1, y: y + 0.38, w: 2.2, h: 0.35,
        fill: { color: "1A0A1E" }, line: { color: C.pink, width: 0.5 }, rectRadius: 0.04,
      });
      s.addText(tag, {
        x: 7.1, y: y + 0.38, w: 2.2, h: 0.35,
        fontSize: 9, color: C.pink, align: "center", valign: "middle",
        fontFace: "Calibri", margin: 0, bold: true,
      });
    });

    s.addNotes("Annonce les livrables avant de raccrocher. Ça donne de la valeur tangible au call et crée un ancrage pour le suivi.");
  }

  // ── SLIDE 20: SECTION BREAK — NEXT STEPS ───────────────────────────────────
  {
    const s = pres.addSlide();
    s.background = { color: C.pink };

    s.addText("Part 05", {
      x: 0.6, y: 1.3, w: 8, h: 0.4,
      fontSize: 12, bold: true, color: "FFFFFF",
      charSpacing: 4, fontFace: "Calibri", margin: 0, transparency: 30,
    });
    s.addText("Next\nSteps", {
      x: 0.6, y: 1.75, w: 9, h: 2.8,
      fontSize: 90, bold: true, color: C.white,
      fontFace: "Cambria", margin: 0,
    });
    s.addText("Agreed actions · Timeline · Next call booked before we hang up", {
      x: 0.6, y: 4.65, w: 9, h: 0.4,
      fontSize: 13, color: "FFB3D9", fontFace: "Calibri", margin: 0,
    });
  }

  // ── SLIDE 21: NEXT STEPS ────────────────────────────────────────────────────
  {
    const s = pres.addSlide();
    darkSlide(s);
    addPageNum(s, 21);

    addEyebrow(s, "Next Steps", 0.5, 0.35);
    addTitle(s, "What Happens After This Call", 0.5, 0.62, 7, 0.7, C.white, 32);
    pinkDivider(s, 0.5, 1.35);

    const steps = [
      { when: "Today", who: "Florian", action: "Send Audit PDF + Prompt Pack + this deck by email." },
      { when: "This week", who: "Danielle", action: "Set up the captions system. One afternoon. Prompt 01 in the pack." },
      { when: "End of week", who: "Danielle", action: "Feedback on the audit: what resonates, what needs adjusting, what's missing." },
      { when: "Week 2", who: "Danielle", action: "MailerLite setup + Wix pop-up live. Welcome sequence activated." },
      { when: "Next call", who: "Both", action: "Review first 2 weeks. Calibrate. Plan month 2. Schedule this before hanging up." },
    ];

    steps.forEach(({ when, who, action }, i) => {
      const y = 1.6 + i * 0.77;
      s.addShape("roundRect", {
        x: 0.5, y, w: 9, h: 0.66,
        fill: { color: i === 4 ? "1A0A1E" : C.cardBg },
        line: { color: i === 4 ? C.pink : "221020", width: i === 4 ? 1 : 0.3 },
        rectRadius: 0.05,
      });
      s.addShape("roundRect", {
        x: 0.62, y: y + 0.16, w: 1.1, h: 0.3,
        fill: { color: i === 4 ? C.pink : "2A1520" },
        line: { color: i === 4 ? C.pink : "441030", width: 0.5 },
        rectRadius: 0.04,
      });
      s.addText(when, {
        x: 0.62, y: y + 0.16, w: 1.1, h: 0.3,
        fontSize: 9, color: i === 4 ? C.white : C.pink, bold: true,
        align: "center", valign: "middle", fontFace: "Calibri", margin: 0,
      });
      s.addShape("roundRect", {
        x: 1.85, y: y + 0.16, w: 1.05, h: 0.3,
        fill: { color: "0A1A2A" }, line: { color: "224466", width: 0.5 }, rectRadius: 0.04,
      });
      s.addText(who, {
        x: 1.85, y: y + 0.16, w: 1.05, h: 0.3,
        fontSize: 9, color: "4499CC", bold: true,
        align: "center", valign: "middle", fontFace: "Calibri", margin: 0,
      });
      s.addText(action, {
        x: 3.05, y: y + 0.14, w: 6.3, h: 0.38,
        fontSize: 11.5, color: i === 4 ? C.white : C.lightGrey,
        fontFace: "Calibri", margin: 0, valign: "middle", bold: i === 4,
      });
    });

    s.addNotes("CRITIQUE: ne raccroche pas sans avoir fixé la prochaine date. 'Avant de se séparer, est-ce qu'on peut bloquer 30 minutes la semaine prochaine pour faire le point sur les premiers résultats?'");
  }

  // ── SLIDE 22: CLOSING ───────────────────────────────────────────────────────
  {
    const s = pres.addSlide();
    darkSlide(s);

    // Large BG text
    s.addText("AD", {
      x: 4, y: -0.5, w: 7, h: 7,
      fontSize: 280, bold: true, color: C.pink,
      fontFace: "Cambria", align: "center", transparency: 92, margin: 0,
    });

    s.addShape("rect", { x: 0.55, y: 1.4, w: 0.04, h: 2.5, fill: { color: C.pink }, line: { color: C.pink, width: 0 } });

    s.addText("ANGRY DOLLZ", {
      x: 0.75, y: 1.4, w: 7, h: 0.4,
      fontSize: 11, bold: true, color: C.pink,
      charSpacing: 5, fontFace: "Calibri", margin: 0,
    });
    s.addText("Let's build it.", {
      x: 0.75, y: 1.85, w: 8, h: 1.2,
      fontSize: 58, bold: true, color: C.white,
      fontFace: "Cambria", margin: 0,
    });

    pinkDivider(s, 0.75, 3.2, 2.5);

    s.addText("Florian Dierckx  ·  AI & Growth Consultant", {
      x: 0.75, y: 3.42, w: 6, h: 0.3,
      fontSize: 11, color: C.midGrey, fontFace: "Calibri", margin: 0,
    });
    s.addText("dierckx.florian@gmail.com", {
      x: 0.75, y: 3.76, w: 5, h: 0.3,
      fontSize: 11, color: C.pink, fontFace: "Calibri", margin: 0,
    });

    s.addNotes("Slide de clôture. Avant de la montrer: assure-toi que la prochaine date est dans le calendrier et que les livrables sont promis par email dans les 24h.");
  }

  // ── SAVE ──────────────────────────────────────────────────────────────────────
  const outPath = "/mnt/user-data/outputs/AngryDollz_Call_Keynote.pptx";
  await pres.writeFile({ fileName: outPath });
  console.log(`✓ Keynote saved: ${outPath}`);
}

build().catch(console.error);
