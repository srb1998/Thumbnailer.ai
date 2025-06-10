# 🎨 ThumbnailGuru - AI YouTube Thumbnail Generator

> Create viral-worthy YouTube thumbnails in seconds using AI

[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-Visit_App-blue?style=for-the-badge)](https://thumbnailer-ai.vercel.app/)

![App Screenshot](https://raw.githubusercontent.com/srb1998/Thumbnailer.ai/dev/backend/app/uploads/UI.PNG)
![App Screenshot](https://raw.githubusercontent.com/srb1998/Thumbnailer.ai/dev/backend/app/uploads/UI2.PNG)

*🎥 [Demo Video - Work in Progress](https://your-demo-video-link.com)*

## ✨ What it does

- **AI-Powered**: Enter your video title → Get professional thumbnails
- **High Quality**: 1280x720 resolution, perfect for YouTube
- **Instant**: Generate thumbnails within 25 seconds
- **Smart**: Uses Google Gemini AI + OpenAI for optimized results

## 🛠️ Tech Stack

**Backend (FastAPI)**
- Python, FastAPI, PostgreSQL
- Google Gemini 2.0 (image generation)
- OpenAI GPT-4 (prompt optimization)
- Cloudinary (image storage)

**Frontend (React)**
- React, Modern UI
- Auto Theme Detection (follows your system dark/light mode)
- Deployed on Vercel

## 🚀 Quick Setup

### 1. Clone & Install
```bash
git clone https://github.com/yourusername/thumbnail-ai.git
cd thumbnail-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Setup
Create `.env` in backend folder:
```env
GEMINI_API_KEY=your_gemini_key
OPENAI_API_KEY=your_openai_key
CLOUDINARY_CLOUD_NAME=your_cloudinary_name
CLOUDINARY_API_KEY=your_cloudinary_key
CLOUDINARY_API_SECRET=your_cloudinary_secret
```

### 3. Run
```bash
# Backend
cd backend
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend  
cd frontend
npm install && npm start
```

Visit: `http://localhost:3000`

## 🚀 Deploy

**Backend**: Deployed FastAPI to Railway
**Frontend**: Already deployed on Vercel

## 📊 Features

- Unlimited free thumbnails
- Email delivery option
- User dashboard with analytics
- High Quality Thumbnail
- Cloud storage with CDN

## 🤝 Contributing

1. Fork the repo
2. Create feature branch: `git checkout -b feature/cool-feature`
3. Commit: `git commit -m 'Add cool feature'`
4. Push: `git push origin feature/cool-feature`
5. Open Pull Request

## 📞 Support

- **Live App**: [thumbnailer-ai.vercel.app](https://thumbnailer-ai.vercel.app/)
- **Issues**: [GitHub Issues](https://github.com/yourusername/thumbnail-ai/issues)

---

**Built with ❤️ by Sourabh**