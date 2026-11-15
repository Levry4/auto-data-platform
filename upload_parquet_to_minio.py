
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
file_path = Path("data/processed/car_brands.parquet")
object_name = "processed/car_brands.parquet"

# 3. Проверяем наличие файла
if not file_path.exists():
    raise FileNotFoundError(f"Файл не найден: {file_path}")

# 4. Проверяем наличие bucket
if not client.bucket_exists(bucket_name):
    raise RuntimeError(f"Bucket {bucket_name} не найден")

# 5. Загружаем Parquet в MinIO
client.fput_object(
    bucket_name,
    object_name,
    str(file_path),
    content_type="application/vnd.apache.parquet"
)

print("Parquet загружен в MinIO")
print("Bucket:", bucket_name)
print("Объект:", object_name)
print("Размер:", file_path.stat().st_size, "байт")