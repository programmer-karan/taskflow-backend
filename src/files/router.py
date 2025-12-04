import uuid
from fastapi import APIRouter, Depends, HTTPException
from src.auth.dependencies import get_current_user
from src.auth.models import User
from src.shared.storage import create_presigned_url

router = APIRouter(prefix="/files", tags=["Files"])


@router.post("/presign")
def generate_upload_url(
    filename: str,
    content_type: str,
    current_user: User = Depends(get_current_user)
):
    # 1. Generate a unique filename to prevent overwrites
    # Example: "12/550e8400-e29b-...-avatar.png"
    unique_filename = f"{current_user.id}/{uuid.uuid4()}-{filename}"

    # 2. Generate URL
    presigned_url = create_presigned_url(
        object_name=unique_filename,
        content_type=content_type
    )

    if not presigned_url:
        raise HTTPException(
            status_code=500, detail="Could not generate upload URL")

    return {
        "upload_url": presigned_url,  # The frontend sends the file here
        # The frontend sends this string back to save in the Task
        "file_key": unique_filename
    }
