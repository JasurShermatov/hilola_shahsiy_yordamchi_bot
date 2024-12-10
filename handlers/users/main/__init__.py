# handlers/users/main/__init__.py
from .start import router as start_router
from .menu import router as menu_router
from .referral import router as referral_router

# Eski importni o'chirib tashlaymiz
# from handlers.users.main import start, referral, dispatch