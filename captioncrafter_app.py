import streamlit as st
st.set_page_config(page_title="CaptionCrafter", layout="wide")
from PIL import Image
import html
from caption_utils import extract_blip_description, rephrase_description, generate_captions

# Custom CSS for styling
st.markdown("""
    <style>
        .caption-box {
            background-color: #1f1f2e;
            padding: 1rem;
            border-radius: 1rem;
            margin-bottom: 1.5rem;
            border-left: 5px solid #ff4b4b;
            transition: all 0.3s ease-in-out;
        }
        .caption-box:hover {
            background-color: #29293d;
            border-left: 5px solid #ff914d;
        }
        .caption-text {
            font-size: 1.1rem;
            color: #f0f0f0;
        }
        .reportview-container .main .block-container{
            padding-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# App Title
st.markdown("""
    <h1 style='text-align: center; color: #ff4b4b;'>🖼️ CaptionCrafter</h1>
    <h3 style='text-align: center; color: #cccccc;'>AI-Powered Image Caption Generator</h3>
""", unsafe_allow_html=True)
st.markdown("---")

# Sidebar Settings
st.sidebar.header("⚙️ Settings")
TONE_MAP = {
    "aesthetic": "Write {} short, stylish, aesthetic captions for: ",
    "funny": "Write {} funny Instagram captions for a photo of: ",
    "poetic": "Write {} poetic and deep captions about: ",
    "motivational": "Write {} inspiring and motivational captions for: ",
    "travel": "Write {} wanderlust-style captions for: ",
    "foodie": "Write {} witty foodie captions about: ",
    "romantic": "Write {} romantic captions for a photo of: ",
    "minimalist": "Write {} short and minimalist captions for: ",
    "sarcastic": "Write {} sarcastic and witty captions for a photo of: ",
    "song-lyrics": "Write {} captions that sound like emotional or aesthetic song lyrics for: ",
    "hashtag-heavy": "Write {} captions with 5 trending hashtags each for a photo of: "
}

col1, col2 = st.sidebar.columns(2)
tone = col1.selectbox("Tone", list(TONE_MAP.keys()), index=0)
mode = col2.radio("Mode", ["Single", "Carousel"])
n_captions = st.sidebar.slider("# Captions", 1, 5, 3)

st.sidebar.markdown("---")
st.sidebar.markdown("🖤 Built with Streamlit + Together.ai")

# Upload Section
st.markdown("### 📤 Upload Image(s)")
uploaded_files = st.file_uploader("Drag and drop or browse", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Generate Button
if st.button("🚀 Generate Captions"):
    if not uploaded_files:
        st.warning("Please upload at least one image.")
    else:
        st.markdown("---")
        st.subheader("🧠 Caption Results")

        if mode == "Single":
            for img_file in uploaded_files:
                st.image(Image.open(img_file), use_column_width=True)
                image = Image.open(img_file).convert("RGB")

                with st.spinner("Generating captions..."):
                    try:
                        raw_desc = extract_blip_description(image)
                        refined_desc = rephrase_description(raw_desc)
                        captions = generate_captions(refined_desc, tone, n_captions)
                    except Exception as e:
                        st.error(f"❌ Failed: {e}")
                        captions = []

                for cap in captions:
                    safe_cap = html.escape(cap)
                    st.markdown(f"""
                        <div class='caption-box'>
                           <div class='caption-text'>📝 {safe_cap}</div>
                            <button onclick="navigator.clipboard.writeText('{cap.replace("'", "\\'")}'); this.innerText='✅ Copied!';"
                                    style="margin-top: 0.5rem; background-color: #444; color: white; border: none; padding: 0.4rem 0.8rem; border-radius: 5px; cursor: pointer;">
                                📋 Copy
                            </button>
                        </div>
                    """, unsafe_allow_html=True)

        else:  # Carousel mode
            st.info("📸 You selected Carousel — captions will summarize all images together.")
            combined_descs = []
            images = []

            for img_file in uploaded_files:
                image = Image.open(img_file).convert("RGB")
                images.append(image)
                st.image(image, use_column_width=True)

            with st.spinner("Extracting visual descriptions from all images..."):
                for img in images:
                    try:
                        desc = extract_blip_description(img)
                        combined_descs.append(desc)
                    except Exception as e:
                        st.error(f"❌ Failed to extract description: {e}")

            if combined_descs:
                combined_text = " ".join(combined_descs)
                with st.spinner("Generating unified carousel captions..."):
                    try:
                        refined_desc = rephrase_description(combined_text)
                        captions = generate_captions(refined_desc, tone, n_captions)
                    except Exception as e:
                        st.error(f"❌ Failed to generate captions: {e}")
                        captions = []

                for cap in captions:
                    safe_cap = html.escape(cap)
                    st.markdown(f"""
                        <div class='caption-box'>
                           <div class='caption-text'>📝 {safe_cap}</div>
                            <button onclick="navigator.clipboard.writeText('{cap.replace("'", "\\'")}'); this.innerText='✅ Copied!';"
                                    style="margin-top: 0.5rem; background-color: #444; color: white; border: none; padding: 0.4rem 0.8rem; border-radius: 5px; cursor: pointer;">
                                📋 Copy
                            </button>
                        </div>
                    """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <hr style="margin-top: 3rem;">
    <div style='text-align: center; color: #777;'>Made with ❤️ by Deepanshu | Streamlit + Together.ai</div>
""", unsafe_allow_html=True)
