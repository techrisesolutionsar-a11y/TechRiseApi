from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import smtplib, ssl
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

@app.post("/email-contact", tags=["form"])
def emailContact(form: dict):
    load_dotenv()
    print(form["name"])
    port = 465
    sender_email = os.getenv("EMAIL_SENDER")
    recive_email = form["email"]
    context = ssl.create_default_context()
    message = MIMEMultipart("alternative")
    message["Subject"] = "TechRiseSolutions"
    message["From"] = sender_email
    message["To"] = recive_email
    text = """\
        Gracias por tú respuesta en la página de TechRiseSolution, nos pondremos en contacto contigo a la brevedad.
    """\
    
    html = """\
    <html>
        <body>
            <p>Gracias por tú mensaje, nos pondremos en contacto contigo a la brevedad.</p>
            <a href="https://techrisesolution.netlify.app">TechRiseSolutions</a>
            <br/><img alt="Tarjeta de presentación de TechRiseSolutions" width="800" height="400" src="https://ibb.co/fg3pbJQ"/>
        </body>
    </html>
    """\
    
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)
    messageForUs = MIMEMultipart("alternative")
    messageForUs["Subject"] = "TechRiseSolutions"
    messageForUs["From"] = sender_email
    messageForUs["To"] = sender_email
    htmlForUs = f"""\
    <html>
        <body>
            <h3>Nuevo Cliente:</h3>
            <p>Cliente: {form["name"]}</p>
            <p>Teléfono: {form["phone"]}</p>
            <p>Correo: {form["email"]}</p>
            <p>Servicio: {form["service"]}</p>
            <p>Detalles: {form["details"]}</p>
        </body>
    </html>
    """\
    
    messageForUsPart1 = MIMEText(htmlForUs, "html")
    messageForUs.attach(messageForUsPart1)
    
    
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, os.getenv("PASWWORD_EMAIL"))
        try:
            server.sendmail(sender_email, recive_email, message.as_string())
            server.sendmail(sender_email, sender_email, messageForUs.as_string())
            return {"status": True, "message": "Correo envíado con éxito."}
        except Exception as e:
            print(e)
            return {"status": False, "message": "No se pudo envíar el correo, intenta más tarde."}
    return {"email": "send email"}