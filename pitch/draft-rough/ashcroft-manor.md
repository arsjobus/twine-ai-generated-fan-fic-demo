# STORY PITCH — *Veil of Ashcroft Manor*
> **Setting:** Gothic Manor / Victorian England  
> **Tone:** Dark Fantasy  
> **Target Audience:** Male  
> **Spiciness:** SFW  
> **Engine:** Twine (Harlowe or Sugarcube)  
> **Scope:** Indie Solo Developer — ~25 passages, 3 endings

---

## LOGLINE

A disgraced occult investigator arrives at a cursed Victorian manor to audit a dead nobleman's estate — and finds himself ensnared in a century-old bargain between the living and the dead.

---

## STORY SUMMARY

You are **Edmund Voss**, a former member of the Crown's secret Department of Anomalous Affairs, stripped of rank after a botched exorcism that cost lives. You receive a letter from the estate of **Lord Aldric Ashcroft**, recently deceased under mysterious circumstances, requesting your expertise for a "routine audit."

Upon arriving at **Ashcroft Manor**, you discover the estate is still very much occupied — by the Lord's enigmatic ward **Seraphine**, a ghost-like woman who seems to know more than she admits; the manor's ancient groundskeeper **Mott**, who warns you to leave; and something else, something old and patient, that watches from the sealed East Wing.

Three paths unfold: uncover the truth and break the curse (True Ending), strike a bargain with the entity and survive at a cost (Dark Pact Ending), or flee — only to find the manor has followed you (Haunted Ending).

---

## CHARACTERS

### Edmund Voss (Player Character)
- Late 30s, lean, weathered face, sharp eyes ringed with fatigue
- Wears a long Victorian coat, carries a leather satchel of occult tools
- Perchance variables: `[EDMUND_COAT]`, `[EDMUND_SATCHEL]`

### Seraphine Ashcroft
- Mid 20s, pale, silver-streaked dark hair, always in mourning dress
- Carries a brass music box that plays on its own
- Perchance variables: `[SERAPHINE_DRESS]`, `[MUSIC_BOX]`

### Mott (Groundskeeper)
- Old, stocky, missing two fingers on his right hand, lantern always at his side
- Perchance variables: `[MOTT_LANTERN]`

### The Veil Entity (The Ashcroft Shade)
- Abstract: a silhouette within smoke, no fixed form, crown of antlers made of shadow
- Perchance variables: `[SHADE_FORM]`, `[SHADE_ANTLERS]`

---

## PERCHANCE GLOBAL VARIABLES

```
[OOMPH] = pixel-perfect anime, highly polished, vibrant yet balanced color palette, visual novel art style

[EDMUND_COAT] = long Victorian charcoal-grey coat with brass buttons, frayed cuffs, subtle dark lining, worn but distinguished

[EDMUND_SATCHEL] = weathered brown leather satchel, bulging with rolled papers, vials, and iron clasps

[SERAPHINE_DRESS] = full-length Victorian mourning dress in matte black silk, high collar trimmed with dark lace, small silver buttons

[MUSIC_BOX] = small brass music box with engraved floral patterns, lid slightly ajar, faint glow at the hinge

[MOTT_LANTERN] = worn iron lantern with cracked amber glass, warm orange flame, hung from a leather strap

[SHADE_FORM] = tall featureless dark silhouette, edges dissolving into black smoke, faint violet luminescence at the core

[SHADE_ANTLERS] = wide branching antlers formed from compressed shadow, tips fading to nothing, asymmetrical
```

---

## ASSET FOLDER STRUCTURE

```
assets/
  image/
    bg/
      manor-exterior-night.png
      entrance-hall.png
      library.png
      east-wing-door.png
      seraphine-chamber.png
      manor-grounds-fog.png
      void-space.png
    char/
      edmund/
        edmund-neutral.png
        edmund-suspicious.png
        edmund-determined.png
      seraphine/
        seraphine-neutral.png
        seraphine-sad.png
        seraphine-fearful.png
        seraphine-knowing.png
      mott/
        mott-warning.png
        mott-resigned.png
      shade/
        shade-distant.png
        shade-close.png
        shade-bargain.png
  music/
    theme-manor-ambient.mp3
    theme-tension.mp3
    theme-seraphine.mp3
    theme-shade.mp3
    theme-ending-true.mp3
    theme-ending-pact.mp3
    theme-ending-haunted.mp3
```

---

## PASSAGE MAP (Scene Flow)

```
[scene-intro] Scene Arrival
       │
       ▼
[scene-hub] Scene Manor Entrance  ◄──────────────────┐
       │                                              │
       ├──► [scene-library] Scene The Library         │
       │           │                                  │
       │           ├──► [scene-seraphine-secret]      │
       │           │    Scene The Secret              │
       │           │           │                      │
       │           │           └──► [scene-east-wing] │
       │           │                Scene East Wing   │
       │           │                      │           │
       │           └──► [scene-mott-warn]             │
       │                Scene Mott Warning ───────────┘
       │
       ├──► [scene-grounds] Scene The Grounds
       │           │
       │           └──► [scene-mott-warn]
       │
       └──► [scene-east-wing-door] Scene East Wing Door (locked)
                   │
                   └──► [scene-hub] (loop back)

[scene-east-wing] Scene East Wing
       │
       ├──► [scene-confrontation] Scene The Confrontation
       │           │
       │           ├──► [scene-ending-true] Scene True Ending
       │           ├──► [scene-ending-pact] Scene Dark Pact Ending
       │           └──► [scene-ending-haunted] Scene Haunted Ending
       │
       └──► [scene-hub] (retreat)
```

---

## PASSAGES

---

### `Scene Arrival`
**Tags:** `scene-intro`  
**Music:** `assets/music/theme-manor-ambient.mp3`  
**Background:** `assets/image/bg/manor-exterior-night.png`  
**Characters shown:** Edmund (neutral)

---

**Narrative:**

The hansom cab deposits you at the iron gates of Ashcroft Manor just as the last bruise of daylight drains from the sky. Rain has begun — not the honest downpour of a storm, but a fine, insidious mist that clings to your coat and refuses to drip.

You are Edmund Voss. Once, that name meant something in certain circles. Tonight it means: the only man willing to take this job.

The manor looms — four storeys of blackened stone, its peaked rooftines stabbing upward like accusations. Every window is dark except one: a single amber glow on the uppermost floor, third window from the left.

It moves.

You adjust your satchel on your shoulder and push open the gate.

---

**Edmund (internal):** *"Whatever Ashcroft left behind in there — it waited a hundred years. It can wait five more minutes while I check my equipment."*

---

**Choices:**
```
[[Inspect the gate for warding marks->Scene Manor Entrance]]
[[Walk straight to the front door->Scene Manor Entrance]]
```

---

**Character Art Prompt — Edmund Voss (neutral):**
```
Full body, standing, slightly hunched against light rain, [EDMUND_COAT], [EDMUND_SATCHEL] over left shoulder, right hand adjusting coat collar, expression calm but alert, dark circles under eyes, short dark hair slightly damp, anime-inspired character sprite, no background, with [OOMPH]
```

**Background Art Prompt — Manor Exterior Night:**
```
Victorian gothic manor exterior at night, four-storey blackened stone facade, iron gate in foreground, fog and fine mist in air, single amber-lit window on upper floor, dark overcast sky, bare twisted trees flanking the path, cobblestone path leading to front door, moody dark fantasy atmosphere, pixel art background, with [OOMPH]
```

---

### `Scene Manor Entrance`
**Tags:** `scene-hub`  
**Music:** `assets/music/theme-manor-ambient.mp3`  
**Background:** `assets/image/bg/entrance-hall.png`  
**Characters shown:** Seraphine (neutral), Edmund (neutral)

---

**Narrative:**

The entrance hall swallows you whole. Vaulted ceilings, a dead chandelier choked with cobwebs, walls lined with portraits whose eyes seem slightly — *wrong*. Not watching you. Looking away, as if they have already seen what happens next and want no part of it.

A figure stands at the foot of the grand staircase. She does not startle at your arrival, does not speak immediately. She simply regards you with pale grey eyes the colour of overcast February.

**Seraphine:** *"Mr. Voss. You are later than expected. The manor noticed."*

**Edmund:** *"The manor — noticed?"*

**Seraphine:** *"The candles. They lit themselves an hour ago. They do that when something significant approaches."*

She descends one step. Her black dress makes no sound. The brass music box in her hand ticks softly, though it is closed.

**Seraphine:** *"I am Seraphine. Lord Ashcroft's ward. I am... all that remains of the household staff."*

---

**Choices:**
```
[[Ask about Lord Ashcroft's death->Scene The Library]]
[[Ask about the East Wing->Scene East Wing Door]]
[[Step outside to speak with the groundskeeper->Scene The Grounds]]
```

---

**Character Art Prompt — Seraphine Ashcroft (neutral):**
```
Full body, standing at foot of staircase pose, [SERAPHINE_DRESS], [MUSIC_BOX] held in both hands at waist level, expression composed and watchful, pale complexion, silver-streaked dark hair pinned loosely, slight downward tilt of chin, anime-inspired character sprite, no background, with [OOMPH]
```

**Character Art Prompt — Edmund Voss (neutral):**
```
Full body, standing, [EDMUND_COAT], [EDMUND_SATCHEL] at side, arms at rest, expression attentive, one eyebrow slightly raised, wet coat shoulders, anime-inspired character sprite, no background, with [OOMPH]
```

**Background Art Prompt — Entrance Hall:**
```
Victorian gothic manor entrance hall interior, vaulted ceiling, unlit chandelier draped in cobwebs, grand staircase with dark wood banister curving upward, oil portrait paintings lining the walls, worn red carpet runner, cold candlelight from wall sconces, dark shadows pooling in corners, pixel art background, with [OOMPH]
```

---

### `Scene The Library`
**Tags:** `scene-library`  
**Music:** `assets/music/theme-tension.mp3`  
**Background:** `assets/image/bg/library.png`  
**Characters shown:** Seraphine (knowing), Edmund (suspicious)

---

**Narrative:**

Seraphine leads you through a side passage to the manor's library — floor-to-ceiling shelves of cracked leather volumes, a cold fireplace, and a desk buried under correspondence. The air is thick with old paper and something beneath it: ozone, like the aftermath of lightning.

She gestures to the desk. Among the letters you spot contracts — dozens of them — all signed in dark red ink. Not wax. Something else.

**Edmund:** *"These contracts. The ink — this isn't cinnabar. This is—"*

**Seraphine:** *"Blood. Yes. Lord Ashcroft made agreements. Long before I came to live here. Long before my mother did."*

She moves to the fireplace and places one hand on the mantle.

**Seraphine:** *"The entity that lives in the East Wing granted the Ashcroft line prosperity. Longevity. Influence. In exchange for — residency. And something renewed each generation."*

**Edmund:** *"What kind of something?"*

Seraphine does not answer immediately. The music box in her hand begins to play on its own — three notes, then silence.

**Seraphine:** *"The next heir. Always the next heir."*

---

**Choices:**
```
[[Press Seraphine for details about the entity->Scene The Secret]]
[[Go investigate the East Wing yourself->Scene East Wing]]
[[Return to the entrance hall->Scene Manor Entrance]]
```

---

**Character Art Prompt — Seraphine Ashcroft (knowing):**
```
Full body, standing beside fireplace, [SERAPHINE_DRESS], [MUSIC_BOX] held loosely in one hand at side, expression calm with a weight of sadness behind it, eyes slightly averted, chin level, quiet resignation in posture, anime-inspired character sprite, no background, with [OOMPH]
```

**Character Art Prompt — Edmund Voss (suspicious):**
```
Full body, leaning slightly forward, [EDMUND_COAT], [EDMUND_SATCHEL] open at his feet, one hand holding a contract paper up toward light, eyes narrowed in scrutiny, jaw set, brow furrowed, anime-inspired character sprite, no background, with [OOMPH]
```

**Background Art Prompt — Library:**
```
Victorian gothic library interior, floor-to-ceiling dark wood bookshelves crammed with aged leather volumes, cold stone fireplace with no fire, large writing desk covered in scattered papers and inkwells, tall arched window with rain-fogged glass, candlelight throwing long shadows across the room, dark moody atmosphere, pixel art background, with [OOMPH]
```

---

### `Scene The Secret`
**Tags:** `scene-seraphine-secret`  
**Music:** `assets/music/theme-seraphine.mp3`  
**Background:** `assets/image/bg/seraphine-chamber.png`  
**Characters shown:** Seraphine (sad), Edmund (determined)

---

**Narrative:**

Seraphine leads you to her private chamber — sparse, cold, a single candle burning on the windowsill. She sits on the edge of a chair and for the first time, some of the composure cracks.

**Seraphine:** *"I am the last of the Ashcroft line, Mr. Voss. Lord Aldric had no children. He adopted me specifically because the contract required an heir. He never told me. Not until last winter."*

**Edmund:** *"He raised you to be — handed over?"*

**Seraphine:** *"He raised me to break the contract. He spent forty years searching for a way. He died before he found one."*

She opens the music box. The three-note melody plays again, and this time you see it: a thin slip of paper inside the lid. Written in a cramped hand.

**Seraphine:** *"He left me this. A name. Yours. He said you were the only one who survived a direct confrontation with a bound entity and walked away."*

**Edmund (internal):** *"Survived. Barely. And three others didn't."*

**Edmund:** *"What does the entity want from you, exactly?"*

**Seraphine:** *"To remain. In me. Permanently."*

---

**Choices:**
```
[[Agree to help Seraphine break the contract->Scene East Wing]]
[[Ask to see Ashcroft's research notes first->Scene The Library]]
```

---

**Character Art Prompt — Seraphine Ashcroft (sad):**
```
Full body, seated on edge of wooden chair, [SERAPHINE_DRESS], [MUSIC_BOX] open in lap, head bowed slightly, eyes downcast with restrained grief, hands trembling slightly at the lid, composed exterior breaking at the edges, anime-inspired character sprite, no background, with [OOMPH]
```

**Character Art Prompt — Edmund Voss (determined):**
```
Full body, standing, [EDMUND_COAT] open at chest, [EDMUND_SATCHEL] gripped in one hand, expression firm and resolute, jaw squared, eyes direct and steady, leaning forward slightly, anime-inspired character sprite, no background, with [OOMPH]
```

**Background Art Prompt — Seraphine's Chamber:**
```
Victorian gothic bedroom interior, sparse furnishings, single wooden chair beside a small writing table, tall narrow window with rain streaking the glass, single candle on windowsill casting warm circle of light in cold room, dark stone walls, rumpled dark bedding in background, intimate and melancholy atmosphere, pixel art background, with [OOMPH]
```

---

### `Scene The Grounds`
**Tags:** `scene-grounds`  
**Music:** `assets/music/theme-manor-ambient.mp3`  
**Background:** `assets/image/bg/manor-grounds-fog.png`  
**Characters shown:** Mott (warning)

---

**Narrative:**

You find the groundskeeper crouched near the rose hedge, trimming dead growth at ten o'clock at night as though this were perfectly reasonable behaviour. He does not look up when you approach, though he clearly hears you.

**Mott:** *"Knew they'd send someone eventually."*

**Edmund:** *"You knew Lord Ashcroft requested—"*

**Mott:** *"Ashcroft's been dead three months. Letter wasn't from him."*

He finally looks up. His eyes are the flat grey of river stones, and his expression is one of a man who has made peace with something ugly.

**Mott:** *"The thing in the East Wing sent that letter. It wants an audience. Needed someone who'd actually come inside instead of running."*

He holds up his right hand — three fingers. Two are missing, the stumps cleanly healed over.

**Mott:** *"I tried to leave once. Made it to the edge of the property. The manor asked for a toll."*

He stands, lifting his lantern.

**Mott:** *"Leave tonight, Mr. Voss. Before it decides you're useful."*

---

**Choices:**
```
[[Ask Mott what he knows about the contract->Scene Manor Entrance]]
[[Ignore the warning and head inside->Scene Manor Entrance]]
```

---

**Character Art Prompt — Mott (warning):**
```
Full body, standing upright, stocky older man in worn groundskeeper's coat and muddy boots, [MOTT_LANTERN] raised in right hand, right hand clearly showing only three fingers, expression grave and direct, weathered face with deep lines, short white stubble, eyes flat and resigned, anime-inspired character sprite, no background, with [OOMPH]
```

**Background Art Prompt — Manor Grounds in Fog:**
```
Victorian gothic manor grounds at night, dense low fog rolling across overgrown garden paths, dead rose hedges trimmed into irregular shapes, iron fence visible in background, pale moonlight diffused through mist, skeletal bare trees, gravel path disappearing into fog, oppressive quiet atmosphere, pixel art background, with [OOMPH]
```

---

### `Scene Mott Warning`
**Tags:** `scene-mott-warn`  
**Music:** `assets/music/theme-tension.mp3`  
**Background:** `assets/image/bg/manor-grounds-fog.png`  
**Characters shown:** Mott (resigned)

---

**Narrative:**

You find Mott again near the gate — or rather, he finds you. He steps out of the fog as if he was waiting.

**Mott:** *"Changed your mind?"*

**Edmund:** *"Not yet. I need to know what's actually in the East Wing."*

Mott is quiet a long time. The fog thickens around his boots.

**Mott:** *"It's old. Older than the manor. The Ashcrofts didn't summon it — they found it already here, in the ground, when they laid the first foundation stone. The first Lord made a deal because the alternative was worse."*

**Edmund:** *"What was the alternative?"*

**Mott:** *"It wore his family's faces. Wore them around the village. Did things. The deal stopped that."*

He turns back toward the manor.

**Mott:** *"Now it wants a permanent body. The girl is the last of the line. After her there's no contract, no deal, no reason to behave."*

---

**Choices:**
```
[[Head to the East Wing immediately->Scene East Wing]]
[[Return to Seraphine->Scene The Secret]]
```

---

**Character Art Prompt — Mott (resigned):**
```
Full body, standing in fog, stocky older man in worn groundskeeper coat, [MOTT_LANTERN] hanging low at his side, right hand with three fingers resting at his belt, expression dull with weary acceptance, eyes distant, shoulders rounded with old defeat, anime-inspired character sprite, no background, with [OOMPH]
```

---

### `Scene East Wing Door`
**Tags:** `scene-east-wing-door`  
**Music:** `assets/music/theme-tension.mp3`  
**Background:** `assets/image/bg/east-wing-door.png`  
**Characters shown:** Edmund (suspicious)

---

**Narrative:**

The East Wing is sealed by a set of double doors at the end of the second-floor corridor. They are locked — but not with a key. Iron bolts on this side, yes, but also something else: a ring of small markings carved into the frame. Old workings. Containment sigils, roughly done but functional.

Someone went to considerable effort to keep what's inside *in*.

And yet. The gap under the door breathes — a slow, rhythmic exhalation, like something sleeping.

**Edmund (internal):** *"Not sleeping. Waiting."*

A single note drifts from beneath the door. The same note Seraphine's music box plays.

---

**Choices:**
```
[[Return to Seraphine and ask about the sigils->Scene The Secret]]
[[Return to the entrance hall->Scene Manor Entrance]]
```

---

**Character Art Prompt — Edmund Voss (suspicious):**
```
Full body, crouching slightly toward door, [EDMUND_COAT], [EDMUND_SATCHEL] open at his feet with papers and vials visible, one hand raised near the doorframe tracing a sigil without touching it, expression sharp and wary, brow furrowed deeply, anime-inspired character sprite, no background, with [OOMPH]
```

**Background Art Prompt — East Wing Door:**
```
Victorian gothic manor interior corridor at night, end of hallway with imposing double doors of dark wood, heavy iron bolts drawn across, faint carved sigil marks around the door frame, no light under door, candlelight barely reaching from behind viewer, shadows pooling heavily, atmosphere of sealed dread, pixel art background, with [OOMPH]
```

---

### `Scene East Wing`
**Tags:** `scene-east-wing`  
**Music:** `assets/music/theme-shade.mp3`  
**Background:** `assets/image/bg/void-space.png`  
**Characters shown:** Shade (distant), Edmund (determined)

---

**Narrative:**

The sigils on the door give way the moment you press your palm to them — they were never locking the door from visitors. They were locking the entity from leaving without invitation.

The East Wing is not what you expected.

The rooms beyond are normal — dusty, cold, forgotten — but at the far end is a space that should not exist: a room larger than the manor's footprint allows, its walls dissolving into deep shadow at the edges. The floor is intact. The ceiling is not. Above you: nothing. An absolute dark that breathes.

And within it — a shape. Tall, antlered, patient.

The Ashcroft Shade regards you without eyes. Its voice arrives not through sound but through the sudden certainty of words already being present in your thoughts.

**The Shade:** *"Edmund Voss. The failed exorcist. The survivor. You are more interesting than the last six the girl tried to summon."*

**Edmund:** *"Those were investigators?"*

**The Shade:** *"Meals."*

---

**Choices:**
```
[[Stand your ground and state your terms->Scene The Confrontation]]
[[Retreat to the corridor->Scene Manor Entrance]]
```

---

**Character Art Prompt — The Ashcroft Shade (distant):**
```
Full body, standing at distance, [SHADE_FORM], [SHADE_ANTLERS], no face or features, posture still and towering, slightly translucent at edges, violet glow faint at center, radiating ancient stillness, anime-inspired character sprite, no background, with [OOMPH]
```

**Character Art Prompt — Edmund Voss (determined):**
```
Full body, standing upright, [EDMUND_COAT], [EDMUND_SATCHEL] open in one hand, other hand extended with iron talisman visible at wrist, expression controlled fear held behind a mask of resolve, jaw tight, eyes fixed forward, anime-inspired character sprite, no background, with [OOMPH]
```

**Background Art Prompt — Void Space:**
```
Interior of an impossibly large dark room within a Victorian manor, stone floor intact but walls fading into absolute shadow at edges, ceiling absent replaced by impenetrable darkness, faint violet luminescence pooling at the centre of the floor, dust motes suspended mid-air, atmosphere of vast ancient emptiness, pixel art background, with [OOMPH]
```

---

### `Scene The Confrontation`
**Tags:** `scene-confrontation`  
**Music:** `assets/music/theme-shade.mp3`  
**Background:** `assets/image/bg/void-space.png`  
**Characters shown:** Shade (close), Edmund (determined), Seraphine (fearful)

---

**Narrative:**

Seraphine appears at your shoulder — you did not hear her follow, but she is here now, the music box open and playing its three-note sequence on a loop. Her face is pale but set.

**Seraphine:** *"We came to dissolve the contract."*

**The Shade:** *"Contracts do not dissolve. They conclude."*

It moves closer. The temperature drops.

**The Shade:** *"The girl concludes this one. Or the investigator may offer an alternative. I am not unreasonable. I simply require — continuity."*

You have what you need from Ashcroft's notes: a dissolution ritual, imperfect, dangerous. You also know what the Shade actually is beneath the theatrics — not a demon, not a spirit. Something older. A fragment of a consciousness that predates the manor, the city, perhaps language itself. It is not evil. It is simply *permanent*, in a world of transient things, and it is lonely in a way that is genuinely terrible.

You make your choice.

---

**Choices:**
```
[[Perform the dissolution ritual->Scene True Ending]]
[[Offer the Shade a different deal->Scene Dark Pact Ending]]
[[Grab Seraphine and run->Scene Haunted Ending]]
```

---

**Character Art Prompt — The Ashcroft Shade (close):**
```
Full body, looming close, [SHADE_FORM], [SHADE_ANTLERS], towering overhead, leaning forward slightly, no face but orientation suggesting it is focused directly on viewer, violet light intensifying at core, smoke roiling at edges, anime-inspired character sprite, no background, with [OOMPH]
```

**Character Art Prompt — Seraphine Ashcroft (fearful):**
```
Full body, standing slightly behind Edmund, [SERAPHINE_DRESS], [MUSIC_BOX] held open in both hands playing, eyes wide with controlled fear, chin raised in defiance despite fear, knuckles white on the music box, shoulders braced, anime-inspired character sprite, no background, with [OOMPH]
```

---

### `Scene True Ending`
**Tags:** `scene-ending-true`  
**Music:** `assets/music/theme-ending-true.mp3`  
**Background:** `assets/image/bg/manor-exterior-night.png`  
**Characters shown:** Edmund (determined), Seraphine (neutral)

---

**Narrative:**

The ritual costs Edmund three years — he feels them leave like warmth draining from a room. But the dissolution holds.

The Shade does not scream. It simply... recedes. Like a tide accepting that the shore belongs to someone else.

Ashcroft Manor does not crumble. It remains, stone and mortar, no longer breathing, no longer watching. Just a building.

You and Seraphine stand at the gate in the early grey of dawn. She still holds the music box. It is silent.

**Seraphine:** *"Will you be all right?"*

**Edmund:** *"I've been not-all-right for years. This is just a new version."*

A pause. She almost smiles.

**Seraphine:** *"There are forty years of Ashcroft anomalous records in that library. Lord Aldric catalogued everything he found. It would take someone with expertise to evaluate them properly."*

**Edmund:** *"Are you offering me a job?"*

**Seraphine:** *"I'm offering you a reason to stay, Mr. Voss. The work will provide its own justification."*

He looks back at the manor. It is, for the first time, simply a house.

**Edmund (internal):** *"Maybe. Maybe that's enough."*

> **TRUE ENDING — "The Weight of Morning"**  
> *The contract is broken. The Shade is dissolved. Seraphine is free.*  
> *Edmund finds, if not peace, at least purpose.*

---

**Background Art Prompt — Manor Exterior Dawn:**
```
Victorian gothic manor exterior at dawn, pale grey and rose light on the horizon, iron gate open, fog retreating across grounds, manor stone facade losing its menace in the growing light, bare trees casting long pale shadows, quiet and still, a sense of something finished, pixel art background, with [OOMPH]
```

---

### `Scene Dark Pact Ending`
**Tags:** `scene-ending-pact`  
**Music:** `assets/music/theme-ending-pact.mp3`  
**Background:** `assets/image/bg/void-space.png`  
**Characters shown:** Shade (bargain), Edmund (neutral)

---

**Narrative:**

**Edmund:** *"You want continuity. You want to persist. There's another way."*

You lay out the terms. The Shade listens — this is, perhaps, the most valuable thing it possesses: patience to hear an argument out.

The alternative: Edmund provides the entity with a bridge — a curated channel, like a lighthouse signal, through the occult records. Not a host. Not possession. A *correspondence*. In exchange, Seraphine goes free. The manor seals permanently. The Shade remains, but contained, connected to the world of the living only through the encrypted communications Edmund will broker for it.

The Shade considers for seventeen seconds. Edmund counts.

**The Shade:** *"You would become my intermediary. My voice."*

**Edmund:** *"Your interpreter. There's a difference."*

**The Shade:** *"Is there."*

It is not a question. But it accepts.

Edmund walks out of Ashcroft Manor with Seraphine. He also walks out with a particular weight behind his left eye that will not leave — a presence, curled at the edge of his thoughts, patient and vast, that occasionally has *opinions* about what he reads.

> **DARK PACT ENDING — "The Interpreter"**  
> *Seraphine is free. The Shade is bound.*  
> *Edmund is neither quite free nor quite bound — and will spend years deciding which is worse.*

---

**Character Art Prompt — The Ashcroft Shade (bargain):**
```
Full body, [SHADE_FORM], [SHADE_ANTLERS], posture slightly lowered from towering height, less aggressive, violet glow softened to a steady pulse, still and attentive, giving the impression of listening, anime-inspired character sprite, no background, with [OOMPH]
```

---

### `Scene Haunted Ending`
**Tags:** `scene-ending-haunted`  
**Music:** `assets/music/theme-ending-haunted.mp3`  
**Background:** `assets/image/bg/manor-exterior-night.png`  
**Characters shown:** Edmund (suspicious)

---

**Narrative:**

You grab Seraphine's wrist and run.

The manor lets you. The gate opens easily. The fog parts. The hansom cab — impossibly — is still waiting, horse calm, driver asleep.

You ride to London in silence. Seraphine says nothing. The music box says nothing. You tell yourself you made the right call.

Three weeks later, you notice that the wallpaper in your flat has a pattern you don't remember selecting. Tiny repeating motifs, barely visible: antlers.

Your landlady says it's always been there.

You find the same pattern on the lining of your coat. On the back page of your case journal. On the fogged-over glass of your bathroom mirror each morning, drawn by some absent hand while you slept.

You never went back to Ashcroft Manor.

But something from Ashcroft Manor came back with you.

> **HAUNTED ENDING — "The Pattern"**  
> *You escaped. Didn't you.*  
> *The contract was not dissolved. It simply found a new address.*

---

**Background Art Prompt — London Flat Interior:**
```
Small Victorian London flat interior at night, modest writing desk, shelved books, wallpaper with barely-visible repeating antler pattern if examined closely, single oil lamp lit on desk, curtains drawn, a sense of ordinary domesticity with something subtly wrong in the details, pixel art background, with [OOMPH]
```

---

## MUSIC CUE SUMMARY

| Track | Usage |
|---|---|
| `theme-manor-ambient.mp3` | Default manor exploration |
| `theme-tension.mp3` | Discovery / investigation scenes |
| `theme-seraphine.mp3` | Seraphine personal scenes |
| `theme-shade.mp3` | East Wing / Shade encounters |
| `theme-ending-true.mp3` | True Ending |
| `theme-ending-pact.mp3` | Dark Pact Ending |
| `theme-ending-haunted.mp3` | Haunted Ending |

---

## PASSAGE COUNT SUMMARY

| Passage | Tag | Type |
|---|---|---|
| Scene Arrival | scene-intro | Linear intro |
| Scene Manor Entrance | scene-hub | Hub / branch point |
| Scene The Library | scene-library | Investigation |
| Scene The Secret | scene-seraphine-secret | Character / story |
| Scene The Grounds | scene-grounds | Character / warning |
| Scene Mott Warning | scene-mott-warn | Character / lore |
| Scene East Wing Door | scene-east-wing-door | Discovery |
| Scene East Wing | scene-east-wing | Major encounter |
| Scene The Confrontation | scene-confrontation | Climax |
| Scene True Ending | scene-ending-true | Ending |
| Scene Dark Pact Ending | scene-ending-pact | Ending |
| Scene Haunted Ending | scene-ending-haunted | Ending |

**Total Passages: 12** *(Manageable solo indie scope)*  
**Total Endings: 3**  
**Total Named Characters: 4 (including PC)*

---

*Pitch document generated for: Veil of Ashcroft Manor — v1.0*