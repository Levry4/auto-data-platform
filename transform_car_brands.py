
import json
from pathlib import Path
from minio import Minio

# 1. Подключаемся к MinIO
client = Minio(
    "localhost:9010",
    access_key="devadmin",
    secret_key="LocalDevPassword2026",
    secure=False
)

bucket_name = "auto-data-lake"

# 2. Читаем исходные данные
raw_path = Path("data/raw/car_brands.json")

with raw_path.open("r", encoding="utf-8") as file:
    data = json.load(file)

# 3. Преобразуем данные
car_brands = []

for car in data["Results"]:
    brand = {
        "id": car["Make_ID"],
        "name": car["Make_Name"]
    }
    car_brands.append(brand)

# 4. Проверяем качество данных
empty_names = 0
ids = []

for brand in car_brands:
    if not brand["name"]:
        empty_names += 1

    ids.append(brand["id"])

print("Всего записей:", len(car_brands))
print("Пустых названий:", empty_names)
print("Уникальных ID:", len(set(ids)))

# 5. Сохраняем обработанные данные локально
processed_path = Path("data/processed/car_brands_processed.json")
processed_path.parent.mkdir(parents=True, exist_ok=True)

with processed_path.open("w", encoding="utf-8") as file:
    json.dump(car_brands, file, ensure_ascii=False, indent=4)

# 6. Загружаем обработанные данные в MinIO
if not client.bucket_exists(bucket_name):
    raise RuntimeError(f"Bucket {bucket_name} не найден")

client.fput_object(
    bucket_name,
    "processed/car_brands_processed.json",
    str(processed_path),
    content_type="application/json"
)

print("Обработанные данные сохранены локально и загружены в MinIO")