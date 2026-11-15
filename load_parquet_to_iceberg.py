
import pandas as pd

df = pd.read_parquet("data/processed/car_brands.parquet")

batch_size = 500
sql_statements = []

for start in range(0, len(df), batch_size):
    batch = df.iloc[start:start + batch_size]

    values = []
    for row in batch.itertuples(index=False):
        name = str(row.name).replace("'", "''")
        values.append(f"({int(row.id)}, '{name}')")

    sql_statements.append(
        "INSERT INTO iceberg.default.car_brands (id, name) VALUES\n"
        + ",\n".join(values)
        + ";"
    )

with open("/tmp/load_car_brands.sql", "w", encoding="utf-8") as f:
    f.write("\n".join(sql_statements))

print(f"Подготовлено строк: {len(df)}")
print(f"SQL-пакетов: {len(sql_statements)}")
print("SQL-файл: /tmp/load_car_brands.sql")

