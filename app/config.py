import os
from dotenv import load_dotenv
load_dotenv()
class C:
    SECRET_KEY=os.getenv("SECRET_KEY","x")
    ADMIN_TOKEN=os.getenv("ADMIN_TOKEN","x")
    NDAC_BASE_URL=os.getenv("NDAC_BASE_URL","http://localhost:5055")
    NDAC_TOKEN=os.getenv("NDAC_TOKEN","")
    NDAC_MOCK=os.getenv("NDAC_MOCK","1")=="1"
    SMTP_HOST=os.getenv("SMTP_HOST","")
    SMTP_PORT=int(os.getenv("SMTP_PORT","587"))
    SMTP_USER=os.getenv("SMTP_USER","")
    SMTP_PASS=os.getenv("SMTP_PASS","")
    FROM_ADDR=os.getenv("FROM_ADDR","ndac@example.com")
    DB_URL=os.getenv("DB_URL","sqlite:///ndac.db")
    POLL_INTERVAL_MIN=int(os.getenv("POLL_INTERVAL_MIN","60"))
    STAKEHOLDERS=os.getenv("STAKEHOLDERS","").split(",") if os.getenv("STAKEHOLDERS") else []
    TZ=os.getenv("TZ","Asia/Kolkata")