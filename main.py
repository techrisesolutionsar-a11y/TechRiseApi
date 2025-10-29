from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import smtplib, ssl
import os
from dotenv import load_dotenv

app = FastAPI()

origins = [
    'http://localhost:3000',
    'https://techrisesolution.netlify.app'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def read_root():
    return {"Welcome API": "Welcome to API TECH RISE SOLUTIONS"}

@app.post("/email-contact")
def emailContact():
    load_dotenv()
    port = 465
    password = input("introduce la contraseña: ")
    sender_email = "techrisesolutionsar@gmail.com"
    context = ssl.create_default_context()
    message = "entrada de datos que ingrese el usuario"
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("techrisesolutionsar@gmail.com", os.getenv("PASWWORD_EMAIL"))
        server.sendmail(sender_email, sender_email, message)
    return {"email": "send email"}