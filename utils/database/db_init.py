import psycopg2
from data.config import load_config

config = load_config()



async def init_db():
    conn = psycopg2.connect(
        f"dbname='{config.db.user}' user='{config.db.user}' host='{config.db.host}' password='{config.db.password}' port='5432'"
    )
    cur = conn.cursor()
    try:
        cur.execute(
            """
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            user_id BIGINT UNIQUE,
            username VARCHAR(32),
            full_name VARCHAR(128),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            referrer_id BIGINT,
            ref_count INTEGER DEFAULT 0,
            is_active BOOLEAN DEFAULT TRUE
        );
        """
        )
        conn.commit()
    except psycopg2.Error as e:
        print(e)
    finally:
        conn.close()
