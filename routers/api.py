from fastapi import FastAPI, UploadFile
from skincare import get_skin_care_routines

app = FastAPI()

@app.post("/skin-care-routines")
async def skin_care_routines(file: UploadFile, skin_type: str, skin_tone: str):
    return get_skin_care_routines(file, skin_type=skin_type, skin_tone=skin_tone)