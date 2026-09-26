from typing import Dict, Set
from fastapi import WebSocket
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        # Map playlist_id to a set of active WebSocket connections
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, playlist_id: str):
        await websocket.accept()
        if playlist_id not in self.active_connections:
            self.active_connections[playlist_id] = set()
        self.active_connections[playlist_id].add(websocket)
        logger.info(f"Client connected to playlist {playlist_id}. Total: {len(self.active_connections[playlist_id])}")

    def disconnect(self, websocket: WebSocket, playlist_id: str):
        if playlist_id in self.active_connections:
            self.active_connections[playlist_id].discard(websocket)
            if not self.active_connections[playlist_id]:
                del self.active_connections[playlist_id]
            else:
                logger.info(f"Client disconnected from playlist {playlist_id}. Remaining: {len(self.active_connections[playlist_id])}")

    async def broadcast_to_playlist(self, playlist_id: str, message: dict):
        """Broadcast a message to all clients connected to a specific playlist."""
        if playlist_id in self.active_connections:
            dead_connections = set()
            for connection in self.active_connections[playlist_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    logger.error(f"Error broadcasting to client: {e}")
                    dead_connections.add(connection)
            
            for dead in dead_connections:
                self.disconnect(dead, playlist_id)

manager = ConnectionManager()
