# YOU ARE NOT THE PROTAGONIST (VN ERROR ROUTE)
## Twine-Based Visual Novel Design Document

---

## STORY PREMISE

In a structured fantasy world governed by a narrative system, every person is assigned a role. There is always one protagonist—someone whose existence anchors fate itself.

But when the story begins, the protagonist is missing.

You, an unnamed background character, begin to experience system instability as reality attempts to force you into the protagonist role.

The world does not ask for your consent.

And the system does not accept “no.”

This is a story about resisting narrative identity, forming unstable bonds with characters who remember different versions of you, and deciding whether to accept, reject, or rewrite existence itself.

Light romance routes exist for emotional grounding, primarily with characters who are also “broken” by the system.

---

# ASSET STRUCTURE

- assets/image/characters/
- assets/image/backgrounds/
- assets/music/

---

# MAIN VARIABLES

- [OOMPH] = pixel dithering, anime cyberpunk lighting, soft glitch overlays, high detail sprite shading
- [ACCESSORIES_NOTEBOOK] = worn archive notebook with memory seals
- [ACCESSORIES_SWORD] = system-issued knight blade with glowing UI runes
- [SYSTEM_CORE_SYMBOL] = floating fragmented UI shard representing narrative authority

---

# PASSAGE LIST

---

## SCENE INTRO - TEXT 01

You wake up in a village that feels… slightly unfinished.

People walk past you without acknowledging your existence properly, as if you are a placeholder in their awareness.

Then you hear it.

A system notification that no one else reacts to:

> “ERROR: PROTAGONIST NOT FOUND. INITIATING SUBSTITUTE EVALUATION.”

You were never supposed to hear that.

### Choices:
- [[Ignore it and go to work->Scene Hub - Text 02]]
- [[Try to ask someone about the message->Scene Hub - Text 02]]
- [[Look for the source of the voice->Scene Library - Text 02]]

---

### PIXEL ART PROMPT - CHARACTER
assets/image/characters/player.png  
Pixel art anime-style young male protagonist, neutral expression, slightly confused posture, simple fantasy village clothing, soft cyber-glitch overlay, subtle UI distortion around eyes, neon highlights, dithering shadows, [OOMPH]

### PIXEL ART PROMPT - BACKGROUND
assets/image/backgrounds/village_day.png  
Fantasy village street, slightly incomplete architecture, soft cyber-fantasy lighting, floating UI fragments in sky, warm but unstable atmosphere, anime pixel art, dithering, [OOMPH]

---

## SCENE HUB - TEXT 02

The village behaves normally, but something is wrong.

A woman drops her basket. It freezes mid-air for a frame too long before falling.

A child repeats the same laugh twice, identically.

The world is buffering.

You feel it again—the system watching you.

### Choices:
- [[Talk to the Archivist nearby->Scene Archivist - Text 02]]
- [[Head to the knight barracks->Scene Knight - Text 02]]
- [[Search for “protagonist” in town records->Scene Library - Text 03]]

---

### PIXEL ART PROMPT - BACKGROUND
assets/image/backgrounds/village_hub.png  
Central fantasy town square with subtle glitch distortions, floating UI fragments, soft neon fantasy lighting, slightly repeated NPC patterns, anime pixel art dithering, [OOMPH]

---

## SCENE ARCHIVIST - TEXT 02

The Archivist looks up as you enter.

She pauses.

Then her expression changes—not surprise, but recognition of something inconsistent.

“You’re… not indexed correctly.”

She opens her notebook.

Every page is blank except your name, repeated in unstable ink.

### Choices:
- [[Ask what “indexed” means->Scene Archivist - Text 03]]
- [[Touch the notebook->Scene Archivist - Text 03]]
- [[Leave immediately->Scene Hub - Text 03]]

---

### PIXEL ART PROMPT - CHARACTER
assets/image/characters/lira_archivist.png  
Female archivist, calm expression, soft mysterious gaze, holding worn notebook [ACCESSORIES_NOTEBOOK], elegant fantasy robes with subtle tech-like seams, slightly glowing ink effects, anime pixel art, [OOMPH]

### PIXEL ART PROMPT - BACKGROUND
assets/image/backgrounds/archive_room.png  
Ancient library room with floating papers, soft neon magical lighting, shelves extending into darkness, subtle UI glitches in corners, anime pixel art dithering, [OOMPH]

---

## SCENE KNIGHT - TEXT 02

A knight stands alone in the training yard.

She is staring into space, unmoving.

Then suddenly—

Her eyes flicker like a corrupted interface.

“Directive received… protect protagonist…”

She looks directly at you.

“…but there is no designated target.”

### Choices:
- [[Tell her you don’t know what she means->Scene Knight - Text 03]]
- [[Ask her to join you->Scene Knight - Text 03]]
- [[Run away->Scene Hub - Text 03]]

---

### PIXEL ART PROMPT - CHARACTER
assets/image/characters/k0_knight.png  
Female knight, cyber-fantasy armor with glowing UI seams, holding [ACCESSORIES_SWORD], slightly glitching eyes, calm but unstable expression, anime pixel art shading, [OOMPH]

### PIXEL ART PROMPT - BACKGROUND
assets/image/backgrounds/barracks_yard.png  
Fantasy knight training yard with digital distortion in sky, floating UI fragments, soft neon sunset lighting, anime pixel art dithering, [OOMPH]

---

## SCENE LIBRARY - TEXT 03

The library is quiet.

Too quiet.

Books shift slightly when you look away.

One shelf collapses into static for half a second before reforming.

A single book floats down and lands in your hands.

Its title reads:

> “PROTAGONIST NOT FOUND: SUBSTITUTE PROTOCOL”

Inside: pages describing you doing things you have never done.

### Choices:
- [[Read further->Scene Library - Text 04]]
- [[Burn the book->Scene Ending Collapse - Text 01]]
- [[Take it to the Archivist->Scene Archivist - Text 04]]

---

### PIXEL ART PROMPT - BACKGROUND
assets/image/backgrounds/library_void.png  
Fantasy library with floating shelves, distorted reality edges, glowing book particles, cyber-magical atmosphere, anime pixel art dithering, [OOMPH]

---

## SCENE ENDING ACCEPTANCE - TEXT 01

You accept the role.

The world stabilizes instantly.

People smile at you with perfect synchronization.

The Archivist forgets her doubts.

The Knight salutes without hesitation.

Everything is correct.

Everything is clean.

You are the protagonist now.

But you cannot remember who you were before.

### ENDING: “STABLE NARRATIVE”

---

## SCENE ENDING COLLAPSE - TEXT 01

You reject the system.

The world begins to tear.

Dialogue boxes overlap.

Characters repeat broken lines.

The Archivist screams as her pages erase themselves.

The Knight dissolves into UI fragments.

The system voice tries one last time:

> “PLEASE ACCEPT ROLE FOR WORLD STABILITY”

You refuse.

Everything ends.

### ENDING: “UNWRITTEN WORLD”

---

## SCENE TRUE END - CO-AUTHORSHIP

You stop responding to the system entirely.

Instead, you speak to the characters as equals.

The system hesitates.

Then… pauses.

For the first time, no correction appears.

The world stops enforcing a single story.

Everyone remains imperfect.

But real.

### ENDING: “CO-AUTHORED EXISTENCE”

---

# OPTIONAL EXPANSION IDEAS

- Hidden “Save File NPCs” that remember previous playthroughs
- Romance routes that only unlock after system corruption thresholds
- Secret UI entity route (dating the Script Voice)
- True antagonist revealed as the “missing protagonist refusing to exist”
- Multi-route convergence ending where all timelines partially merge

---