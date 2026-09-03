# Twine AI Generated Fan Fic Demo

A Twine 2 + Harlowe visual novel creation kit.

## Project Summary

- Engine: Twine 2 (Harlowe 3.x)
- Local server: `http://127.0.0.1:8080/`
- Open command: `yarn open --story {story-name}` (requires running http server with `yarn serve` in the background).
- Build command: `yarn build --story {story-name}`
- Deployment target: itch.io compatible web package (.zip)

## Requirements

- Python 3
- Node v26

## Quick Start

1) Install Yarn (npm install yarn -g)
2) Install node deps: `yarn install`
3) Make Python venv: `python -m venv .venv`
4) Activate Python venv: `. .venv/bin/activate`
5) Install Python deps: `pip install -r requirements.txt`
6) Can proceed to use most commands specified in remainder of this readme.md doc.

## Folder Structure

- `input/**/*` - folder not committed to repo
- `output/**/*` - folder not committed to repo
- `lora/**/*` - recommend to keep lora safetensor files in this location
- `models/**/*` - recommend to keep model safetensor files in this location
- `stories/{story-name}` - directory to keep the .html story and the assets. ex. `stories/ashcroft-manor`
- `stories/{story-name}/{story-name}.html` - Twine story export
- `stories/{story-name}/assets/image` - game art and background image assets
- `stories/{story-name}/assets/music` - game audio tracks and music
- `stories/{story-name}/pitch/rough-draft` - VN story pitches (rough draft)
- `stories/{story-name}/pitch/final-draft` - VN story pitches (final draft)
- `pitch/` - keep pitches for the stories generated within here
- `scripts/` — build tools
- `build/` — temporary build output
- `dist/` — packaged distribution assets
- `pytools/` - python scripts and tools for image manipulation
- `workflow/` - AI Generation workflow pipeline as ordered .md files
- `docs/how-to-prompt-better-vn-story.md` - Instructions and tips to prompt AI to generate a unique story rich visual novel game

## Make a new VN Game

- Step #01 - Prompt Claude AI to run workflow process #1: "Run workflow process 1-pitch-a-story.md to make a unique story pitch"
- Step #02 - Copy the generated pitch into the pitch/draft-rough folder as {story-name}.md, and then copy it again into pitch/draft-final folder as {story-name}.md
- Step #03 - Keep the rough draft story pitch to reference what Claude AI gave us, but modify and tailor the final draft story pitch to be followed in next steps.
- Step #04 - Prompt Claude AI: "Generate my story in twine (Harlowe ~3.3): pitch/draft-final/{story-name}.md" (While referenced the workflow/2-gen-twine-story.md file)
- Step #05 - Copy the {story-name}.html file into Stories folder of Twine and open it at least once to ensure it works.
- Step #06 - Copy the {story-name}.html file back into this repo under the stories/{story-name}/{story-name}.html file path location.
- Step #07 - "Generate art assets from prompts." (while selected the workflow/3-gen-art-asset.md file) (Human does this step for now..)
- Step #08 - Prompt AI: "Add art assets in my story." (while selected the workflow/4-add-art-assets-into-story.md file) (Skip this if done earlier in step #4)
- Step #09 - Playtest... and polish the game - and add music assets.
- Step #10 - Attribute and credit authors appropriately on the Scene Credits scene.

## Local Development

1. Clone submodules - `git submodule update --init --recursive --remote`
2. Serve the repository from `http://127.0.0.1:8080/`.
3. Install dependencies once if needed:

```bash
yarn install
```

4. From VS Code or any terminal in this repo, run:

```bash
yarn serve
```

5. Open the URL in your browser.

## Build & Package

Use the project build script to prepare the game set in the package.json 'config.story' for deployment.

```bash
yarn build --story ashcroft-manor
```

This script runs `node scripts/build.js` and packages the project into the dist folder as (.zip) Itch.io compatible upload

**Note**: The build process automatically excludes `src/` directories from the final package, so only processed assets are included in the distribution.

### Building Specific Stories

To build a specific story from the `stories/` directory:

```bash
# Use the story name (matches stories/[name]/[name].html)
yarn build --story ashcroft-manor

# Or set it in package.json config
yarn config set story ashcroft-manor
yarn build:story

# Or use environment variable
STORY=ashcroft-manor yarn build
```

## Image Processing

Process images from the `assets/image/src` directory into pixel art for your stories.

```bash
yarn process-images --story ashcroft-manor
```

This command:
- Finds all images in `stories/{story-name}/assets/image/src/`
- **Skips background images by default** (files/directories containing "background")
- Processes character and other images with `pytools/pixel.py -c 64 --remove-bg --outline`
- Outputs processed images to `stories/{story-name}/assets/image/src/processed/`
- **Converts all output to PNG format** (`.png` extension)
- Creates output directories as needed
- Preserves subdirectory structure

### Processing Background Images

To include background images in processing:

```bash
yarn process-images:all --story ashcroft-manor
```

### Processing Specific Stories

```bash
# Process images for a specific story (characters only) background excluded
yarn process-images --story ashcroft-manor

# Or set it in package.json config
yarn config set story ashcroft-manor
yarn process-images:story      # characters only
yarn process-images:all:story  # including backgrounds
```

The image processor automatically resolves story sources the same way as the build system.

### Build Options

- `yarn build --story [name]` - Build specific story
- `yarn build --strip-only` - Strip URLs without creating zip
- `yarn build:story` - Build using npm config story setting
- `yarn process-images --story [name]` - Process character images for specific story
- `yarn process-images:story` - Process character images using npm config story setting
- `yarn process-images:all` - Process all images (including backgrounds) for default story
- `yarn process-images:all --story [name]` - Process all images for specific story
- `yarn process-images:all:story` - Process all images using npm config story setting

## Deployment Notes

- The build output is intended for static web hosting (specifically Itch.io)
- Use `dist/` contents for itch.io or similar web deployment.
- Keep asset paths relative so the game runs offline and in packaged builds.

## Useful Commands

- `yarn serve` — serve the assets locally
- `ls ~/.cache/huggingface/hub/` - check for downloaded models from hugging face
- `rm -rf ~/.cache/huggingface/` - remove model generation files to gain back file spaace

## Resources

- The manifest and process documents define the current naming conventions for scenes and assets
- The project uses `assets/image/` and `assets/music/` as the main runtime asset directories
- Upscale AI Artwork Src Images (HQX algorithm) - https://aifreebox.com/tools/image/enhance
- Separate vocals from music - https://vocalremover.org/
- Find royalty free video game music - https://opengameart.org/
- Free online tool to generate artwork (no login required) - https://perchance.org/ai-text-to-image-generator
- Free online tool to remove BG from anime - https://huggingface.co/spaces/skytnt/anime-remove-background
- Free online tool to animate an image with prompt - https://huggingface.co/spaces/kulkas2pintu/wan555
- Rotate, animate, and clean-up pixel art (sometimes) - https://www.pixellab.ai/
- Models for Anime Pixel Art generation: https://civitai.com/models/6755/cetus-mix?modelVersionId=48569
- LoRA for SD1.5 Model to generate decent pixel art - https://civitai.com/models/44960/mpixel
- Twine-to-JSON converter example that works with Harlowe v3: https://jtschoonhoven.github.io/twine-to-json/