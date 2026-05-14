from fastapi import FastAPI
from api_routes import upload_file ,send_email
app=FastAPI()

@app.get("/")
def chek_health():
    return {
        "Message":"Healthy"
    }

app.include_router(upload_file.router)
app.include_router(send_email.router)