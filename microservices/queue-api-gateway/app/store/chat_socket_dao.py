from typing import Optional, Dict
import pickle
from pathlib import Path
from websockets.legacy.server import WebSocketServerProtocol as WebSocketSession
from persona_sync_pylib.utils.singleton import singleton
from persona_sync_pylib.utils.minio_client import MinioClient

from ..utils.environment import SOCKET_SESSIONS_BUCKET, SOCKET_SESSIONS_TMP_DIR


@singleton
class ChatSocketDao:
    def __init__(self) -> None:
        self.__client = MinioClient()

    def get_socket_sessions(
        self, chat_id: str
    ) -> Optional[Dict[str, WebSocketSession]]:
        local_path = Path(f"{SOCKET_SESSIONS_TMP_DIR}/{chat_id}")

        try:
            self.__client.download_file(
                bucket_name=SOCKET_SESSIONS_BUCKET,
                object_name=chat_id,
                file_path=local_path,
            )
        except FileNotFoundError:
            return None

        if local_path.exists():
            with open(local_path, "rb") as f:
                return pickle.load(f)

    def upsert_socket_sessions(
        self, chat_id: str, socket_sessions: Dict[str, WebSocketSession]
    ) -> None:
        local_path = Path(f"{SOCKET_SESSIONS_TMP_DIR}/{chat_id}")

        with open(local_path, "wb") as f:
            pickle.dump(socket_sessions, f)

        self.__client.upload_file(
            bucket_name=SOCKET_SESSIONS_BUCKET,
            object_name=chat_id,
            file_path=local_path,
        )
