import os
from dotenv import load_dotenv
load_dotenv()
url = os.getenv("SUPABASE_DB_URL")
print("URL in env:", url)
print("Using fallback?", not url)
from sqlalchemy import create_engine
engine = create_engine(url or "sqlite:///./dus.db")
with engine.connect() as conn:
    res = conn.execute("SELECT count(*) FROM categories")
    print("CATEGORIES:", res.fetchone()[0])
