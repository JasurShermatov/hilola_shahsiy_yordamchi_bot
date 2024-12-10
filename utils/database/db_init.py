from typing import final

import psycopg2
from datetime import datetime
from data.config import load_config

config = load_config()


async def init_db():
    conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='postgres' port='5432'")
    cur = conn.cursor()
    try:
        cur.execute("""
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
        """)
        conn.commit()
    except psycopg2.Error as e:
        print(e)
    finally:
        conn.close()

async def create_user(user_id, username, full_name, referrer_id, created_at=datetime.now(), ref_count=0, is_active=True):
    conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='postgres' port='5432'")
    cur = conn.cursor()
    try:
        # Using %s placeholders instead of .format()
        cur.execute(
            """
            INSERT INTO users (user_id, username, full_name, created_at, referrer_id, ref_count, is_active) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (user_id, username, full_name, created_at, referrer_id, ref_count, is_active)
        )
        conn.commit()
    except psycopg2.Error as e:
        print(e)
        conn.rollback()  # Added rollback on error
    finally:
        cur.close()     # Added cursor close
        conn.close()
