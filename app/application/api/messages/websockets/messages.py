from fastapi import Depends
from fastapi import APIRouter
from fastapi import WebSocket
from punq import Container

from infra.websockets.managers import BaseConnectionManager
from logic.init import init_container


router = APIRouter(tags=["chats"])


# WebSoket
@router.websocket("/{chat_oid}/")
async def websocket_endpoint(
    chat_oid: str, websocket: WebSocket, container: Container = Depends(init_container)
):
    connection_manager: BaseConnectionManager = container.resolve(BaseConnectionManager)
