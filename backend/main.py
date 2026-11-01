from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# Database
from backend.database import Base, engine

# Models (important! Loads all table definitions)
import backend.models

# Routers
from backend.routers.projects import router as project_router
from backend.routers.requirements import router as requirement_router



# Create database tables
Base.metadata.create_all(bind=engine)

# FastAPI App
app = FastAPI(
    title="AI SDLC Accelerator",
    description="AI Powered SDLC Management Platform",
    version="1.0.0"
)

# Register Routers
app.include_router(project_router)
app.include_router(requirement_router)


# Home Page
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head>
            <title>AI SDLC Accelerator</title>
        </head>
        <body>
            <h1>AI SDLC Accelerator</h1>
            <p>Application Started Successfully</p>

            <h3>Quick Links</h3>

            <ul>
                <li>
                    <a href="/docs">Swagger API Documentation</a>
                </li>

                <li>
                    <a href="/projects">Projects API</a>
                </li>
            </ul>
        </body>
    </html>
    """