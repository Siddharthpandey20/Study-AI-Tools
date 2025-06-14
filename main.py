from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import os
from functions import (
    generate_flashcards,
    generate_mcqs,
    create_mind_map,
    generate_learning_path,
    create_sticky_notes,
    generate_exam_questions,
    process_uploaded_file,
    classify_question_importance
)

# Add YouTube functions import
from youtubefunctions import (
    get_video_id,
    get_transcript,
    download_audio,
    transcribe_audio,
    summarize_transcript,
    generate_summary
)

# Add the import for document Q&A routes
from doc_qna_routes import create_doc_qna_routes

app = FastAPI(title="Smart Study Tool", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories if they don't exist
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Pydantic models
class TextInput(BaseModel):
    text: str

class FlashcardResponse(BaseModel):
    id: str
    question: str
    answer: str
    difficulty: str

class MCQResponse(BaseModel):
    id: str
    question: str
    options: List[str]
    correct_answer: int
    explanation: str
    difficulty: str

class MindMapNode(BaseModel):
    id: str
    label: str
    children: List['MindMapNode'] = []
    level: int
    color: str

class LearningStep(BaseModel):
    step_number: int
    title: str
    description: str
    estimated_time: str
    prerequisites: List[str]
    resources: List[str]

class StickyNote(BaseModel):
    id: str
    content: str
    category: str  # red, yellow, green
    priority: int
    tags: List[str]

class ExamQuestion(BaseModel):
    id: str
    question: str
    type: str  # short_answer, long_answer, hots
    probability_score: float
    difficulty: str
    keywords: List[str]

class VideoRequest(BaseModel):
    url: str

class VideoSummaryResponse(BaseModel):
    video_id: str
    title: str
    thumbnail: str
    summary: str
    source: str  # "transcript" or "audio"
    duration: Optional[str] = None

# Add document Q&A routes
app = create_doc_qna_routes(app)

# API Routes

@app.get("/", response_class=HTMLResponse)
async def get_homepage():
    """Serve the main application page"""
    try:
        if os.path.exists("templates/index.html"):
            with open("templates/index.html", "r", encoding="utf-8") as f:
                return HTMLResponse(content=f.read())
        else:
            # Return inline HTML if file doesn't exist
            return HTMLResponse(content=get_inline_html())
    except Exception as e:
        return HTMLResponse(content=get_inline_html())

def get_inline_html():
    """Return inline HTML when template file is not available"""
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Smart Study Tool</title></head>
    <body>
        <h1>Smart Study Tool API</h1>
        <p>API is running! Visit <a href="/docs">/docs</a> for API documentation.</p>
        <p>Upload your files using the API endpoints to generate study materials.</p>
    </body>
    </html>
    """

# 🔥 1. Smart Revision Mode Routes
@app.post("/api/generate-flashcards", response_model=List[FlashcardResponse])
async def create_flashcards(file: UploadFile = File(None), text: str = Form(None)):
    """Generate flashcards from uploaded file or text"""
    try:
        if file:
            content = await process_uploaded_file(file)
        elif text:
            content = text
        else:
            raise HTTPException(status_code=400, detail="Please provide either a file or text")
        
        flashcards = await generate_flashcards(content)
        return flashcards
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating flashcards: {str(e)}")

@app.post("/api/generate-mcqs", response_model=List[MCQResponse])
async def create_mcqs(file: UploadFile = File(None), text: str = Form(None)):
    """Generate MCQs from uploaded file or text"""
    try:
        if file:
            content = await process_uploaded_file(file)
        elif text:
            content = text
        else:
            raise HTTPException(status_code=400, detail="Please provide either a file or text")
        
        mcqs = await generate_mcqs(content)
        return mcqs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating MCQs: {str(e)}")

@app.get("/api/quiz/{quiz_id}")
async def get_quiz_interface(quiz_id: str):
    """Get quiz interface for a specific quiz"""
    return {"quiz_id": quiz_id, "status": "active"}

# 🧠 2. Mind Map Generator Routes
@app.post("/api/generate-mindmap", response_model=dict)
async def create_mindmap(file: UploadFile = File(None), text: str = Form(None)):
    """Generate interactive mind map from content"""
    try:
        if file:
            content = await process_uploaded_file(file)
        elif text:
            content = text
        else:
            raise HTTPException(status_code=400, detail="Please provide either a file or text")
        
        mindmap_data = await create_mind_map(content)
        return mindmap_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating mind map: {str(e)}")

@app.get("/api/mindmap/{map_id}")
async def get_mindmap(map_id: str):
    """Get specific mind map data"""
    return {"map_id": map_id, "status": "ready"}

# 🎯 3. Learning Path Generator Routes
@app.post("/api/generate-learning-path", response_model=List[LearningStep])
async def create_learning_path(file: UploadFile = File(None), text: str = Form(None)):
    """Generate step-by-step learning path"""
    try:
        if file:
            content = await process_uploaded_file(file)
        elif text:
            content = text
        else:
            raise HTTPException(status_code=400, detail="Please provide either a file or text")
        
        learning_path = await generate_learning_path(content)
        return learning_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating learning path: {str(e)}")

@app.get("/api/learning-path/{path_id}")
async def get_learning_path(path_id: str):
    """Get specific learning path"""
    return {"path_id": path_id, "status": "active"}

# 🎨 4. Context-Aware Sticky Notes Routes (USP Feature)
@app.post("/api/generate-sticky-notes", response_model=List[StickyNote])
async def create_smart_sticky_notes(file: UploadFile = File(None), text: str = Form(None)):
    """Generate color-coded sticky notes with smart categorization"""
    try:
        if file:
            content = await process_uploaded_file(file)
        elif text:
            content = text
        else:
            raise HTTPException(status_code=400, detail="Please provide either a file or text")
        
        sticky_notes = await create_sticky_notes(content)
        return sticky_notes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating sticky notes: {str(e)}")

@app.get("/api/sticky-notes/{note_id}")
async def get_sticky_note(note_id: str):
    """Get specific sticky note details"""
    return {"note_id": note_id, "status": "active"}

@app.put("/api/sticky-notes/{note_id}/category")
async def update_sticky_note_category(note_id: str, category: str):
    """Update sticky note category (red/yellow/green)"""
    return {"note_id": note_id, "category": category, "updated": True}

# 🔹 5. Exam Booster Mode Routes
@app.post("/api/generate-exam-questions", response_model=List[ExamQuestion])
async def create_exam_questions(file: UploadFile = File(None), text: str = Form(None)):
    """Generate most likely exam questions with probability scores"""
    try:
        if file:
            content = await process_uploaded_file(file)
        elif text:
            content = text
        else:
            raise HTTPException(status_code=400, detail="Please provide either a file or text")
        
        exam_questions = await generate_exam_questions(content)
        return exam_questions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating exam questions: {str(e)}")

@app.get("/api/exam-questions/by-type/{question_type}")
async def get_questions_by_type(question_type: str):
    """Get questions filtered by type (short_answer, long_answer, hots)"""
    return {"question_type": question_type, "status": "filtered"}

@app.get("/api/exam-questions/by-probability/{min_probability}")
async def get_questions_by_probability(min_probability: float):
    """Get questions with probability score above threshold"""
    return {"min_probability": min_probability, "status": "filtered"}

# 📺 6. YouTube Video Summarizer Routes
@app.post("/api/summarize-youtube", response_model=VideoSummaryResponse)
async def summarize_youtube_video(request: VideoRequest):
    """Summarize YouTube video from URL"""
    try:
        video_url = request.url
        video_id = get_video_id(video_url)

        if not video_id:
            raise HTTPException(status_code=400, detail="Invalid YouTube URL")

        # Get video info for thumbnail and title
        try:
            import yt_dlp
            ydl_opts = {'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                title = info.get('title', 'YouTube Video')
                thumbnail = info.get('thumbnail', f'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg')
                duration = info.get('duration_string', 'Unknown')
        except:
            title = 'YouTube Video'
            thumbnail = f'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg'
            duration = 'Unknown'

        # Try to get transcript first
        transcript = get_transcript(video_id)

        if transcript:
            summary = summarize_transcript(transcript)
            source = "transcript"
        else:
            try:
                audio_path = download_audio(video_url)
                transcript_text = transcribe_audio(audio_path)
                summary = generate_summary(transcript_text)
                source = "audio"
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Audio processing failed: {str(e)}")

        return VideoSummaryResponse(
            video_id=video_id,
            title=title,
            thumbnail=thumbnail,
            summary=summary,
            source=source,
            duration=duration
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")

@app.get("/api/video-info/{video_id}")
async def get_video_info(video_id: str):
    """Get video information including thumbnail"""
    try:
        import yt_dlp
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        ydl_opts = {'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
        return {
            "video_id": video_id,
            "title": info.get('title', 'YouTube Video'),
            "thumbnail": info.get('thumbnail', f'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg'),
            "duration": info.get('duration_string', 'Unknown'),
            "channel": info.get('uploader', 'Unknown Channel'),
            "view_count": info.get('view_count', 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching video info: {str(e)}")

# 📊 Analytics and Progress Routes
@app.get("/api/analytics/study-progress")
async def get_study_progress():
    """Get user's study progress analytics"""
    return {
        "flashcards_completed": 0,
        "mcqs_attempted": 0,
        "accuracy_rate": 0.0,
        "study_time": "0h 0m",
        "weak_areas": [],
        "strong_areas": []
    }

@app.get("/api/analytics/performance")
async def get_performance_metrics():
    """Get detailed performance metrics"""
    return {
        "weekly_progress": [],
        "subject_wise_performance": {},
        "difficulty_wise_accuracy": {},
        "time_spent_per_topic": {}
    }

# 🎮 Interactive Features Routes
@app.post("/api/quiz/submit-answer")
async def submit_quiz_answer(quiz_id: str, question_id: str, answer: int):
    """Submit quiz answer and get feedback"""
    return {
        "quiz_id": quiz_id,
        "question_id": question_id,
        "is_correct": True,  # This would be calculated
        "explanation": "Detailed explanation here",
        "next_question": "next_question_id"
    }

@app.post("/api/flashcard/mark-difficulty")
async def mark_flashcard_difficulty(flashcard_id: str, difficulty: str):
    """Mark flashcard as easy/medium/hard for spaced repetition"""
    return {
        "flashcard_id": flashcard_id,
        "difficulty": difficulty,
        "next_review": "2024-01-01T00:00:00Z"
    }

# 🔄 Utility Routes
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/api/supported-formats")
async def get_supported_formats():
    """Get list of supported file formats"""
    return {
        "supported_formats": [
            "pdf", "docx", "txt", "pptx", 
            "md", "html", "csv", "json"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)