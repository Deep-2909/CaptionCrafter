## 🖼️ CaptionCrafter 🖼️

**AI-Powered Image Caption Generator for Instagram**  
Generate stunning, stylish, and **visually-grounded** captions for your images using BLIP + LLMs.  
No hallucinations. Just real, aesthetic descriptions tailored to your vibe.

---

## 🚀 Features

- 🤖 **Visual Understanding with BLIP:** Automatically describe uploaded images.
- 🧠 **Grounded Rephrasing with Mixtral (via Together.ai):** Converts raw descriptions into factual, stylish summaries.
- ✍️ **Caption Generator:** Choose from tones like:
  - Aesthetic, Poetic, Funny, Motivational, Romantic, Minimalist, Sarcastic, etc.
- 🖼️ **Carousel Mode:** Upload multiple images — get a combined caption set that summarizes the entire vibe.
- 🎛️ **Streamlit Interface:** Sleek, dark-themed UI with tone selector, copy buttons & interactive output.

---

## 🗂️ Directory Structure
CaptionCrafter/
├── captioncrafter_app.py # Streamlit UI logic
├── caption_utils.py # BLIP + Together API logic
├── requirements.txt # Python dependencies
├── .env # Hidden file for API key
└── README.md # You're reading it!


---

## 🛠️ Setup Instructions:
1. Clone this repo

```bash
git clone https://github.com/Deep-2909/CaptionCrafter.git
cd CaptionCrafter
```

2. Install required packages
```bash
pip install -r requirements.txt
```

3. Add your Together API key
Create a .env file in the root directory:
**TOGETHER_API_KEY**=your_actual_api_key_here

4. Launch the app
```bash
streamlit run captioncrafter_app.py
```

**✨ How It Works**

**Image Input**: Upload 1 or more images via the Streamlit UI.
**BLIP Model**: Generates raw visual description per image.
**LLM Rephrasing (Mixtral via Together.ai)**: Refines the description into stylish, factual prose.
**Caption Generation**: Multiple caption styles are generated based on the selected tone.
**Copy Buttons**: Instantly copy any caption with one click.

## 🎨 Tones Supported

**Tone**	                                            **Description**
Aesthetic	                        Clean, minimal, Instagram-friendly vibes
Poetic	                            Deep, metaphorical yet grounded in visuals
Funny	                            Witty and quirky — but based on what’s visible
Motivational	                    Uplifting quotes inspired by the subject’s stance/pose
Minimalist	                        Sleek, one-line captions with elegance
Sarcastic	                        Edgy, Gen-Z tone with visual relevance
Romantic	                        Only when romance is visibly implied
Travel, Foodie	                    Auto-skip fiction if not visibly relevant
Hashtag-Heavy	                    Each caption has 5 trending hashtags
Song-Lyrics	                        Lyric-style captions that match the scene’s aesthetic

## 🧰 Built With

Streamlit
HuggingFace Transformers
Together.ai API
Salesforce BLIP
Python, PIL, Requests