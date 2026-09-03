import sys
import random
import os
import torch
from diffusers import (
    StableDiffusionPipeline,
    StableDiffusionImg2ImgPipeline,
    DPMSolverMultistepScheduler,
)
from safetensors.torch import load_file
from PIL import Image
from datetime import datetime
import numpy as np

# ==========================================
# DEVICE SETUP
# ==========================================
if torch.backends.mps.is_available():
    device = "mps"
    dtype = torch.float32
    print("Using device: mps (Apple Silicon)")
elif torch.cuda.is_available():
    device = "cuda"
    dtype = torch.float16
    print(f"Using device: cuda ({torch.cuda.get_device_name(0)})")
else:
    device = "cpu"
    dtype = torch.float32
    print("Using device: cpu (this will be slow)")

# ==========================================
# LOAD BASE MODEL
# ==========================================
MODEL_PATH = "models/cetusMix_Coda2.safetensors"

print("Loading base model (CetusMix)...")

pipe = StableDiffusionPipeline.from_single_file(
    MODEL_PATH,
    torch_dtype=dtype,
).to(device)

pipe.scheduler = DPMSolverMultistepScheduler.from_config(
    pipe.scheduler.config,
    algorithm_type="dpmsolver++",
    use_karras_sigmas=True,
)

pipe.enable_attention_slicing()
if device == "cuda":
    pipe.enable_xformers_memory_efficient_attention()
pipe.vae.enable_slicing()

pipe.safety_checker = None
pipe.requires_safety_checker = False

# ==========================================
# LOAD LORAS
# ==========================================
def load_kohya_lora(pipe, lora_path, alpha=0.5):
    """
    Manually load a Kohya/A1111-format LoRA into a diffusers pipeline.
    """

    if not os.path.isfile(lora_path):
        print(f"LoRA file not found, skipping: {lora_path}")
        return

    state_dict = load_file(lora_path)
    visited = set()

    for key in state_dict:
        if "lora_down" not in key:
            continue

        up_key = key.replace("lora_down", "lora_up")
        alpha_key = key.split("lora_down")[0] + "alpha"

        if up_key not in state_dict:
            continue

        down = state_dict[key].float()
        up = state_dict[up_key].float()

        lora_alpha = (
            state_dict[alpha_key].item()
            if alpha_key in state_dict
            else down.shape[0]
        )

        scale = alpha * (lora_alpha / down.shape[0])

        if key.startswith("lora_unet_"):
            layer_path = key[len("lora_unet_"):].split(".lora_down")[0]
            model = pipe.unet

        elif key.startswith("lora_te_"):
            layer_path = key[len("lora_te_"):].split(".lora_down")[0]
            model = pipe.text_encoder

        else:
            continue

        parts = layer_path.split("_")

        module = model
        found = True
        i = 0

        while i < len(parts):
            matched = False

            for j in range(len(parts), i, -1):
                candidate = "_".join(parts[i:j])

                if hasattr(module, candidate):
                    module = getattr(module, candidate)
                    i = j
                    matched = True
                    break

            if not matched:
                found = False
                break

        if not found or not hasattr(module, "weight"):
            continue

        if key in visited:
            continue

        visited.add(key)

        if up.dim() == 4:
            delta = (
                up.squeeze(-1).squeeze(-1)
                @ down.squeeze(-1).squeeze(-1)
            ).unsqueeze(-1).unsqueeze(-1)

        else:
            delta = up @ down

        module.weight.data += (
            scale
            * delta.to(module.weight.dtype).to(module.weight.device)
        )

    print(f"LoRA applied: {len(visited)} layers patched (alpha={alpha:.3f})")

def load_kohya_lora_additive(pipe, lora_path, alpha=0.5):
    """
    Load a Kohya/A1111-format LoRA into a diffusers pipeline with additive blending.
    Multiple LoRAs can be applied sequentially and will sum their effects.
    """
    if not os.path.isfile(lora_path):
        print(f"LoRA file not found, skipping: {lora_path}")
        return

    state_dict = load_file(lora_path)

    for key in state_dict:
        if "lora_down" not in key:
            continue

        up_key = key.replace("lora_down", "lora_up")
        alpha_key = key.split("lora_down")[0] + "alpha"

        if up_key not in state_dict:
            continue

        down = state_dict[key].float()
        up = state_dict[up_key].float()

        # Determine layer-specific alpha
        lora_alpha = state_dict[alpha_key].item() if alpha_key in state_dict else down.shape[0]
        scale = alpha * (lora_alpha / down.shape[0])

        # Determine target module
        if key.startswith("lora_unet_"):
            layer_path = key[len("lora_unet_"):].split(".lora_down")[0]
            model = pipe.unet
        elif key.startswith("lora_te_"):
            layer_path = key[len("lora_te_"):].split(".lora_down")[0]
            model = pipe.text_encoder
        else:
            continue

        # Traverse to the module
        parts = layer_path.split("_")
        module = model
        found = True
        i = 0
        while i < len(parts):
            matched = False
            for j in range(len(parts), i, -1):
                candidate = "_".join(parts[i:j])
                if hasattr(module, candidate):
                    module = getattr(module, candidate)
                    i = j
                    matched = True
                    break
            if not matched:
                found = False
                break

        if not found or not hasattr(module, "weight"):
            continue

        # Compute LoRA delta
        if up.dim() == 4:
            delta = (
                up.squeeze(-1).squeeze(-1)
                @ down.squeeze(-1).squeeze(-1)
            ).unsqueeze(-1).unsqueeze(-1)
        else:
            delta = up @ down

        # Additive blending: sum with existing weights
        module.weight.data += scale * delta.to(module.weight.dtype).to(module.weight.device)

    print(f"LoRA applied additively: {lora_path} (alpha={alpha:.3f})")

# ==========================================
# CLI PARSING
# ==========================================
raw_args = sys.argv[1:]

# --hires
ENABLE_HIRES = "--hires" in raw_args
raw_args = [a for a in raw_args if a != "--hires"]

# ==========================================
# HELPERS
# ==========================================
def parse_int_flag(name, default):
    i = 0

    while i < len(raw_args):
        a = raw_args[i]

        if a == name and i + 1 < len(raw_args):
            val = int(raw_args[i + 1])
            del raw_args[i:i + 2]
            return val

        elif a.startswith(f"{name}="):
            val = int(a.split("=", 1)[1])
            del raw_args[i]
            return val

        i += 1

    return default


def parse_string_flag(name, default=None):
    i = 0

    while i < len(raw_args):
        a = raw_args[i]

        if a == name and i + 1 < len(raw_args):
            val = raw_args[i + 1]
            del raw_args[i:i + 2]
            return val

        elif a.startswith(f"{name}="):
            val = a.split("=", 1)[1]
            del raw_args[i]
            return val

        i += 1

    return default


# ==========================================
# FLAGS
# ==========================================
seed = parse_int_flag("--seed", None)

if seed is None:
    seed = random.randint(0, 2**32 - 1)

width = parse_int_flag("--width", 512)
height = parse_int_flag("--height", 768)
count = parse_int_flag("--count", 1)

custom_negative = parse_string_flag("--negative", "")
image_name = parse_string_flag("--image-name", None)

count = max(1, count)


def fix_dim(x):
    return max(64, (x // 8) * 8)


width = fix_dim(width)
height = fix_dim(height)

# ==========================================
# PROMPT
# ==========================================
if not raw_args:
    print(
        'Usage: python gen-art-anime.py "prompt" '
        '[--negative "text"] '
        '[--image-name "name"] '
        '[--hires] [--seed N] [--count N] '
        '[--width W] [--height H]'
    )

    print()
    print('  --negative TEXT   Extra negative prompt')
    print('  --image-name N    Output filename base')
    print('  --width W         Image width  (default 512)')
    print('  --height H        Image height (default 768)')
    print('  --count N         Number of images (default 1)')
    print('  --hires           Run hires fix')
    print('  --seed N          Reproducible seed')

    sys.exit(1)

user_prompt = raw_args[0]

print(f"Seed:       {seed}")
print(f"Size:       {width}x{height}")
print(f"Count:      {count}")
print(f"Hires:      {'enabled' if ENABLE_HIRES else 'disabled'}")

if image_name:
    print(f"Image Name: {image_name}")

# ==========================================
# PROMPTS
# ==========================================
QUALITY_PREFIX = (
    "(masterpiece, high quality, ultra-detailed)"
    # ", intricate eyes, beautiful eyes, detailed eyes"
    # ", perfect eyes, soft eyelashes, sharp pupils"
    ", vibrant colors, "
)

DEFAULT_NEGATIVE_PROMPT = (
    "(bad quality, low quality, lowres, low resolution:2), isometric"
    # ", bad eyes, deformed pupils, blurry eyes"
    # ", bad anatomy, bad hands, missing fingers"
    # ", extra fingers, fused fingers, too many fingers"
    # ", bad proportions, ugly, disfigured, blurry, watermark"
)

NEGATIVE_PROMPT = DEFAULT_NEGATIVE_PROMPT

if custom_negative:
    NEGATIVE_PROMPT += custom_negative

prompt = QUALITY_PREFIX + user_prompt

print(f"\nPrompt:   {prompt}")
print(f"Negative: {NEGATIVE_PROMPT}\n")

# ==========================================
# CONDITIONAL LORA LOADING (with alpha normalization)
# ==========================================
# Each entry: (trigger phrase, lora file path, base alpha at single-LoRA strength)
LORA_REGISTRY = [
    ("pixel", ".lora/pixel_f2.safetensors", 0.5),
    ("vados", ".lora/ogt_u6_vados-v1.safetensors", 0.7),
    ("android 18", ".lora/android_18_v110.safetensors", 0.6),
    ("bulma", ".lora/bulma_v1_1.safetensors", 0.6),
    ("sticker", ".lora/StickersRedmond15Version-Stickers-Sticker.safetensors", 0.5),
]

prompt_lower = user_prompt.lower()

active_loras = [
    (trigger, path, base_alpha)
    for trigger, path, base_alpha in LORA_REGISTRY
    if trigger in prompt_lower
]

num_active = len(active_loras)

if num_active > 1:
    print(
        f"{num_active} LoRA triggers detected — "
        f"normalizing alphas (dividing each by {num_active}) to avoid over-saturation"
    )
elif num_active == 1:
    print("1 LoRA trigger detected — using base alpha (no normalization needed)")

for trigger, path, base_alpha in active_loras:
    normalized_alpha = base_alpha / num_active
    print(
        f"Trigger word '{trigger}' detected — loading LoRA "
        f"(base alpha={base_alpha:.3f} -> normalized alpha={normalized_alpha:.3f})..."
    )
    load_kohya_lora(pipe, path, alpha=normalized_alpha)
    print("LoRA loaded successfully")

# ==========================================
# CLIP SKIP
# ==========================================
def encode_prompt_with_clip_skip(
    pipe,
    prompt,
    negative_prompt,
    clip_skip=2
):
    tokenizer = pipe.tokenizer
    text_encoder = pipe.text_encoder

    def encode(text):
        tokens = tokenizer(
            text,
            padding="max_length",
            max_length=tokenizer.model_max_length,
            truncation=True,
            return_tensors="pt",
        ).input_ids.to(device)

        with torch.no_grad():
            outputs = text_encoder(
                tokens,
                output_hidden_states=True
            )

            hidden = outputs.hidden_states[-(clip_skip + 1)]
            hidden = text_encoder.text_model.final_layer_norm(hidden)

        return hidden

    return encode(prompt), encode(negative_prompt)


print("Encoding prompts (clip skip=2)...")

prompt_embeds, negative_embeds = encode_prompt_with_clip_skip(
    pipe,
    prompt,
    NEGATIVE_PROMPT,
    clip_skip=2,
)

# ==========================================
# CFG RESCALE
# ==========================================
def rescale_cfg(image, factor=0.7):
    arr = np.array(image).astype(np.float32)

    mean = arr.mean(axis=(0, 1), keepdims=True)

    arr = mean + factor * (arr - mean)

    return Image.fromarray(
        np.clip(arr, 0, 255).astype(np.uint8)
    )

# ==========================================
# PIXELIZATION
# ==========================================
def to_pixel_art(img, downscale_factor=3):
    img = img.convert("RGB")

    w, h = img.size

    img = img.resize(
        (w // downscale_factor, h // downscale_factor),
        Image.Resampling.NEAREST
    )

    img = img.quantize(
        colors=256,
        method=Image.Quantize.MEDIANCUT,
        dither=Image.Dither.ORDERED
    )

    return img

# ==========================================
# GENERATION LOOP
# ==========================================
all_outputs = []

for idx in range(count):

    current_seed = seed + idx

    print()
    print("==========================================")
    print(f"Generating image {idx + 1}/{count}")
    print(f"Seed: {current_seed}")
    print("==========================================")

    generator = torch.Generator(device=device).manual_seed(
        current_seed
    )

    # ==========================================
    # BASE PASS
    # ==========================================
    print("Generating base image...")

    image = pipe(
        prompt_embeds=prompt_embeds,
        negative_prompt_embeds=negative_embeds,
        width=width,
        height=height,
        #num_inference_steps=20, # less steps for faster generation, pixel art can hide some imperfections (anime)
        num_inference_steps=35, # more steps for better quality, but slower (anime) 28
        guidance_scale=7.0,
        generator=generator,
    ).images[0]

    image = rescale_cfg(image, factor=0.7)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    suffix = f"_{idx + 1:03d}"

    base_filename = (
        image_name
        if image_name
        else f"cetus_base_{timestamp}"
    )

    base_path = (
        f"output/{base_filename}{suffix}.png"
    )

    image.save(base_path)

    print(f"Base image saved: {base_path}")

    # ==========================================
    # HIRES FIX
    # ==========================================
    if ENABLE_HIRES:

        print("Running hires fix (two-pass)...")

        img2img = StableDiffusionImg2ImgPipeline(
            **pipe.components
        )

        w, h = image.size
        scale = 1.5

        up1 = image.resize(
            (int(w * scale), int(h * scale)),
            Image.Resampling.LANCZOS
        )

        # Pass 1
        print("  Hires pass 1/2 (structural)...")

        pass1 = img2img(
            prompt_embeds=prompt_embeds,
            negative_prompt_embeds=negative_embeds,
            image=up1,
            strength=0.35,
            guidance_scale=7.0,
            num_inference_steps=20,
            generator=torch.Generator(
                device=device
            ).manual_seed(current_seed),
        ).images[0]

        # Pass 2
        print("  Hires pass 2/2 (detail sharpening)...")

        refined = img2img(
            prompt_embeds=prompt_embeds,
            negative_prompt_embeds=negative_embeds,
            image=pass1,
            strength=0.20,
            guidance_scale=6.0,
            num_inference_steps=15,
            generator=torch.Generator(
                device=device
            ).manual_seed(current_seed + 1),
        ).images[0]

        refined = rescale_cfg(refined, factor=0.7)

        hires_filename = (
            f"{image_name}_hires"
            if image_name
            else f"cetus_hires_{timestamp}"
        )

        hires_path = (
            f"output/{hires_filename}{suffix}.png"
        )

        refined.save(hires_path)

        print(f"Hires image saved: {hires_path}")

    else:
        refined = image
        hires_path = None
        print("Hires fix skipped")

    # ==========================================
    # PIXELIZATION
    # ==========================================
    # pixel_art = to_pixel_art(refined)

    # pixel_filename = (
    #     f"{image_name}_pixel"
    #     if image_name
    #     else f"pixel_art_{timestamp}"
    # )

    # pixelized_path = (
    #     f"output/{pixel_filename}{suffix}.png"
    # )

    # pixel_art.save(pixelized_path)

    # print(f"Pixelized image saved: {pixelized_path}")

    all_outputs.append({
        "seed": current_seed,
        "base": base_path,
        "hires": hires_path,
        #"pixel": pixelized_path,
    })

# ==========================================
# SUMMARY
# ==========================================
print("\nDone! Outputs saved:\n")

for i, out in enumerate(all_outputs, start=1):

    print(f"[Image {i}]")
    print(f"  Seed:      {out['seed']}")
    print(f"  Base:      {out['base']}")

    if out["hires"]:
        print(f"  Hires:     {out['hires']}")

    #print(f"  Pixelized: {out['pixel']}")
    print()