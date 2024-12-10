# utils/database/functions/users.py
import asyncpg
from datetime import datetime
from typing import List, Dict, Any, Optional, Union
from data.config import load_config

class Database:
   def __init__(self):
       self.pool: Union[asyncpg.Pool, None] = None

   async def create_pool(self):
       config = load_config()
       self.pool = await asyncpg.create_pool(
           user=config.db.user,
           password=config.db.password,
           host=config.db.host,
           database=config.db.database
       )

   async def get_users_count(self) -> int:
       try:
           return await self.pool.fetchval('SELECT COUNT(*) FROM users')
       except Exception as e:
           print(f"Error counting users: {e}")
           return 0

   async def get_today_users_count(self) -> int:
       try:
           query = "SELECT COUNT(*) FROM users WHERE DATE(created_at) = CURRENT_DATE"
           return await self.pool.fetchval(query)
       except Exception as e:
           print(f"Error counting today's users: {e}")
           return 0

   async def get_active_referrers_count(self) -> int:
       try:
           query = "SELECT COUNT(*) FROM users WHERE ref_count > 0"
           return await self.pool.fetchval(query)
       except Exception as e:
           print(f"Error counting active referrers: {e}")
           return 0

   async def get_top_referrers(self, limit: int = 5) -> List[Dict[str, Any]]:
       try:
           rows = await self.pool.fetch('''
               SELECT user_id, username, full_name, ref_count
               FROM users
               WHERE ref_count > 0
               ORDER BY ref_count DESC
               LIMIT $1
           ''', limit)
           return [dict(row) for row in rows]
       except Exception as e:
           print(f"Error getting top referrers: {e}")
           return []

   async def get_weekly_stats(self) -> Dict[str, int]:
       try:
           rows = await self.pool.fetch('''
               SELECT 
                   DATE(created_at) as date,
                   COUNT(*) as count
               FROM users
               WHERE created_at >= CURRENT_DATE - INTERVAL '7 days'
               GROUP BY DATE(created_at)
               ORDER BY date DESC
           ''')
           return {row['date'].strftime('%Y-%m-%d'): row['count'] for row in rows}
       except Exception as e:
           print(f"Error getting weekly stats: {e}")
           return {}

   async def get_all_users(self) -> List[Dict[str, Any]]:
       try:
           rows = await self.pool.fetch('''
               SELECT 
                   u1.user_id,
                   u1.username,
                   u1.full_name,
                   u1.created_at,
                   u1.referrer_id,
                   u1.ref_count,
                   u1.is_active,
                   u2.username as referrer_username
               FROM users u1
               LEFT JOIN users u2 ON u1.referrer_id = u2.user_id
               ORDER BY u1.created_at DESC
           ''')
           return [dict(row) for row in rows]
       except Exception as e:
           print(f"Error getting all users: {e}")
           return []

   async def add_user(self, user_id: int, username: str = None,
                     full_name: str = None, referrer_id: int = None) -> bool:
       try:
           # Avval user mavjudligini tekshirish
           user = await self.pool.fetchrow(
               'SELECT * FROM users WHERE user_id = $1',
               user_id
           )

           if not user:
               # Yangi user qo'shish
               await self.pool.execute('''
                   INSERT INTO users (user_id, username, full_name, referrer_id, created_at)
                   VALUES ($1, $2, $3, $4, $5)
               ''', user_id, username, full_name, referrer_id, datetime.now())

               # Agar referrer bo'lsa, uning ref_countini oshirish
               if referrer_id:
                   await self.pool.execute('''
                       UPDATE users 
                       SET ref_count = ref_count + 1
                       WHERE user_id = $1
                   ''', referrer_id)

           return True
       except Exception as e:
           print(f"Error adding user: {e}")
           return False

   async def get_user_referrals_count(self, user_id: int) -> int:
       """Foydalanuvchining referallari sonini olish"""
       try:
           sql = "SELECT ref_count FROM users WHERE user_id = $1"
           count = await self.pool.fetchval(sql, user_id)
           return count or 0
       except Exception as e:
           print(f"Error getting referrals count: {e}")
           return 0

   async def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
       """Foydalanuvchi ma'lumotlarini olish"""
       try:
           row = await self.pool.fetchrow(
               'SELECT * FROM users WHERE user_id = $1',
               user_id
           )
           return dict(row) if row else None
       except Exception as e:
           print(f"Error getting user: {e}")
           return None

db = Database()