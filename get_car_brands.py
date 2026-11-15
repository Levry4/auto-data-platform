
import requests as rq
import json

# 1. Получаем данные из API
url = "https://vpic.nhtsa.dot.gov/api/vehicles/GetAllMakes?format=json"

response = rq.get(url)
response.raise_for_status()

data = response.json()

# 2. Сохраняем исходные данные
with open("data/raw/car_brands.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print("Исходные данные сохранены")