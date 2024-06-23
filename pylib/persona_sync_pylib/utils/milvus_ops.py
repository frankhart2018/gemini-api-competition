from pymilvus import MilvusClient

from .environment import MILVUS_HOST, EMBEDDING_SIZE


class MilvusConnection:
    def __init__(self, collection_name: str) -> None:
        self.__client = MilvusClient(uri=MILVUS_HOST)
        self.__client.create_collection(
            collection_name=collection_name, dimension=EMBEDDING_SIZE
        )

    def get_client(self) -> MilvusClient:
        return self.__client
