import json
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path

# 1. Пути к файлам
json_path = Path("data/processed/car_brands_processed.json")
parquet_path = Path("data/processed/car_brands.parquet")

# 2. Читаем обработанный JSON
with json_path.open("r", encoding="utf-8") as file:
    data = json.load(file)

# 3. Преобразуем список словарей в таблицу
table = pa.Table.from_pylist(data)

# 4. Сохраняем таблицу в Parquet
pq.write_table(table, parquet_path, compression="snappy")

# 5. Проверяем результат
print("Количество строк:", table.num_rows)
print("Столбцы:", table.column_names)
print("Размер файла:", parquet_path.stat().st_size, "байт")

# 6. Читаем Parquet обратно для проверки
check_table = pq.read_table(parquet_path)
print("Повторное чтение успешно:", check_table.num_rows == table.num_rows)