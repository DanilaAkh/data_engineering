from db_connection import connect_db
import json
import csv

def parse_data(file_name):
    with open(file_name, "r", encoding="UTF-8") as f:
        items = []
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            row["price"] = float(row["price"])
            row["quantity"] = int(row["quantity"])
            if row["views"] is None:
                row["views"] = int(row["isAvailable"])
                row["isAvailable"] = row["fromCity"]
                row["fromCity"] = row["category"]
                row["category"] = "no"
            items.append(row)
        return items


def create_table(db):
    cursor = db.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS task4
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT,
            price       FLOAT,
            quantity    INTEGER,
            category    TEXT,
            fromCity    TEXT,
            isAvailable TEXT,
            views       INTEGER,
            updated     INTEGER NOT NULL DEFAULT(0)
        )       
        """)
    cursor.close()

        
def insert_data_to_table(db, data):
    cursor = db.cursor()    
    cursor.executemany("""
                    INSERT INTO task4 
                    (
                        name,    
                        price,      
                        quantity,   
                        category,   
                        fromCity,   
                        isAvailable,
                        views      
                    )
                    VALUES
                    (
                        :name,    
                        :price,      
                        :quantity,   
                        :category,   
                        :fromCity,   
                        :isAvailable,
                        :views      
                    )""", data)
    db.commit()


def load_update_data(file_name):
    with open(file_name, "r", encoding="UTF-8") as f:
        data = json.load(f)
        items = []
        for d in data:
            d = dict(d)
            items.append(d)
    return items


def del_by_name(db, name):
    cursor = db.cursor()
    cursor.execute("DELETE FROM task4 WHERE name = ?", [name])
    db.commit()


def available_by_name(db, name, param):
    cursor = db.cursor()
    param = "True" if param == 1 else "False"
    cursor.execute("UPDATE task4 SET isAvailable = ? WHERE (name = ?)", [param, name])
    cursor.execute("UPDATE task4 SET updated = updated + 1 WHERE name = ?", [name])
    db.commit()


def price_abs_by_name(db, name, param):
    cursor = db.cursor()
    res = cursor.execute("UPDATE task4 SET price = ROUND((price + ?), 2) WHERE (name = ?) AND ((price + ?) > 0)", [param, name, param])
    if res.rowcount > 0:
        cursor.execute("UPDATE task4 SET updated = updated + 1 WHERE name = ?", [name])
        db.commit()


def quantity_update_by_name(db, name, param):
    cursor = db.cursor()
    res = cursor.execute("UPDATE task4 SET quantity = (quantity + ?) WHERE (name = ?) AND ((quantity + ?) > 0)", [param, name, param])
    if res.rowcount > 0:
        cursor.execute("UPDATE task4 SET updated = updated + 1 WHERE name = ?", [name])
        db.commit()


def price_percent_by_name(db, name, param):
    cursor = db.cursor()    
    cursor.execute("UPDATE task4 SET price = ROUND(price * (1+?), 2) WHERE name = ?", [param, name])
    cursor.execute("UPDATE task4 SET updated = updated + 1 WHERE name = ?", [name])
    db.commit()


def handle_update(db, update_items):    
    for item in update_items:
        match item["method"]:
            case "remove": 
                del_by_name(db, item["name"])
            case "available": 
                available_by_name(db, item["name"], item["param"])
            case "price_abs": 
                price_abs_by_name(db, item["name"], item["param"])
            case "quantity_add":
                quantity_update_by_name(db, item["name"], item["param"])
            case "quantity_sub":
                quantity_update_by_name(db, item["name"], item["param"])
            case "price_percent": 
                price_percent_by_name(db, item["name"], item["param"])


def first_request(db):
    """
    Вывод первых 10 строк по самым изменяемым товарам
    """
    cursor = db.cursor()
    data = cursor.execute("SELECT * FROM task4 ORDER BY updated LIMIT 10")
    for row in data.fetchall():
        row = dict(row)
        print(row)

        
def second_request(db):
    """
    Вывод суммы, максильмальной, минимальной и средней стоимости товаров в группе
    """
    cursor = db.cursor()
    data = cursor.execute("""
                          SELECT
                            category,
                            SUM(price) as sum,
                            MAX(price) as max,
                            MIN(price) as mix,
                            AVG(price) as avg                            
                          FROM task4
                          GROUP BY category
                          """)
    
    for row in data.fetchall():
        row = dict(row)
        print(row)


def third_request(db):
    """
    Вывод самых просматриваемых товаров по группам
    """
    cursor = db.cursor()
    data = cursor.execute("""
                            SELECT * 
                            FROM task4                        
                            WHERE (SELECT MAX(views) FROM task4)
                            GROUP BY category
""")
    for row in data.fetchall():
        row = dict(row)
        print(row)


def main():
    # парсинг данных из файла
    #data = parse_data("task_4_var_10_product_data.csv")
    
    #Подключение к базе данных
    conn = connect_db("task4.db")

    # Создание таблицы
    #create_table(conn)

    #Внесение данных в таблицу
    #insert_data_to_table(conn, data)

    # парсинг данных обновления
    #update_data = load_update_data("task_4_var_10_update_data.json")
    
    # Обновление данных в таблице
    #handle_update(conn, update_data)

    # Запросы
    first_request(conn)
    print("##############################################################")
    second_request(conn)
    print("##############################################################")
    third_request(conn)


if __name__ == "__main__":
    main()