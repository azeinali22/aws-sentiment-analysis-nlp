# 🎥 Intelligent Video Learning Dashboard (AWS + Flask + NLP)

This project is an end-to-end pipeline for building an **interactive video learning dashboard** powered by AWS and NLP. It allows students to explore course videos via **searchable transcripts**, **topic modeling**, and **key phrase extraction**, with a clean, Flask-based interface deployed on **EC2 Ubuntu**.

---

## 🔧 What It Does

✅ Extracts and normalizes transcripts from course videos using OpenAI’s Whisper  
✅ Extracts **key phrases** using RAKE and **topics** using LDA (Gensim)  
✅ Visualizes results in an interactive Flask dashboard  
✅ Supports **search by topic or phrase**, **watching videos**, and **word cloud generation**  
✅ Allows users to **download videos** directly  
✅ Hosted on AWS (S3 + EC2) with serverless processing logic

---

## 🛠 Technologies Used

| Layer | Tech Stack |
|------|-------------|
| 🧠 NLP | `Whisper`, `RAKE-NLTK`, `Gensim (LDA)` |
| ☁️ Cloud | `AWS S3`, `EC2 (Ubuntu)`, `Boto3` |
| 🧪 Data Processing | `NLTK`, `Pydub`, `FFmpeg`, `ThreadPoolExecutor` |
| 🖥️ Frontend | `Flask`, `Bootstrap`, `Jinja2`, `HTML5 video` |
| 🎨 Extras | `Matplotlib` (Word Cloud), `base64` encoding |

---

## 🚀 How It Works

### 1. Upload & Convert
- Upload `.mp4` course videos to an S3 bucket.
- Convert videos to `.wav` audio using `FFmpeg`.

### 2. Transcription (Whisper)
- Transcribe audio to text via `whisper` (OpenAI).
- Save raw transcriptions to S3 in JSON format.

### 3. Normalize & Process
- Normalize transcripts with `NLTK` (lowercase, lemmatize, stopword removal).
- Extract:
  - 🔑 **Key phrases** with RAKE
  - 🧠 **Topics** with LDA
- Save results to S3.

### 4. Flask Dashboard
- Searchable interface for phrases & topics.
- View associated videos with playback, phrases, topics, and word clouds.
- Highlight matched keywords.
- Enable download per video.

---

## 📊 Dashboard Preview

**Features:**
- 🔍 Full-text search on key phrases & topics
- 🎬 Embedded video player
- ☁️ Word cloud visualization
- 📥 Download button
- 📚 Display of extracted topics and key phrases

![screenshot](assets/dashboard.png)

---

## 🧠 NLP Example Output

```json
"Mod01_Course Overview": {
  "key_phrases": [
    "machine learning process", "amazon sagemaker", "natural language processing"
  ],
  "topics": [
    ["learning", "machine", "youll", "section", "data"],
    ["data", "skill", "model", "training", "problem"]
  ]
}
