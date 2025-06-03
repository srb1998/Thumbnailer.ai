# app/routes/api.py
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from models.database import SessionLocal, Thumbnail, User, Analytics
from models.schemas import ThumbnailRequest, ThumbnailResponse
from services.ai_service import AIService
from services.image_service import ImageService
from services.email_service import EmailService
from services.storage_service import CloudinaryStorage
from datetime import datetime, timedelta
import time
import json

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

ai_service = AIService()
image_service = ImageService()
email_service = EmailService()
storage = CloudinaryStorage()
    
@router.post("/generate-thumbnail", response_model=ThumbnailResponse)
async def generate_thumbnail(
    request: ThumbnailRequest, 
    user_email: str = Query(None),
    db: Session = Depends(get_db)
):
    """Generate AI-powered YouTube thumbnail with full tracking"""
    start_time = time.time()
    print("Api called")    
    try:
        # Check daily limits for free users
        # if user_email:
        #     today = datetime.utcnow().date()
        #     daily_count = db.query(Thumbnail).filter(
        #         Thumbnail.user_email == user_email,
        #         func.date(Thumbnail.created_at) == today
        #     ).count()
            
        #     if daily_count >= 50:  # Free tier limit
        #         raise HTTPException(
        #             status_code=429, 
        #             detail="Daily limit reached. Please try again tomorrow."
        #         )
        
        # Generate optimized prompt
        prompt = ai_service.generate_thumbnail_prompt(
            request.title, 
            request.description
        )
        print("prompt is ",prompt)

        result = await image_service.generate_thumbnail_with_gemini(prompt=prompt, original_title=request.title)
        print(" result is ",result["success"])
        print(" result is ",result["image_url"])
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail="Failed to generate thumbnail")
        generation_time = time.time() - start_time
        
        return ThumbnailResponse(
            success=True,
            image_url=result["image_url"],  # Medium size for web
            download_url=result["download_url"],
            thumbnail_url=result["thumbnail_url"],
            prompt_used="",
            generation_time=round(generation_time, 2)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@router.get("/download/{thumbnail_id}")
async def download_thumbnail(thumbnail_id: int, db: Session = Depends(get_db)):
    """Get download URL and track download"""
    thumbnail = db.query(Thumbnail).filter(
        Thumbnail.id == thumbnail_id,
        Thumbnail.is_active == True
    ).first()
    
    if not thumbnail:
        raise HTTPException(status_code=404, detail="Thumbnail not found")
    
    # Increment download count
    thumbnail.download_count += 1
    db.commit()
    
    # Update user download count
    if thumbnail.user_email:
        user = db.query(User).filter(User.email == thumbnail.user_email).first()
        if user:
            user.total_downloads += 1
            db.commit()
    
    # Track analytics
    analytics = Analytics(
        thumbnail_id=thumbnail.id,
        action="download",
        user_email=thumbnail.user_email
    )
    db.add(analytics)
    db.commit()
    
    return {
        "download_url": thumbnail.download_url or thumbnail.image_url,
        "filename": f"{thumbnail.title[:50]}-thumbnail.jpg"
    }

@router.get("/user/{email}/dashboard")
async def get_user_dashboard(email: str, db: Session = Depends(get_db)):
    """Get user dashboard with stats and recent thumbnails"""
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        # Create user if doesn't exist
        user = User(email=email)
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # Get recent thumbnails
    recent_thumbnails = db.query(Thumbnail).filter(
        Thumbnail.user_email == email,
        Thumbnail.is_active == True
    ).order_by(desc(Thumbnail.created_at)).limit(10).all()
    
    # Get daily usage
    today = datetime.utcnow().date()
    daily_count = db.query(Thumbnail).filter(
        Thumbnail.user_email == email,
        func.date(Thumbnail.created_at) == today
    ).count()
    
    # Get popular genres
    genre_stats = db.query(
        Thumbnail.genre,
        func.count(Thumbnail.id).label('count')
    ).filter(
        Thumbnail.user_email == email
    ).group_by(Thumbnail.genre).order_by(desc('count')).limit(5).all()
    
    return {
        "user": {
            "email": user.email,
            "total_thumbnails": user.total_thumbnails,
            "total_downloads": user.total_downloads,
            "member_since": user.created_at.strftime("%B %Y"),
            "daily_usage": daily_count,
            "daily_limit": 50
        },
        "recent_thumbnails": [
            {
                "id": t.id,
                "title": t.title,
                "genre": t.genre,
                "thumbnail_url": t.thumbnail_url,
                "download_count": t.download_count,
                "created_at": t.created_at.isoformat()
            } for t in recent_thumbnails
        ],
        "genre_stats": [
            {"genre": genre, "count": count} for genre, count in genre_stats
        ]
    }

@router.get("/analytics/popular")
async def get_popular_content(db: Session = Depends(get_db)):
    """Get popular genres and trending content"""
    
    # Popular genres (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    popular_genres = db.query(
        Thumbnail.genre,
        func.count(Thumbnail.id).label('count')
    ).filter(
        Thumbnail.created_at >= thirty_days_ago
    ).group_by(Thumbnail.genre).order_by(desc('count')).limit(10).all()
    
    # Most downloaded thumbnails
    top_downloads = db.query(Thumbnail).filter(
        Thumbnail.created_at >= thirty_days_ago,
        Thumbnail.download_count > 0
    ).order_by(desc(Thumbnail.download_count)).limit(5).all()
    
    return {
        "popular_genres": [
            {"genre": genre, "count": count} for genre, count in popular_genres
        ],
        "trending_thumbnails": [
            {
                "title": t.title,
                "genre": t.genre,
                "downloads": t.download_count,
                "thumbnail_url": t.thumbnail_url
            } for t in top_downloads
        ]
    }

@router.get("/storage-stats")
async def get_storage_stats():
    """Get Cloudinary usage statistics"""
    stats = storage.get_usage_stats()
    return stats