# utils/database/functions/users.py

# Jadval yaratish
CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT PRIMARY KEY,
    username VARCHAR(255),
    full_name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    referrer_id BIGINT,
    referrer_username VARCHAR(255),
    ref_count INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE
);
"""

# Asosiy metodlar
async def create_tables(self):
    """Database jadvallarini yaratish"""
    try:
        await self.pool.execute(CREATE_USERS_TABLE)
    except Exception as e:
        print(f"Error creating tables: {e}")

async def add_user(self, user_id: int, username: str = None, full_name: str = None, referrer_id: int = None):
    """Yangi foydalanuvchi qo'shish"""
    try:
        sql = """
            INSERT INTO users (user_id, username, full_name, referrer_id)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (user_id) 
            DO UPDATE SET username = $2, full_name = $3
            RETURNING *
        """
        user = await self.pool.fetchrow(sql, user_id, username, full_name, referrer_id)
        return dict(user)
    except Exception as e:
        print(f"Error adding user: {e}")
        return None

async def get_user(self, user_id: int):
    """Foydalanuvchi ma'lumotlarini olish"""
    try:
        sql = "SELECT * FROM users WHERE user_id = $1"
        user = await self.pool.fetchrow(sql, user_id)
        return dict(user) if user else None
    except Exception as e:
        print(f"Error getting user: {e}")
        return None

async def get_all_users(self):
    """Barcha foydalanuvchilarni olish"""
    try:
        sql = "SELECT * FROM users ORDER BY created_at DESC"
        rows = await self.pool.fetch(sql)
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"Error getting all users: {e}")
        return []

async def get_users_count(self) -> int:
    """Jami foydalanuvchilar soni"""
    try:
        sql = "SELECT COUNT(*) FROM users"
        return await self.pool.fetchval(sql)
    except Exception as e:
        print(f"Error counting users: {e}")
        return 0

async def get_today_users_count(self) -> int:
    """Bugun qo'shilgan foydalanuvchilar soni"""
    try:
        sql = """
            SELECT COUNT(*) 
            FROM users 
            WHERE DATE(created_at) = CURRENT_DATE
        """
        return await self.pool.fetchval(sql)
    except Exception as e:
        print(f"Error counting today's users: {e}")
        return 0

async def get_top_referrers(self, limit: int = 5):
    """Top referrerlarni olish"""
    try:
        query = """
            SELECT user_id, username, full_name, ref_count
            FROM users
            WHERE ref_count > 0
            ORDER BY ref_count DESC
            LIMIT $1
        """
        rows = await self.pool.fetch(query, limit)
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"Error getting top referrers: {e}")
        return []

async def get_weekly_stats(self):
    """So'nggi 7 kunlik statistika"""
    try:
        query = """
            SELECT 
                DATE(created_at) as date,
                COUNT(*) as count
            FROM users
            WHERE created_at >= CURRENT_DATE - INTERVAL '7 days'
            GROUP BY DATE(created_at)
            ORDER BY date DESC
        """
        rows = await self.pool.fetch(query)
        return {
            row['date'].strftime('%Y-%m-%d'): row['count']
            for row in rows
        }
    except Exception as e:
        print(f"Error getting weekly stats: {e}")
        return {}

async def get_active_referrers_count(self) -> int:
    """Faol referral beruvchilar soni"""
    try:
        query = "SELECT COUNT(*) FROM users WHERE ref_count > 0"
        return await self.pool.fetchval(query)
    except Exception as e:
        print(f"Error counting active referrers: {e}")
        return 0