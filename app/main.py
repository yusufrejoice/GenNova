from fastapi import FastAPI
# Triggering reload to apply new robustness fixes
from app.modules.auth.routes import router as auth_router
from app.modules.text_to_text.routes import router as text_to_text_router
from app.modules.text_to_image.routes import router as text_to_image_router
from app.modules.admin.routes import router as admin_router
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title="GenNova AI Platform API",
    description="Secure Authentication System for SaaS AI Platform",
    version="1.0.0"
)

# Include modules
app.include_router(auth_router)
app.include_router(text_to_text_router)
app.include_router(text_to_image_router)
app.include_router(admin_router)

@app.get("/")
def health_check():
    return {"status": "GenNova API is running", "version": "1.0.0"}
