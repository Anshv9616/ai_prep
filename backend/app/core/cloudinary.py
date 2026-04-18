import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

load_dotenv()


cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")

)

def upload_resume(file_path:str,user_id:int)->str:
    result=cloudinary.uploader.upload(
        file_path,
        resource_type="raw",
        folder=f"resumes/{user_id}",
        overwrite=True,
        public_id=f"resume_{user_id}"
    )
    return result["secure_url"]
    print(result["secure_url"])


def delete_resume(public_id: str):
    cloudinary.uploader.destroy(public_id, resource_type="raw")

