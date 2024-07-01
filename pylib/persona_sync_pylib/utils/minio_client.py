from minio import Minio, S3Error

from .environment import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY


class MinioClient:
    def __init__(self) -> None:
        self.__client = Minio(
            endpoint=MINIO_ENDPOINT,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=False,
        )

    def make_bucket_if_not_exists(self, bucket_name: str) -> None:
        if not self.__client.bucket_exists(bucket_name):
            self.__client.make_bucket(bucket_name)

    def upload_file(
        self, bucket_name: str, object_name: str, file_path: str, content_type: str
    ) -> None:
        self.__client.fput_object(
            bucket_name, object_name, file_path, content_type=content_type
        )

    def upload_file_if_not_exists(
        self, bucket_name: str, object_name: str, file_path: str, content_type: str
    ) -> None:
        self.make_bucket_if_not_exists(bucket_name)
        try:
            self.__client.stat_object(bucket_name, object_name)
        except S3Error:
            self.upload_file(bucket_name, object_name, file_path, content_type)

    def download_file(self, bucket_name: str, object_name: str, file_path: str) -> None:
        try:
            self.__client.fget_object(bucket_name, object_name, file_path)
        except S3Error:
            raise FileNotFoundError(
                f"File {object_name} not found in bucket {bucket_name}"
            )
