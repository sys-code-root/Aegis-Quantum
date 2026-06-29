import sqlite3
from datetime import datetime, timedelta
import time
import pandas as pd
import schedule

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute(
    "CREATE TABLE products (id INT, name TEXT, current_stock INT)"
)
cursor.execute(
    "CREATE TABLE sales (product_id INT, quantity INT, sale_date TEXT)"
)

cursor.executemany(
    "INSERT INTO products VALUES (?, ?, ?)"
    [(101, "Mechanical Keybord", 15), (102, "Gaming Hause", 80)],
)
cursor.executemany(

)