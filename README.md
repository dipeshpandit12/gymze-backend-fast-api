# Gymze Backend (FastAPI) 💪  
🎯 **Project Overview**  
The FastAPI backend for the Gymze AI-powered gym companion processes videos to detect gym equipment using computer vision, enabling personalized workout creation based on available equipment.

---

## ✨ **Core Features**  

### **Video Processing System**  
- Accepts video URLs and user IDs via the `/process-video` endpoint.  
- Validates the successful upload of the video by communicating with the Next.js frontend.  
- Downloads the video and stores it in a temporary folder.  
- Extracts frames from the video to detect gym equipment using the Ultralytics YOLOv8 model.  
- Returns the following as a response:  
  - Unique detected equipment  
  - User ID  
  - Video URL  

### **Queue System**  
- Handles multiple requests by processing videos sequentially in a queue.  

### **Storage Optimization**  
- Deletes downloaded videos after processing to conserve storage space.  

---
## 🤖 **AI Model Development**  

### **YOLOv8 Custom Model**  
- **Dataset Preparation**:  
  - Annotated a dataset of 400 gym equipment images, covering a wide variety of equipment types and perspectives.  
- **Model Training**:  
  - Trained the YOLOv8 model using this annotated dataset.  
  - Achieved an accuracy of **60-70%**, sufficient for detecting gym equipment effectively in video frames.  
- **Key Features**:  
  - Real-time equipment detection.  
  - High accuracy for identifying unique gym equipment.  

---

## 🛠 **Tech Stack**  

### **Backend**  
- **FastAPI**: Backend framework for creating RESTful APIs.  
- **Python**: Core programming language.  
- **Ultralytics YOLOv8**: AI model for gym equipment detection.  

### **Frontend Integration**  
- **Next.js**: Frontend framework for seamless communication with the backend.  

### **Other Tools**  
- **FFmpeg**: For video frame extraction.  
- **Queue Management**: Ensures sequential video processing.  

---

## ⚙️ **Installation Guide**  

### **📦 Clone the Repository**  
```bash
git clone https://github.com/dipeshpandit12/gymze-backend-fast-api.git

```

## Environment Variables Setup

Create a `.env` file in the root directory with the following variables:

```properties
// /gymze-backend-fast-api/.env

# MongoDB Configuration
MONGODB_URI=XXXXXXXXXXXXXXXXXXXX

```

# 🏋️‍♂️ Gymze Next.js (Frontend Setup)

---

##  Explore the Repository

Click below to dive into the codebase and documentation:

🔗 **[Visit the Repository](https://github.com/dipeshpandit12/gymze)**

---
