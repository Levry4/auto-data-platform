
from minio import Minio
from pathlib import Path

# 1. Подключаемся к MinIO
client = Minio(
    "localhost:9010",
    access_key="devadmin",
    secret_key="LocalDevPassword2026",
    secure=False
)

# 2. Указываем bucket и файл
bucket_name = "auto-data-lake"
file_path = Path("data/raw/car_brands.json")
object_name = "raw/car_brands.json"

# 3. Проверяем, существует ли bucket
if not client.bucket_exists(bucket_name):
    raise RuntimeError(f"Bucket {bucket_name} не найден")

# 4. Загружаем файл
client.fput_object(
    bucket_name,
    object_name,
    str(file_path),
    content_type="application/json"
)

print(f"Файл {file_path} загружен в MinIO")