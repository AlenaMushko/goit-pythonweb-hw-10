import cloudinary
import cloudinary.uploader
from cloudinary import CloudinaryImage
from cloudinary.utils import cloudinary_url

from src.conf.config import settings
from src.conf.constants import CLOUDINARY_AVATARS_FOLDER

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True,
)


class UploadFileService:
    @staticmethod
    def get_avatar_public_id(user_id: int) -> str:
        return f"{CLOUDINARY_AVATARS_FOLDER}/user_{user_id}"

    @staticmethod
    def upload_avatar(file_path: str, public_id: str) -> str:
        print(f"file_path: {file_path} public_id: {public_id}")
        
        try:
            response = cloudinary.uploader.upload(file_path, public_id=public_id, overwrite=True)
            return response.get("secure_url")

        except Exception as e:
            print("CLOUDINARY ERROR TYPE:", type(e))
            print("CLOUDINARY ERROR:", str(e))
            raise
        
    @staticmethod
    def delete_avatar(public_id: str) -> None:
        cloudinary.uploader.destroy(public_id, invalidate=True)
