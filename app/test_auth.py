import asyncio
from app.auth.telegram_auth import send_code, verify_code


async def test():
    phone = "+905063308318"
    session_name = "user_test"

    await send_code(phone, session_name)

    code = input("Enter code: ")
    await verify_code(phone, code)

    print("AUTH SUCCESS")


if __name__ == "__main__":
    asyncio.run(test())
