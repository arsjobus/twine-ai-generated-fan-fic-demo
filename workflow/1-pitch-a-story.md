# WORKFLOW PROCESS #1 - Convert Idea into Story Pitch

## Prompt for AI ChatBot to generate a pitch:

Provide the response as Markdown (.md) format either save the file to my local system (preferred) or provide an easy to copy output.

Create a complete design outline for a Twine-based visual novel from the chosen story. Prompt me to choose for each:

- Setting: [Feudal Japan, Ancient Egypt, Medieval Europe, Viking Age Scandinavia, Imperial China, Ottoman Empire, Ancient Greece / Mythology, Aztec Empire, Renaissance Italy, Victorian England, Cyberpunk Megacity, Deep Space Station, Generation Ship (mid-voyage), Mars Colony, Post-Singularity Earth, Underwater Arcology, Lunar City, Dyson Sphere Habitat, Time-Loop Research Facility, Orbital Elevator, Modern High School, Tokyo University Dorm, Indie Music Scene (any city), Hospital / Medical Drama, Small Coastal Town, Culinary Academy, Fashion Week (Paris / Milan), Online Streaming World (influencer life), Professional eSports House, Rural Countryside Village, Abandoned Asylum, Cursed Gothic Manor, Plague-Era Town, Sunken Ghost Ship, Eldritch Research Station (Antarctica), Liminal Hotel (between worlds), Carnival of Souls, Post-Apocalyptic Wasteland, Infected Quarantine Zone, Cult Compound, Floating Sky Islands, Clockwork Steampunk City, Dream Realm (shared dreamscape), Mushroom Forest Kingdom, Spirit World Crossroads, Pocket Dimension Library, Sentient Starship Interior, Mythological Underworld (Hades-inspired), Enchanted Academy for Monsters, Living Desert (sand sea with dune ships), other (specify..)]
- Tone: [romance / horror / mystery / sci-fi / other (specify..)]
- Target Audience: [male / female]
- Spiciness: [SFW / NSFW / other (specify..)]

## Additional Requirements:

- Use Twine passage naming conventions like `Scene <SceneName>` (No underscores!)
- Use scene tags in lower-case hyphenated form, such as `scene-intro`, `scene-hub`, etc..
- Include branching choices, logical hubs, and multiple endings.

For every unique passage:

- Write the narrative text and the character dialogue, and clearly group them separately under the appropriate heading.
- Include player dialogue choices in Twine format `[[Choice->Scene <SceneName>]]`.
- Add a matching pixel-art generation prompts for each character in the scene and backgrounds separately.
- Use asset paths and folders compatible with this project: `assets/image/`, `assets/music/`

## Art Requirements:

I need prompts for each character within a passage and the background art used in the scene - but note that I want to generate the characters separate from the backgrounds so the details about backgrounds shouldn't be in the prompts for characters and details about characters shouldn't be in the prompts for backgrounds. The generated prompts should be fixed to make use of variables like [VARIABLE_NAME] because I use Perchance AI to generate the artwork. If one of the characters has an object they possess such as a guitar throughout the passages then that needs a variable like [GUITAR] and needs details about the object generated to keep consistency and assigned to the variable so that this character possessed object or outfit can be some what consistent throughout the story. Furthermore, the character themselves need to maintain consistency by having core and body features described in a [{char_name}_CORE] variable. i.e. hair color, hair type, body build, skin color, eyes color, makeup details, bust size and butt size in the case of females. Note: The [OOMPH] variable is always used in every prompt at the end "with [OOMPH]". Remove the duplicate keywords out of the prompts that [OOMPH] has already. [OOMPH] should always have these keywords: pixel-perfect anime, highly polished, vibrant yet balanced color palette, visual novel art style. Character art prompts should always have the terms "solid white background" at the end of the prompt.

- Anime-inspired aesthetic
- Gradients are permissible but not required
- True pixel art only

## Project Scope:

Keep the scope manageable for an indie solo developer, but allow extension easily