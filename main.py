from fastapi import FastAPI, HTTPException,BackgroundTasks
from pydantic import BaseModel
from ultralytics import YOLO
import os
import requests
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

uri =os.getenv("MONGODB_URI")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['users']
collection = db['videos']
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("Error while connecting:", e)

app = FastAPI()

model = YOLO("gymze-customized.pt")
latest_video_data = {}

class VideoData(BaseModel):
    userId: str
    videoUrl: str

def update_mongoDB(video_url: str, user_id: str, detected_objects: set):
    try:
        updated_document = collection.update_one(
            {
                "$and": [
                    {"userId": user_id},
                    {"videoUrl": video_url}
                ]
            },
            {
                "$push": {"detected_items": {"$each": list(detected_objects)}}
            },
            upsert=True  # Create the document if no matching document is found
        )

        if updated_document.matched_count == 0:
            print("No matching document found to update, a new document was created.")
        else:
            print("Document updated successfully.")

    except Exception as e:
        print(f"Error updating in MongoDB: {str(e)}")

def cleanup_temp_files():
    try:
        if os.path.exists("temp"):
            for file in os.listdir("temp"):
                file_path = os.path.join("temp", file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            os.rmdir("temp")
            print("Cleaned up temporary files")
    except Exception as e:
        print(f"Error during cleanup: {str(e)}")

def process_yolo_detection(video_url: str, user_id: str):
    try:
        # Create temp directory if it doesn't exist
        if not os.path.exists("temp"):
            os.makedirs("temp")

        # Download the video if it's a URL
        if video_url.startswith("http"):
            video_path = os.path.join("temp", os.path.basename(video_url))
            response = requests.get(video_url)
            with open(video_path, "wb") as f:
                f.write(response.content)
        else:
            video_path = video_url

        # Run YOLO model on the video
        results = model(video_path, stream=True)

        # Extract detected objects
        detected_objects = []
        try:
            for result in results:
                for box in result.boxes:
                    detected_objects.append({
                        "class": result.names[int(box.cls[0].item())],  # Convert class index
                        "confidence": float(box.conf[0].item()),        # Convert confidence score
                        "coordinates": box.xyxy[0].tolist()            # Convert coordinates
                    })
        except IndexError as ie:
            print(f"Error extracting box data: {str(ie)}")
            return []

        # Log detected objects
        if detected_objects:
            unique_objects = {obj["class"] for obj in detected_objects}
            print(f"UserID: {user_id}, Detected Objects: {unique_objects}")
            update_mongoDB(video_url, user_id,unique_objects)
        else:
            print(f"No objects detected for UserID: {user_id}")
        cleanup_temp_files()
        return detected_objects

    except Exception as e:
        print(f"Error processing YOLO detection: {str(e)}")
        cleanup_temp_files()
        return []


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}



@app.post("/process-video/")
async def process_video(data: VideoData, background_tasks: BackgroundTasks):
    try:
        global latest_video_data
        latest_video_data = {
            "userId": data.userId,
            "videoUrl": data.videoUrl
        }
        background_tasks.add_task(process_yolo_detection, data.videoUrl, data.userId)
        return {"status": "ok", "message": "Video processed successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the video")
