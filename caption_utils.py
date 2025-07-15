import streamlit as st
import os
import requests
from PIL import Image
from dotenv import load_dotenv
from transformers import BlipProcessor, BlipForConditionalGeneration

load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# Load BLIP model
@st.cache_resource
def load_blip_model():
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base", use_fast=False)
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    return processor, model

processor, model = load_blip_model()

# Extract raw BLIP description
def extract_blip_description(pil_image):
    inputs = processor(images=pil_image, return_tensors="pt")
    out = model.generate(**inputs)
    description = processor.decode(out[0], skip_special_tokens=True)
    return description

# Rephrase the description (fully grounded)
def rephrase_description(raw_desc):
    prompt = (
        f"The image shows: {raw_desc}\n\n"
        f"Rewrite this into a stylish yet 100% factual description. "
        f"Do NOT assume anything that is not visually obvious. "
        f"Avoid all references to night, neon lights, bars, cities, drinks, emotions, mood, or narrative. "
        f"Only describe what's clearly visible: person's clothing, pose, surroundings, lighting, objects, and setting style. "
        f"This will be used to generate grounded Instagram captions. No fiction."
    )

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "messages": [
            {"role": "system", "content": "You are a precise visual describer who creates stylish but strictly image-grounded summaries for social media."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5,
        "max_tokens": 200,
        "top_p": 0.9
    }

    response = requests.post("https://api.together.xyz/v1/chat/completions", headers=headers, json=data)

    try:
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception:
        raise RuntimeError(f"❌ Rephrasing failed: {response.text}")

# Generate tone-specific captions
def generate_captions(rephrased_prompt, tone, n_captions=3):
    tone_prompt_map = {
        "aesthetic": f"Write {n_captions} stylish yet visually grounded Instagram captions for: ",
        "funny": f"Write {n_captions} witty and grounded captions that reflect visible details for: ",
        "poetic": f"Write {n_captions} poetic but image-faithful captions that describe what’s clearly visible for: ",
        "travel": f"Write {n_captions} travel-inspired captions only if the visual setting supports it. Otherwise, focus on styling what's seen for: ",
        "hashtag-heavy": f"Write {n_captions} grounded Instagram captions with 5 relevant trending hashtags each for: ",
        "motivational": f"Write {n_captions} motivational captions grounded in the subject’s visible stance, pose, or expression for: ",
        "foodie": f"Write {n_captions} foodie captions only if food is clearly visible. Otherwise, skip food references and focus on visible aesthetics for: ",
        "romantic": f"Write {n_captions} romantic-style captions only if romantic cues are visible. Otherwise, focus on what's visually stylish and elegant for: ",
        "minimalist": f"Write {n_captions} minimalist, clean captions that reflect the visual simplicity of: ",
        "sarcastic": f"Write {n_captions} sarcastic or edgy captions grounded in visible clothing, expression, or vibe — no fiction — for: ",
        "song-lyrics": f"Write {n_captions} poetic, song-lyric-style captions only if the image evokes a clear aesthetic. Keep it grounded in what’s seen for: ",
    }

    prompt = (
        f"{tone_prompt_map.get(tone, tone_prompt_map['aesthetic'])}{rephrased_prompt}\n\n"
        f"Only generate captions that clearly match what's described above. "
        f"Avoid imaginative storytelling or metaphors. "
        f"The captions should reflect the person’s appearance, surroundings, and style — not assumed context."
    )

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "messages": [
            {"role": "system", "content": "You are a Gen-Z Instagram caption writer who only writes grounded, visual captions."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8,
        "max_tokens": 300,
        "top_p": 0.9
    }

    response = requests.post("https://api.together.xyz/v1/chat/completions", headers=headers, json=data)

    try:
        captions_raw = response.json()["choices"][0]["message"]["content"].strip().split("\n")
        captions = [cap.lstrip('-•*1234567890. ').strip() for cap in captions_raw if cap.strip()]
        return captions[:n_captions]
    except Exception:
        raise RuntimeError(f"❌ Caption generation failed: {response.text}")
