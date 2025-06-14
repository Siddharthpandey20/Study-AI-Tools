# 🧠 Smart Study Tool - AI-Powered Learning Platform

**Winner-Ready Hackathon Project** 🏆

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application
python run.py

# 3. Open browser
http://localhost:8000
```

## ✨ Features

### 🔥 1. Smart Revision Mode
- **Auto Flashcards**: AI-generated Q&A cards with difficulty levels
- **Interactive MCQs**: Quiz-style questions with instant feedback
- **Smart Explanations**: Detailed explanations for each answer

### 🧠 2. Mind Map Generator  
- **Visual Learning**: Convert notes into beautiful mind maps
- **Interactive Nodes**: Clickable, hierarchical topic structure
- **Color-Coded**: Different colors for different topic levels

### 🎯 3. Learning Path Generator
- **Step-by-Step**: Personalized learning sequences
- **Time Estimates**: Realistic time planning for each step
- **Prerequisites**: Clear dependency mapping

### 🎨 4. Smart Sticky Notes (🌟 USP Feature)
- **🔴 RED**: Must memorize (critical facts, formulas)
- **🟡 YELLOW**: Good to know (important concepts)  
- **🟢 GREEN**: Bonus/Extra (interesting additions)
- **AI Classification**: Automatic importance detection

### 🏆 5. Exam Booster Mode
- **Question Prediction**: Most likely exam questions
- **Probability Scores**: AI-calculated likelihood (0-100%)
- **Question Types**: Short answer, Long answer, HOTS
- **Smart Categories**: Visual badges for each type

## 🛠️ Tech Stack

- **Backend**: FastAPI + Python
- **AI Engine**: Google Gemini 1.5 Flash
- **File Processing**: PyPDF2, python-docx
- **Frontend**: Modern HTML5 + CSS3 + JavaScript
- **UI/UX**: Glassmorphism design with animations

## 📁 Supported File Formats

- PDF documents
- Word documents (.docx)
- Text files (.txt)
- Markdown files (.md)

## 🎨 Design Highlights

- **Glassmorphism UI**: Modern backdrop-blur effects
- **Smooth Animations**: Professional micro-interactions
- **Responsive Design**: Works on all devices
- **Color Psychology**: Strategic use of colors for learning
- **Interactive Elements**: Hover effects and transitions

## 🚀 API Endpoints

### Core Features
- `POST /api/generate-flashcards` - Generate flashcards
- `POST /api/generate-mcqs` - Create MCQ quizzes  
- `POST /api/generate-mindmap` - Build mind maps
- `POST /api/generate-learning-path` - Create study paths
- `POST /api/generate-sticky-notes` - Smart sticky notes
- `POST /api/generate-exam-questions` - Predict exam questions

### Utility
- `GET /docs` - Interactive API documentation
- `GET /api/health` - Health check
- `GET /api/supported-formats` - Supported file types

## 🏗️ Architecture

```
Smart Study Tool/
├── main.py              # FastAPI application
├── functions.py         # AI processing logic
├── requirements.txt     # Dependencies
├── run.py              # Startup script
├── templates/
│   └── index.html      # Frontend interface
├── static/             # Static assets
└── uploads/            # File uploads
```

## 🤖 AI Integration

- **Gemini 1.5 Flash**: Latest Google AI model
- **Intelligent Prompting**: Optimized prompts for education
- **Fallback System**: Works even without AI (graceful degradation)
- **Content Analysis**: Smart categorization and prioritization

## 🎯 Hackathon Winning Features

1. **🎨 Unique USP**: Color-coded sticky notes with AI classification
2. **📊 Data-Driven**: Probability scores for exam questions
3. **🎮 Interactive**: Game-like quiz interface with instant feedback
4. **🎭 Beautiful UI**: Professional design that impresses judges
5. **⚡ Fast Performance**: Optimized for real-time generation
6. **🛡️ Robust**: Error handling and fallback mechanisms

## 🚀 Demo Flow

1. **Upload**: Drag & drop study material
2. **Choose**: Select feature (flashcards, mind map, etc.)
3. **Generate**: AI processes content in seconds
4. **Interact**: Engage with beautiful, interactive results
5. **Study**: Use generated materials for effective learning

## 🏆 Why This Wins

- **Innovation**: First AI tool with color-coded study notes
- **Practicality**: Solves real student problems
- **Technology**: Cutting-edge AI integration
- **Design**: Professional, modern interface
- **Scalability**: Easy to extend and improve
- **Impact**: Can help millions of students worldwide

## 🚀 Future Enhancements

- [ ] Mobile app version
- [ ] Collaborative study rooms
- [ ] Progress tracking & analytics
- [ ] Integration with LMS platforms
- [ ] Voice-to-text note taking
- [ ] AR/VR mind map visualization

---

**Made with ❤️ for education and powered by AI** 🤖

*Ready to revolutionize how students learn!* 🎓
