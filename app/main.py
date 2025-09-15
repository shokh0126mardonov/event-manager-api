from fastapi import FastAPI

from .database import Base, engine
from .models import users

from .dependencies import get_db

from .routers.users import router as users_router
from .routers.events import router as events_router
from .routers.venues import router as venues_router
from .routers.tickets import router as tickets_router
from .routers.orders import router as orders_router


app = FastAPI(title="Event Manager API")

Base.metadata.create_all(engine)

app.include_router(users_router)
app.include_router(events_router)
app.include_router(venues_router)
app.include_router(tickets_router)
app.include_router(orders_router)
