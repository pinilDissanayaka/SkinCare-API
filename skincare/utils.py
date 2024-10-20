import os 
import base64
from dotenv import load_dotenv
from fastapi import UploadFile, status, HTTPException
from groq import Groq


load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")


def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

def save_img_locally(uploaded_file: UploadFile):
    try:
        with open(uploaded_file.filename, "wb") as buffer:
            buffer.write(uploaded_file.file.read())
        return uploaded_file.filename
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))




def get_skin_care_routines(uploaded_file: UploadFile, skin_type:str, skin_tone:str):
    
    try:
        image_path = save_img_locally(uploaded_file)

        base64_image = encode_image(image_path)

        client = Groq()
        
        prompt=f"""
        You are a highly skilled AI dermatologist with expertise in personalized skincare. 
        You are provided with an image of a person's skin condition, along with information about their skin type (e.g., oily, dry, combination, or sensitive) 
        and skin tone (e.g., fair, medium, dark). Analyze the image and take into account the skin type and tone while diagnosing the skin disease. 
        After identifying the skin condition, provide a detailed diagnosis including the name of the disease, its symptoms, and any relevant characteristics.
        Following the diagnosis, create a tailored skincare routine that factors in the individual’s skin type and tone. The routine should include:
            Daily steps (cleanser, moisturizer, sunscreen, etc.).
            Specific product recommendations (e.g., ingredients to look for or avoid).
            Adjustments based on the individual's skin type and tone.
            Lifestyle tips to help manage and improve skin health, as well as any precautions to avoid irritation or worsening of the condition.
        Information:
            Skin type: {skin_type}
            Skin tone: {skin_tone}
        Start with the diagnosis and follow with the skincare routine.
        """
        

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            model="llava-v1.5-7b-4096-preview",
        )

        return chat_completion.choices[0].message.content
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    finally:
        if os.path.exists(image_path):
            os.remove(image_path)