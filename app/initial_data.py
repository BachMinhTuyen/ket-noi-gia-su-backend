from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import User, Role
from app.core.security import hash_password
import uuid

# Init roles (ASYNC)
async def create_initial_roles(db: AsyncSession):
    default_roles = ["Admin", "Tutor", "Student"]
    for role_name in default_roles:
        result = await db.execute(select(Role).filter(Role.roleName == role_name))
        exists = result.scalars().first()
        if not exists:
            new_role = Role(roleId=str(uuid.uuid4()), roleName=role_name)
            db.add(new_role)
    try:
        await db.commit()
        print("Roles created.")
    except Exception as e:
        print(f"Error occurred during commit: {e}")
        await db.rollback()

# Init admin account (ASYNC)
async def create_initial_admin(db: AsyncSession):
    username = "administrator"

    # Checking if the admin account already exists
    result = await db.execute(select(User).filter(User.username == username))
    existing_admin = result.scalars().first()

    if not existing_admin:
        result = await db.execute(select(Role).filter(Role.roleName == "Admin"))
        admin_role = result.scalars().first()

        if admin_role:
            new_admin = User(
                userId=str(uuid.uuid4()),
                username=username,
                password=hash_password("admin123"),
                fullName="Administrator",
                birthDate=None,
                phoneNumber="0000000000",
                address = "Vietnam",
                email="admin@example.com",
                avatarUrl = "https://res.cloudinary.com/dgl1kzmgc/image/upload/v1745341169/user_default.jpg",
                averageRating=5,
                roleId=admin_role.roleId,
                isVerified=True
            )
            db.add(new_admin)
            try:
                await db.commit()
                print("Admin user created.")
            except Exception as e:
                print(f"Error occurred during commit: {e}")
                await db.rollback()
        else:
            print("Role 'Admin' does not exist.")
    else:
        print("Admin account already exists.")
