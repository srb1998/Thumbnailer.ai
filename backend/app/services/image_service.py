import requests
import os
import os
import uuid
import time
import base64
import re
from typing import Optional, Dict
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from google import genai
from google.genai import types
from config import settings
from services.storage_service import CloudinaryStorage


class ImageService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.storage = CloudinaryStorage()
        os.makedirs("outputs", exist_ok=True)

        self.font_path_arial = "arial.ttf" # Consider making these configurable or checking existence
        self.font_path_impact = "impact.ttf"
        
        try:
            self.font = ImageFont.truetype(self.font_path_arial, 40)
            self.title_font = ImageFont.truetype(self.font_path_impact, 70) # Try to load Impact
            
        except IOError:
            print("Warning: Impact font not found. Falling back to default font.")
            self.title_font = ImageFont.load_default()
    
    async def generate_thumbnail_with_gemini(self, prompt: str, original_title: str) -> Dict:
        """Generate thumbnail using Gemini model - (gemini-2.0-flash-preview-image-generation)"""
        print("generate_thumbnail_with_gemini called")
        start_time = time.time()
        try:
            # key_words = self.extract_main_keywords(title)
            image_generation_request_prompt = f"""
                Create a 4k graphic like YouTube thumbnail image with these specifications:

                TECHNICAL SPECS:
                - Aspect Ratio: 16:9 (1280x720 pixels)
                - Style: Bold, vibrant, high-contrast YouTube thumbnail design
                - Quality: Ultra High-resolution, sharp focus, professional

                VISUAL CONTENT: {prompt}
            """

            print(f"prompt is - {image_generation_request_prompt}")

            response = self.client.models.generate_content(
                model="gemini-2.0-flash-preview-image-generation",
                contents=image_generation_request_prompt,
                config=types.GenerateContentConfig(
                      response_modalities=['TEXT','IMAGE']
                    )
            )
            print("Response received from Gemini")

            image_from_gemini_pil = None # Will hold the PIL Image object

            # Your existing logic to extract image data (which you said works)
            if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'inline_data') and part.inline_data is not None and hasattr(part.inline_data, 'data'):
                        
                        data = part.inline_data.data
                        decoded_data = None
                        if isinstance(data, bytes):
                            try:
                                decoded_data = base64.b64decode(data)
                            except base64.binascii.Error:
                                decoded_data = data
                        elif isinstance(data, str):
                            decoded_data = base64.b64decode(data)
                        else:
                            continue
                        
                        if decoded_data:
                            try:
                                image_from_gemini_pil = Image.open(BytesIO(decoded_data))
                                print(f"ImageService: Successfully created PIL Image. Size: {image_from_gemini_pil.size}")
                                break  # Exit loop once we have a valid image
                            except Exception as img_error:
                                print(f"ImageService: Failed to create PIL Image: {img_error}")
                                continue
                    
            if not image_from_gemini_pil:
                print("ImageService: No valid image could be processed from Gemini response.")
                return {"success": False, "error": "Failed to generate or process image from AI"}

            # Generate filename
            sanitized_title = re.sub(r'\W+', '_', original_title[:30])
            filename = f"thumbnail_{sanitized_title}_{uuid.uuid4().hex[:4]}.png"

            # Convert image to bytes for Cloudinary upload
            img_byte_array = BytesIO()
            image_from_gemini_pil.save(img_byte_array, format='PNG')
            img_bytes_for_upload = img_byte_array.getvalue()

            # Upload directly to Cloudinary
            print(f"ImageService: Uploading image to Cloudinary as '{filename}'...")
            upload_result = self.storage.upload_image_from_bytes(
                image_data=img_bytes_for_upload,
                filename=filename,
                folder="youtube-thumbnails"
            )

            if not upload_result.get("success"):
                error_msg = upload_result.get('error', 'Unknown Cloudinary error')
                print(f"ImageService: Cloudinary upload failed: {error_msg}")
                return {"success": False, "error": f"Cloudinary upload failed: {error_msg}"}

            print(f"ImageService: ✓ Successfully uploaded to Cloudinary: {upload_result.get('url')}")
            generation_time = time.time() - start_time
            
            return {
                "success": True,
                "image_url": upload_result.get("url"),
                "download_url": upload_result.get("download_url", upload_result.get("url")),
                "thumbnail_url": upload_result.get("thumbnail_url", upload_result.get("url")),
                "public_id": upload_result.get("public_id"),
                "generation_time": round(generation_time, 2),
            }

        except types.BlockedPromptException as bpe:
            error_message = "Content policy violation: Your prompt was blocked by the API."
            if hasattr(bpe, 'response') and bpe.response and hasattr(bpe.response, 'prompt_feedback') and bpe.response.prompt_feedback:
                 error_message += f" Reason: {bpe.response.prompt_feedback.block_reason_message or bpe.response.prompt_feedback.block_reason}"
            print(f"ImageService: Gemini prompt blocked by API exception: {error_message}")
            return {"success": False, "error": error_message}
        except Exception as e:
            print(f"ImageService: General error in generate_thumbnail_with_gemini: {e}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": str(e)}