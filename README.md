
# YouTube Video Transcript Summarizer

This project is a **Streamlit web app** that extracts transcripts from YouTube videos and summarizes them using the **Gemini Generative AI model**. It's designed to help users quickly understand the content of long videos without watching them entirely.

---

## Features

-  Input YouTube video URLs
-  Automatically extracts and summarizes video transcripts
- Supports multiple languages (if transcript available)
- Powered by Google Gemini Generative AI
- Clean and responsive user interface built with Streamlit
- Screenshot of interface included

---

## Demo

![App Interface](images/interface.png)

---

##Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **AI Model**: Gemini Generative API (Google)
- **APIs Used**: `youtube_transcript_api`, Gemini AI
- **Others**: dotenv, requests, and more

---

##Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Youtube-Transcript-Summarizer.git
cd Youtube-Transcript-Summarizer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your `.env` file

Create a `.env` file in the root directory and add your **Gemini API key**:

```env
GOOGLE_API_KEY=your_api_key_here
```

### 4. Run the Streamlit app

```bash
streamlit run app.py
```

---

## Project Structure

```
.
├── app.py                   # Main Streamlit application
├── requirements.txt         # Python dependencies
├── .env                     # API key (add this manually)
├── images/
│   └── interface.png        # UI screenshot
└── README.md                # Project documentation
```

---

## To-Do

- [ ] Add option for manual transcript input
- [ ] Support summarization of private/unlisted videos
- [ ] Improve error handling and loading animations
- [ ] Add download/export summary option

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss your ideas.

---

## License

[MIT License](LICENSE)

---

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [YouTube Transcript API](https://pypi.org/project/youtube-transcript-api/)
- [Google Gemini Generative AI](https://deepmind.google/technologies/gemini/)
