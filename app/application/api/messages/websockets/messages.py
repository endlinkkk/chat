from fastapi import WebSocket, WebSocketDisconnect, Depends, APIRouter
from fastapi.security import HTTPBearer
from punq import Container

from infra.websockets.managers import BaseConnectionManager
from logic.commands.messages import CreateMessageCommand, GetChatCommand
from logic.commands.permissions import AccessCheckUserCommand
from logic.exceptions.messages import ChatNotFoundException
from logic.init import init_container
from logic.mediator import Mediator


router = APIRouter(tags=["chats"])
http_bearer = HTTPBearer()


# WebSoket
@router.websocket("/{chat_oid}/")
async def websocket_endpoint(
    chat_oid: str,
    websocket: WebSocket,
    container: Container = Depends(init_container),
):
    connection_manager: BaseConnectionManager = container.resolve(BaseConnectionManager)
    mediator: Mediator = container.resolve(Mediator)

    token = websocket.headers.get("Authorization")
    if token is None or not token.startswith("Bearer "):
        await websocket.close(code=1008)
        return

    token = token.split(" ")[1]
    user, *_ = await mediator.handle_command(AccessCheckUserCommand(access_token=token))

    try:
        await mediator.handle_command(GetChatCommand(chat_oid=chat_oid))
    except ChatNotFoundException as error:
        await websocket.accept()
        await websocket.send_json(data={"error": error.message})
        await websocket.close()
        return

    await connection_manager.accept_connection(websocket=websocket, key=chat_oid)

    await websocket.send_text("You are now connected!")

    try:
        while True:
            message = await websocket.receive_text()
            await connection_manager.send_all(chat_oid, message.encode())
            await mediator.handle_command(
                CreateMessageCommand(text=message, chat_oid=chat_oid, user=user)
            )

    except WebSocketDisconnect:
        await connection_manager.remove_connection(websocket=websocket, key=chat_oid)
