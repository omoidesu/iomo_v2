from miniopy_async import Minio

from src.config import minio_endpoint, minio_access_key, minio_secret_key


class MinioClient:
    _client = Minio(minio_endpoint, access_key=minio_access_key, secret_key=minio_secret_key, secure=False)

    @classmethod
    def instance(cls) -> Minio:
        return cls._client
