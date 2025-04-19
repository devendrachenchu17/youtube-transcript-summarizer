import os
import streamlit as st
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from urllib.parse import urlparse, parse_qs
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google GenerativeAI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# List available models to verify access
try:
    available_models = genai.list_models()
    print("Available models:")
    for model in available_models:
        print(f"- {model.name}")
except Exception as e:
    print(f"Error listing models: {e}")

# Updated prompt for better results
PROMPT_TEMPLATE = """
Please analyze the following YouTube video transcript and provide a concise summary with:
1. Main topic and purpose (1-2 sentences)
2. 3-5 key points (as bullet points)
3. Any important facts, figures, or statistics mentioned
4. Overall conclusions or takeaways

Guidelines:
- Keep summary under 250 words
- Use neutral, academic tone
- Focus on factual content only
- Format with clear section headings

Transcript:
{transcript}
"""

def get_video_id(url):
    """Extract video ID from various YouTube URL formats"""
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            return parse_qs(query.query)['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    return None

def extract_transcript_details(youtube_video_url):
    try:
        video_id = get_video_id(youtube_video_url)
        if not video_id:
            st.error("⚠️ Invalid YouTube URL format")
            return None
            
        # Check available transcripts
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        if not transcript_list:
            st.warning("🔇 No transcripts available for this video")
            return None
            
        # Try to get English transcript first
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        except:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            
        return " ".join([i['text'] for i in transcript])
        
    except TranscriptsDisabled:
        st.error("❌ Transcripts are disabled for this video")
        return None
    except NoTranscriptFound:
        st.error("🔍 No transcripts found for this video")
        return None
    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")
        return None

def generate_gemini_content(transcript_text):
    try:
        # Initialize with the correct model name
        # Try different model naming formats
        model_names_to_try = [
            'gemini-1.5-pro-latest',  # Most recent model
            'gemini-pro',             # Standard name
            'models/gemini-pro'      # Fully qualified name
        ]
        
        model = None
        last_error = None
        
        for model_name in model_names_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                break
            except Exception as e:
                last_error = e
                continue
                
        if model is None:
            raise Exception(f"Could not load any model. Last error: {last_error}")
        
        # Configure safety settings
        safety_settings = {
            "HARM_CATEGORY_HARASSMENT": "BLOCK_ONLY_HIGH",
            "HARM_CATEGORY_HATE_SPEECH": "BLOCK_ONLY_HIGH",
            "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_ONLY_HIGH",
            "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_ONLY_HIGH"
        }
        
        # Generate content
        response = model.generate_content(
            PROMPT_TEMPLATE.format(transcript=transcript_text),
            safety_settings=safety_settings,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,
                top_p=0.95,
                top_k=40,
                max_output_tokens=2048
            )
        )
        
        return response.text
        
    except Exception as e:
        st.error(f"🚨 Generation failed: {str(e)}")
        return None

# Streamlit UI
st.set_page_config(
    page_title="YouTube AI Summarizer",
    page_icon="📺",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("📺 YouTube AI Summarizer")
st.caption("Generate concise summaries from YouTube video transcripts")

with st.sidebar:
    st.header("Settings")
    max_length = st.slider("Max summary length (words)", 100, 500, 250)
    temperature = st.slider("Creativity level", 0.0, 1.0, 0.3)

youtube_link = st.text_input(
    "Enter YouTube URL:",
    placeholder="https://www.youtube.com/watch?v=...",
    help="Paste any public YouTube video link"
)

if st.button("Generate Summary", type="primary"):
    if not youtube_link:
        st.warning("Please enter a YouTube URL")
        st.stop()
    
    with st.spinner("🔍 Extracting transcript..."):
        transcript = extract_transcript_details(youtube_link)
        
    if not transcript:
        st.stop()
    
    with st.spinner("🧠 Generating summary (this may take a minute)..."):
        summary = generate_gemini_content(transcript)
    
    if summary:
        st.success("✅ Summary generated successfully!")
        st.markdown("---")
        st.subheader("Summary")
        st.write(summary)
        
        # Download options
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "Download as TXT",
                data=summary,
                file_name="youtube_summary.txt",
                mime="text/plain"
            )
        with col2:
            st.download_button(
                "Download as MD",
                data=f"# YouTube Summary\n\n{summary}",
                file_name="youtube_summary.md",
                mime="text/markdown"
            )
    else:
        st.error("Failed to generate summary. Please try a different video or check your API key permissions.")

st.markdown("---")
st.caption("ℹ️ Note: Requires videos with available transcripts. Some content may be filtered by safety systems.")