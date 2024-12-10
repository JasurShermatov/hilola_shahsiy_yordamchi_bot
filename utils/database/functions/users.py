from typing import Optional, List, Dict, Any, Union
import asyncpg


class Database:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def create_pool(self, config) -> None:
        """Initialize database connection pool"""
        self.pool = await asyncpg.create_pool(
            user=config.db.user,
            password=config.db.password,
            host=config.db.host,
            database=config.db.database,
        )

    async def close_pool(self) -> None:
        """Close the database connection pool"""
        if self.pool:
            await self.pool.close()

    async def add_user(
        self,
        user_id: Union[int, str],
        username: Optional[str] = None,
        full_name: Optional[str] = None,
        referrer_id: Optional[Union[int, str]] = None,
    ) -> bool:
        """
        Add a new user to the database. If the user exists, return True without modifications.
        Updates referrer's ref_count if a valid referrer_id is provided.
        """
        if not self.pool:
            raise RuntimeError("Database pool not initialized")

        # Convert user_id and referrer_id to integers
        try:
            user_id = int(user_id)
            referrer_id = int(referrer_id) if referrer_id else None
        except (TypeError, ValueError) as e:
            print(f"Error converting IDs to integers: {e}")
            return False

        async with self.pool.acquire() as conn:
            async with conn.transaction():
                try:
                    # Check if user exists
                    existing_user = await conn.fetchrow(
                        "SELECT id FROM users WHERE user_id = $1", user_id
                    )

                    if not existing_user:
                        # Add new user
                        await conn.execute(
                            """
                            INSERT INTO users (user_id, username, full_name, referrer_id)
                            VALUES ($1, $2, $3, $4)
                        """,
                            user_id,
                            username,
                            full_name,
                            referrer_id,
                        )

                        # Update referrer's count if provided
                        if referrer_id:
                            await conn.execute(
                                """
                                UPDATE users 
                                SET ref_count = ref_count + 1
                                WHERE user_id = $1
                            """,
                                referrer_id,
                            )

                    return True
                except Exception as e:
                    print(f"Error adding user: {e}")
                    return False

    async def get_users_count(self) -> int:
        """Get total number of users"""
        if not self.pool:
            raise RuntimeError("Database pool not initialized")

        async with self.pool.acquire() as conn:
            try:
                return await conn.fetchval("SELECT COUNT(*) FROM users")
            except Exception as e:
                print(f"Error counting users: {e}")
                return 0

    async def get_today_users_count(self) -> int:
        """Get number of users registered today"""
        if not self.pool:
            raise RuntimeError("Database pool not initialized")

        async with self.pool.acquire() as conn:
            try:
                query = (
                    "SELECT COUNT(*) FROM users WHERE DATE(created_at) = CURRENT_DATE"
                )
                return await conn.fetchval(query)
            except Exception as e:
                print(f"Error counting today's users: {e}")
                return 0

    async def get_active_referrers_count(self) -> int:
        """Get number of users who have referred others"""
        if not self.pool:
            raise RuntimeError("Database pool not initialized")

        async with self.pool.acquire() as conn:
            try:
                query = "SELECT COUNT(*) FROM users WHERE ref_count > 0"
                return await conn.fetchval(query)
            except Exception as e:
                print(f"Error counting active referrers: {e}")
                return 0

    async def get_top_referrers(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get top referrers ordered by ref_count"""
        if not self.pool:
            raise RuntimeError("Database pool not initialized")

        async with self.pool.acquire() as conn:
            try:
                rows = await conn.fetch(
                    """
                    SELECT id, user_id, username, full_name, ref_count
                    FROM users
                    WHERE ref_count > 0
                    ORDER BY ref_count DESC
                    LIMIT $1
                """,
                    limit,
                )
                return [dict(row) for row in rows]
            except Exception as e:
                print(f"Error getting top referrers: {e}")
                return []

    async def get_weekly_stats(self) -> Dict[str, str]:
        """Get user registration statistics for the last 7 days"""
        if not self.pool:
            raise RuntimeError("Database pool not initialized")

        async with self.pool.acquire() as conn:
            try:
                rows = await conn.fetch(
                    """
                    SELECT 
                        DATE(created_at) as date,
                        COUNT(*) as count
                    FROM users
                    WHERE created_at >= CURRENT_DATE - INTERVAL '7 days'
                    GROUP BY DATE(created_at)
                    ORDER BY date DESC
                """
                )
                return {str(row["date"]): str(row["count"]) for row in rows}
            except Exception as e:
                print(f"Error getting weekly stats: {e}")
                return {}

    async def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users with their referrer information"""
        if not self.pool:
            raise RuntimeError("Database pool not initialized")

        async with self.pool.acquire() as conn:
            try:
                rows = await conn.fetch(
                    """
                    SELECT 
                        u1.id, u1.user_id, u1.username, u1.full_name,
                        u1.created_at, u1.referrer_id, u1.ref_count,
                        u1.is_active, u2.username as referrer_username
                    FROM users u1
                    LEFT JOIN users u2 ON u1.referrer_id = u2.user_id
                    ORDER BY u1.created_at DESC
                """
                )
                return [dict(row) for row in rows]
            except Exception as e:
                print(f"Error getting all users: {e}")
                return []

    async def get_user_referrals_count(self, user_id: int) -> int:
        """Get number of referrals for a specific user"""
        if not self.pool:
            raise RuntimeError("Database pool not initialized")

        async with self.pool.acquire() as conn:
            try:
                return (
                    await conn.fetchval(
                        "SELECT ref_count FROM users WHERE user_id = $1", user_id
                    )
                    or 0
                )
            except Exception as e:
                print(f"Error getting referrals count: {e}")
                return 0

    async def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user details by user_id"""
        if not self.pool:
            raise RuntimeError("Database pool not initialized")

        async with self.pool.acquire() as conn:
            try:
                row = await conn.fetchrow(
                    """
                    SELECT 
                        id, user_id, username, full_name,
                        created_at, referrer_id, ref_count, is_active
                    FROM users 
                    WHERE user_id = $1
                """,
                    user_id,
                )
                return dict(row) if row else None
            except Exception as e:
                print(f"Error getting user: {e}")
                return None


db = Database()
