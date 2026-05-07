import random
import string
from typing import Optional
import redis.asyncio as redis
from app.core.config import settings

class AuthService:
    def __init__(self):
        self.redis = redis.from_url(settings.REDIS_URL)

    async def generate_otp(self, email: str) -> str:
        """Generate a 6-digit OTP and store it in Redis for 10 minutes."""
        otp = "".join(random.choices(string.digits, k=6))
        # Use a key format like "otp:user@example.com"
        await self.redis.set(f"otp:{email}", otp, ex=600)
        return otp

    async def verify_otp(self, email: str, otp: str) -> bool:
        """Verify the OTP from Redis."""
        stored_otp = await self.redis.get(f"otp:{email}")
        if stored_otp and stored_otp.decode() == otp:
            await self.redis.delete(f"otp:{email}")
            return True
        return False

auth_service = AuthService()
