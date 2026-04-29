from database import engine
from sqlalchemy import text

with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR(20) NOT NULL DEFAULT 'customer'"))
        conn.commit()
        print("role column added.")
    except Exception as e:
        print("Skipped (already exists):", e)
