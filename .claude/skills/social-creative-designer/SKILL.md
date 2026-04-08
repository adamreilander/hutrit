---
name: social-creative-designer
description: |
  Generates on-brand carousel slide sets and single social media graphics as PNG images for Hutrit and Hutrit Club, using the Nano Banana MCP (mcp__nanobanana__generate_image) for image generation.

  Trigger this skill whenever the user asks to:
  - Create a carousel, post set, slide set, or series of social graphics
  - Design or generate a post, visual, graphic, banner, or creative for Instagram, LinkedIn, Facebook, or any social platform
  - Make content visuals for a topic, tip, insight, or announcement
  - Produce a single static social image

  Even if the user just says "hazme un post sobre X", "crea un carrusel de Y", or "necesito un visual para Z" — trigger this skill immediately. Don't wait for the user to be more specific.
---

# Social Creative Designer — Hutrit

Generates on-brand PNG image sets for social media using Nano Banana. Reads the brand style guide at runtime to stay visually consistent without hardcoding design decisions.

---

## Defaults

| Parameter | Default | Options |
|-----------|---------|---------|
| Slides per set | 3 | Any number (user-specified) |
| Aspect ratio | 4:5 | 1:1, 3:4, 9:16, 4:5 |
| Platform | Instagram | LinkedIn, Facebook, others |
| Mode | Carousel (multi-slide) | Single static image |

---

## Step 1 — Load context before doing anything else

Read these two files before generating a single image:

1. **Brand context:** `_context/brand_verview.md`
2. **Visual style guide:** `_templates/social-creatives-hutrit-club/guia_estilo_hutrit_club_posts.md`

The style guide contains the full design system: colors, typography, layout rules, illustration direction, copy tone, and a ready-to-use base prompt (section 13). Everything you need to build accurate, on-brand prompts is there.

If either file is missing, tell the user before proceeding.

---

## Step 2 — Clarify the request (if needed)

If the user gave you a topic but didn't specify mode, number of slides, aspect ratio, or platform, assume the defaults and proceed. You don't need to ask — just declare what you're doing at the top of your response:

> "Generating a 3-slide Instagram carousel in 4:5 about [topic]…"

Only pause to ask if the user gave genuinely ambiguous instructions (e.g., "make something about remote work" with no other context).

---

## Step 3 — Plan the content

Design the narrative arc before writing prompts. Each slide has a distinct role:

### Carousel structure
- **Slide 1 — Hook:** Bold attention-stopping headline. Minimal text. Should make someone stop scrolling. Use a question, a surprising statement, or a direct promise. No more than 8 words on screen.
- **Middle slides — Value:** One insight, tip, or step per slide. A numbered circle (1, 2, 3…) in the upper area, the core message in 1–2 lines, a simple illustration below. One idea per slide — never two.
- **Final slide — CTA or takeaway:** Summarize or drive action. "Regístrate gratis", "Guarda este post", or a closing insight. Include the Hutrit Club branding.

### Single image structure
Same visual identity, single composition: hook headline + supporting line + illustration. No numbered elements. More editorial feel.

---

## Step 4 — Build the image prompts

For each slide, write a detailed prompt using the style guide's base prompt (section 13) as the foundation, then layer in slide-specific content.

### Base style instructions to include in every prompt

```
Vertical social media graphic, 4:5 format (1080x1350px). Corporate-minimalist and friendly style for a remote work brand. Very light warm background (#F3F3F1) with a subtle pattern of thin, monoline remote-work icons (laptop, calendar, wifi, message bubble, office chair, headphones, email envelope) in very light grayish-green at low opacity — these icons must not compete with the main message. Centered composition with generous white space and clear visual hierarchy. Clean, geometric sans-serif typography (Poppins or Montserrat style). Colors: dark teal (#005A5A) for main headings, bright green (#17A85B) for highlighted words or accents, dark gray (#5E5E5E) for subtitles. Friendly, modern digital illustration in the lower portion featuring a remote work or productivity scene, using soft greens, beige, and warm wood tones. Illustration should feel warm, clean, professional, and optimistic. Minimal text on image — prioritize visual clarity.
```

Then add slide-specific instructions:

**For Slide 1 (Hook):** Include the hook headline large and bold at center. State the exact text to render. Include the Hutrit Club logo text ("Hutrit" in dark teal, "Club" in bright green) at the top, small and centered.

**For middle slides:** Include a dark teal filled circle with a white number at the upper center. State the tip text (1–2 lines max). No logo needed unless requested.

**For the CTA slide:** Include a bold CTA line, a supporting line, and "Hutrit" + "Club" branding. Add a CTA button or pill shape with "REGÍSTRATE GRATIS" text in white on a bright green (#17A85B) rounded rectangle.

### Reference images for style conditioning

Pick 2–3 images from `_templates/social-creatives-hutrit-club/` to pass as `input_image_path_1`, `input_image_path_2` when calling Nano Banana. This gives the model visual anchors for the exact brand aesthetic. Choose images that are compositionally similar to the slide you're generating (cover → pick a cover, step slide → pick a step slide). Any images in that folder work — they're all the same style. Use low-numbered files (1.png–20.png) if unsure which to pick.

---

## Step 5 — Generate with Nano Banana

Call `mcp__nanobanana__generate_image` for each slide. Key parameters:

```
prompt: <your full slide prompt>
aspect_ratio: "4:5"  (or as requested)
input_image_path_1: "_templates/social-creatives-hutrit-club/1.png"
input_image_path_2: "_templates/social-creatives-hutrit-club/2.png"
output_path: "social/"
model_tier: "nb2"
resolution: "high"
negative_prompt: "dark background, photorealistic photo, cluttered layout, too much text, multiple columns of text, neon colors, gradients, stock photo, busy background"
```

Generate slides sequentially (one at a time, not in parallel) so each slide's result can inform the next if needed for consistency.

**If Nano Banana is unavailable:** Stop immediately and tell the user: "La generación de imágenes con Nano Banana no está disponible en este momento. Verifica que el MCP server esté activo y vuelve a intentarlo."

---

## Step 6 — Present and save

After all images are generated:

1. Show each slide inline so the user can see the full set immediately.
2. State the file path where each was saved (inside `social/`).
3. Give the user a short summary: what was generated, how many slides, and one line of creative direction used.

Name output files descriptively:
```
social/carousel-[topic-slug]-slide-1.png
social/carousel-[topic-slug]-slide-2.png
social/carousel-[topic-slug]-slide-3.png
```

For single images:
```
social/post-[topic-slug].png
```

---

## Tone and copy notes

When writing the text content that goes into the prompt, follow these rules from the brand style guide:

- Copy goes **directly to the point** — no preamble
- Hook formats that work: question connecting to a real problem, direct promise ("Haz esto durante 30 días"), actionable tip ("Organiza tu día antes de empezarlo")
- Highlighted words (rendered in bright green `#17A85B`) are 1–3 key words per slide, not full sentences
- Subtitles are in dark gray — they clarify, not repeat, the headline
- No paragraphs on slides — max 2 lines of body text per slide

---

## Platform adjustments

| Platform | Aspect ratio | Tone |
|----------|-------------|------|
| Instagram | 4:5 (default) | Energetic, direct, visual-first |
| LinkedIn | 4:5 or 1:1 | More professional, slightly more text |
| Facebook | 4:5 or 1:1 | Similar to Instagram |
| Story/Reel cover | 9:16 | Full-bleed, large text, minimal illustration |
| Square | 1:1 | Reduce text, center composition tightly |

For LinkedIn, you may increase subtitle text slightly and reduce illustration size to give more room for the insight. The color system and typography stay identical.

---

## Quick-start examples

**User:** "Crea un carrusel de 3 slides sobre cómo mejorar tu perfil para trabajo remoto"
→ Generate: Hook (¿Tu perfil no está atrayendo oportunidades remotas?) + 2 steps + CTA

**User:** "Hazme un post de Instagram sobre los errores al aplicar a vacantes"
→ Single static: Hook headline + supporting line + illustration scene

**User:** "Necesito 5 slides para LinkedIn sobre fit cultural en equipos remotos"
→ 5-slide LinkedIn carousel (4:5): Hook + 3 value slides + CTA, tone slightly more consultative
