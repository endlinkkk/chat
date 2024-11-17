from fastapi import FastAPI
from application.api.users.handlers import router as auth_router
from application.api.messages.handlers import router as message_router
from application.api.moderator.handlers import router as moderator_router
from application.api.messages.websockets.messages import router as message_ws_router


def create_application() -> FastAPI:
    app = FastAPI(
        debug=True,
        title="ChatBridge",
        docs_url="/api/docs",
    )
    app.include_router(auth_router, prefix="/auth")
    app.include_router(message_router, prefix="/chats")
    app.include_router(moderator_router, prefix="/m/chats")
    app.include_router(message_ws_router, prefix='/chats')
    return app
