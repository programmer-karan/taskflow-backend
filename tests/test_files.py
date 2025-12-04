import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_presigned_url(client: AsyncClient):
    """
    Test that a logged-in user can request an upload URL.
    """
    # 1. Setup: Register & Login (Get Token)
    email = "files_test@example.com"
    password = "password123"

    await client.post("/auth/register", json={"email": email, "password": password})
    login_res = await client.post("/auth/token", data={"username": email, "password": password})
    token = login_res.json()["access_token"]

    # 2. Act: Request Presigned URL
    # Notice: Params go in the URL query string
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "filename": "avatar.png",
        "content_type": "image/png"
    }

    response = await client.post("/files/presign", params=params, headers=headers)

    # 3. Assert: Check success
    assert response.status_code == 200
    data = response.json()

    # Verify we got both keys back
    assert "upload_url" in data
    assert "file_key" in data

    # Verify the structure
    assert "http" in data["upload_url"]
    assert str(data["file_key"]).endswith("-avatar.png")

    # Verify the URL contains the MinIO bucket (from your logic)
    # Note: Boto3 generates a complex signed URL, we just check basics
    assert "X-Amz-Signature" in data["upload_url"]


@pytest.mark.asyncio
async def test_presign_unauthorized(client: AsyncClient):
    """
    Test that an anonymous user CANNOT generate URLs.
    """
    params = {
        "filename": "hacker.exe",
        "content_type": "application/x-msdownload"}
    response = await client.post("/files/presign", params=params)

    assert response.status_code == 401
