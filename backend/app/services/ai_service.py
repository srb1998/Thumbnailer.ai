import google.generativeai as genai
from config import settings
from typing import List, Dict
from openai import OpenAI

class AIService:
    def __init__(self):
        """Initialize AI service with Gemini and OpenAI clients"""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate_thumbnail_prompt(self, title: str, description: str) -> str:
        """Generate optimized prompt for thumbnail creation"""
          
        genre_styles = {
            "educational": "person pointing at screen/whiteboard, bright clean background, professional appearance, clear facial expression",
            "entertainment": "exaggerated facial expressions, bright colorful background, dynamic poses, high energy",
            "gaming": "character close-up, neon colors, action elements, gaming setup visible, excited expression",
            "tech": "product showcase, clean modern background, hands holding device, professional lighting",
            "lifestyle": "warm natural lighting, relatable person, cozy environment, genuine smile",
            "news": "serious professional appearance, clean background, authoritative pose, clear lighting",
            "comedy": "exaggerated surprised/laughing expression, bright colors, funny props, energetic pose",
            "horror": "dramatic shadows on face, dark atmosphere, suspenseful expression, mysterious elements",
            "documentary": "compelling subject focus, natural environment, authentic moment, good lighting",
            "tutorial": "person demonstrating, clear view of hands/process, bright lighting, focused composition",
            "review": "product prominently displayed, person with clear expression, comparison elements visible"
        }
        
        # Get genre-specific guidance
        # genre_guidance = genre_styles.get(genre.lower(), "clear subject focus, good lighting, engaging composition")

        prompt_for_llm = f"""
            You are an expert YouTube thumbnail designer. Based on the video info below, create a clear, vivid, cinematic image prompt for AI image generation.
            
            **Video details:**
            Title: "{title}"
            Description: "{description}"
            **Thumbnail style:**
            - One strong focal point (person, object, or scene)
            - Bright, high-contrast colors that stand out
            - Simple, clean background (not cluttered)
            - Dramatic or cinematic lighting
            - If showing people: expressive facial expression and dynamic pose
            - Camera angle (close-up, medium shot, or wide shot)
            - Include bold, readable text overlay with the title or main phrase, styled to pop (e.g., metallic, glitch, or vibrant colors), placed prominently but not blocking the focal point
            
            Write a 40-50 word detailed prompt describing the scene, colors, lighting, main subject, and the text overlay style and placement.
            
            Avoid clutter, small details, and muddy colors.
            
            Example: "Close-up of excited person pointing at glowing smartphone, bright studio lighting, vibrant blue background, shocked expression, dynamic pose. Bold white text overlay near bottom with metallic effect: 'Amazing Tech Revealed!'"
            Thumbnail prompt:
            """

        print("generate_thumbnail_prompt called")

        try:
            response = self.client.responses.create(
                model="gpt-4.1-mini",
                input=prompt_for_llm
            )
            print(f"Response from OpenAI: {response.output_text}")
            return response.output_text
        
        except Exception as e:
            print(f"exception is {e}")
            return f"Exception: Create a YouTube thumbnail for '{title}' style with bold text and vibrant colors"

    def analyze_thumbnail_effectiveness(self, title: str, genre: str) -> List[str]:
        """Provide suggestions for thumbnail improvement"""
        prompt = f"""
        Analyze this YouTube video and provide 5 specific suggestions for creating an effective thumbnail:
        
        Title: {title}
        Genre: {genre}
        
        Focus on:
        - Color psychology
        - Text readability
        - Visual hierarchy
        - Genre-specific elements
        - Click-through optimization
        
        Provide actionable, specific advice.
        """
        
        try:
            response = self.model.generate_content(prompt)
            suggestions = response.text.split('\n')
            return [s.strip('- ').strip() for s in suggestions if s.strip()][:5]
        except Exception as e:
            return [
                "Use contrasting colors for better visibility",
                "Include faces with strong emotions",
                "Add bold, readable text overlay",
                "Use the rule of thirds for composition",
                "Ensure mobile-friendly design"
            ]

    def generate_title_variations(self, original_title: str, genre: str) -> List[str]:
        """Generate alternative titles for A/B testing"""
        prompt = f"""
        Generate 3 alternative YouTube titles for this video:
        Original: {original_title}
        Genre: {genre}
        
        Make them:
        - More clickable
        - SEO optimized
        - Genre appropriate
        - Under 60 characters
        
        Return only the titles, one per line.
        """
        
        try:
            response = self.model.generate_content(prompt)
            titles = [t.strip() for t in response.text.split('\n') if t.strip()]
            return titles[:3]
        except Exception as e:
            return [original_title]