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
                        print("ImageService: Found inline_data with a 'data' attribute.")
                        data = part.inline_data.data
                        print(f"ImageService: Data type from Gemini: {type(data)}, Length: {len(data)}")

                        decoded_data = None
                        if isinstance(data, bytes):
                            try: # Try decoding as base64 first
                                decoded_data = base64.b64decode(data)
                                print(f"ImageService: Decoded base64 bytes. Length: {len(decoded_data)}")
                            except base64.binascii.Error: # If not base64, assume raw bytes
                                print("ImageService: Data is bytes, but not base64. Assuming raw image bytes.")
                                decoded_data = data
                        elif isinstance(data, str): # If it's a string, assume base64 string
                            decoded_data = base64.b64decode(data)
                            print(f"ImageService: Decoded base64 string. Length: {len(decoded_data)}")
                        else:
                            print(f"ImageService: Data is of unexpected type: {type(data)}")
                            continue # Skip this part

                        if decoded_data:
                            try:
                                image_from_gemini_pil = Image.open(BytesIO(decoded_data))
                                image_from_gemini_pil = image_from_gemini_pil.convert("RGB") # Ensure RGB
                                print(f"ImageService: ✓ Image opened with Pillow: {image_from_gemini_pil.size}, format: {image_from_gemini_pil.format}")
                                break # Found and opened the image
                            except Exception as e_pil:
                                print(f"ImageService: Error opening image with Pillow: {e_pil}")
                                image_from_gemini_pil = None # Reset
                                continue # Try next part if any
                    # else:
                        # print("ImageService: Part has no inline_data or no data attribute, or inline_data is None.")
            
            if not image_from_gemini_pil:
                print("ImageService: No valid image could be processed from Gemini response.")
                return {"success": False, "error": "Failed to generate or process image from AI"}

            # *** CRITICAL CHANGE FOR TEXT OVERLAY - START ***
            print(f"ImageService: Preparing text overlay for title: '{original_title}'")
            text_for_overlay = self.extract_main_keywords(original_title=original_title, text_input=original_title, max_words=5)
            print(f"ImageService: Text extracted for overlay: '{text_for_overlay}'")

            # Add text to the image using Pillow. Make a copy to avoid modifying the original if needed elsewhere.
            image_with_text_overlay_pil = self.add_text_to_image(image_from_gemini_pil.copy(), text_for_overlay, title=True)
            print("ImageService: ✓ Text overlay added to image.")
            # *** CRITICAL CHANGE FOR TEXT OVERLAY - END ***

            # Generate filename (using a sanitized title base for better readability)
            sanitized_title = re.sub(r'\W+', '_', original_title[:30])
            filename = f"thumbnail_{sanitized_title}_{uuid.uuid4().hex[:8]}.png"

            # Optional: Save the image WITH TEXT locally for debugging
            # local_filepath_with_text = os.path.join("outputs", filename)
            # try:
            #    image_with_text_overlay_pil.save(local_filepath_with_text)
            #    print(f"ImageService: Image WITH TEXT saved locally to: {local_filepath_with_text}")
            # except Exception as e_save:
            #    print(f"ImageService: Error saving image with text locally: {e_save}")


            # Convert the image WITH TEXT to bytes for Cloudinary upload
            img_byte_array_with_text = BytesIO()
            image_with_text_overlay_pil.save(img_byte_array_with_text, format='PNG') # Save the modified image
            img_bytes_for_upload = img_byte_array_with_text.getvalue()

            # Upload to Cloudinary
            print(f"ImageService: Uploading image WITH TEXT to Cloudinary as '{filename}'...")
            upload_result = self.storage.upload_image_from_bytes(
                image_data=img_bytes_for_upload, # Use the bytes of the image with text
                filename=filename,
                folder="youtube-thumbnails"
            )

            if not upload_result.get("success"): # Check for success key more reliably
                error_msg = upload_result.get('error', 'Unknown Cloudinary error')
                print(f"ImageService: Cloudinary upload failed: {error_msg}")
                # No fallback to local file URL here unless you specifically want to serve unprocessed local files
                return {"success": False, "error": f"Cloudinary upload failed: {error_msg}"}

            print(f"ImageService: ✓ Successfully uploaded to Cloudinary: {upload_result.get('url')}")
            generation_time = time.time() - start_time
            
            return {
                "success": True,
                "image_url": upload_result.get("url"), # URL of the image with text
                "download_url": upload_result.get("download_url", upload_result.get("url")),
                "thumbnail_url": upload_result.get("thumbnail_url", upload_result.get("url")),
                "public_id": upload_result.get("public_id"),
                "generation_time": round(generation_time, 2),
                # "cloudinary_bytes": upload_result.get("bytes", 0) # If available
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
        
    # This is a synchronous function, no 'async' needed
    def add_text_to_image(self, image: Image.Image, text: str, title: bool = False) -> Image.Image:
        """Add high-impact text overlay like professional YouTube thumbnails"""
        draw = ImageDraw.Draw(image)

        # Use larger, bolder fonts for YouTube
        font_size = 90 if title else 60  # Increased sizes
        try:
            # Try to load Roboto font (best for YouTube)
            font_to_use = ImageFont.truetype("fonts/Roboto.ttf", font_size)
        except:
            try:
                # Fallback to Arial Bold
                font_to_use = ImageFont.truetype("arialbd.ttf", font_size)
            except:
                font_to_use = ImageFont.load_default()

        # YouTube-style colors: White text with dark outline
        text_color = (255, 255, 255)  # Pure white
        stroke_color = (0, 0, 0)      # Pure black
        stroke_width = 4 if title else 3  # Thicker outline

        # Get text dimensions
        try:
            text_box = draw.textbbox((0, 0), text, font=font_to_use, stroke_width=stroke_width)
            text_width = text_box[2] - text_box[0]
            text_height = text_box[3] - text_box[1]
        except AttributeError:
            text_width, text_height = draw.textsize(text, font=font_to_use)

        image_width, image_height = image.size

        # Position text in upper third (YouTube best practice)
        x = (image_width - text_width) / 2
        y = image_height * 0.15  # Top 15% area

        # Ensure text fits within bounds
        if y + text_height > image_height * 0.4:  # Don't go below 40% height
            y = image_height * 0.4 - text_height

        # Add text with outline
        draw.text((x, y), text, font=font_to_use, fill=text_color, 
                  stroke_width=stroke_width, stroke_fill=stroke_color)

        return image

    def extract_main_keywords(self, original_title: str, text_input: str, max_words: int = 3) -> str:
        """Extract 2-3 powerful words for YouTube thumbnail overlay"""

        # Power words that work well in thumbnails
        power_words = {'secret', 'hidden', 'revealed', 'shocking', 'amazing', 'incredible', 
                      'ultimate', 'best', 'worst', 'new', 'leaked', 'exposed', 'truth'}

        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                     'of', 'with', 'by', 'how', 'why', 'what', 'when', 'where', 'is', 'are'}

        words = re.findall(r"[a-zA-Z0-9']+", original_title.lower())

        # Prioritize power words and longer words
        key_words = []
        for word in words:
            if word not in stop_words and len(word) > 3:
                if word in power_words:
                    key_words.insert(0, word.upper())  # Power words first, in CAPS
                else:
                    key_words.append(word.capitalize())

        # Take best 2-3 words
        selected = key_words[:max_words]
        result = ' '.join(selected)

        # If result is too long, shorten it
        if len(result) > 25:
            result = ' '.join(selected[:2])

        return result if result else original_title.split()[0].upper()