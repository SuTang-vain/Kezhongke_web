from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.models.user import User, UserCreate, UserRead, UserUpdate
from app.db.session import AsyncSessionLocal
import bcrypt

class UserService:
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

    async def create_user(self, user_create: UserCreate) -> User:
        async with AsyncSessionLocal() as session:
            # Auto-generate nickname from email if not provided
            nickname = user_create.nickname or user_create.email.split('@')[0]
            user = User(
                email=user_create.email,
                nickname=nickname,
                hashed_password=self.hash_password(user_create.password),
                is_active=user_create.is_active,
                is_verified=user_create.is_verified,
                role=user_create.role
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    async def get_user_by_email(self, email: str) -> User | None:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(User).where(User.email == email))
            return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            return result.scalar_one_or_none()

    async def update_user(self, user_id: UUID, user_update: UserUpdate) -> User | None:
        async with AsyncSessionLocal() as session:
            user = await self.get_user_by_id(user_id)
            if not user:
                return None
            
            # Need to get a fresh session-bound user object
            db_user = await session.get(User, user_id)
            
            update_data = user_update.model_dump(exclude_unset=True)
            if "password" in update_data:
                update_data["hashed_password"] = self.hash_password(update_data.pop("password"))
            
            for key, value in update_data.items():
                setattr(db_user, key, value)
            
            session.add(db_user)
            await session.commit()
            await session.refresh(db_user)
            return db_user

    def user_to_read(self, user: User) -> UserRead:
        return UserRead(
            id=user.id,
            email=user.email,
            nickname=user.nickname,
            avatar_url=user.avatar_url,
            bio=user.bio,
            is_active=user.is_active,
            is_verified=user.is_verified,
            role=user.role
        )

user_service = UserService()
