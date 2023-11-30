from db_connection import connect_db
import json


def parse_data(file_name):
    """
    Функция считывает и возвращает данные из json файла (без id)
    """
    with open(f"{file_name}", "r", encoding="UTF-8") as f:
        lines = json.load(f)
        for line in lines:
            del line["id"]
        return lines


def insert_data(db, data):
    """
    Функция создает таблицу в базе данных (если она не существует)
    и заполняет ее данными
    """
    cursor = db.cursor()
    # Поле id индексируется от 1
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS task1
                (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                city TEXT,
                begin FLOAT,
                system TEXT,
                tours_count INTEGER,
                min_rating INTEGER,
                time_on_game INTEGER
                )
                """)    
    cursor.executemany("""
        INSERT INTO task1
        (
            name,
            city,
            begin,
            system,
            tours_count,
            min_rating,
            time_on_game       
        )
        VALUES
        (
            :name,
            :city,
            :begin,
            :system,
            :tours_count,
            :min_rating,
            :time_on_game
        );
        """, data)
    db.commit()


def get_top_min_rating(db, limit):
    """
    Вывод первых limit (вариант № 10 = 20) строк
    отсортированных по min_rating
    """
    cursor = db.cursor()
    data = cursor.execute("SELECT * FROM task1 ORDER BY min_rating DESC LIMIT ?", [limit])
    items = []
    for row in data.fetchall():
        item = dict(row)
        items.append(item)

    cursor.close()
    return items
    

def get_stat_by_tours_count(db):
    """
    Вывод на экран суммы, среднего, минимального 
    и максимального значений поля tours_count
    """
    cursor = db.cursor()
    data = cursor.execute("""
                        SELECT
                            SUM(tours_count) as sum,
                            AVG(tours_count) as avg,
                            MIN(tours_count) as min,
                            MAX(tours_count) as max
                          from task1
                          """)
    print(dict(data.fetchone()))


def get_freq_by_city(db):
    """
    Вывод на экран частоты встречаемости городов
    """
    cursor = db.cursor()
    data = cursor.execute("""
                            SELECT city, COUNT(*) as count
                            FROM task1
                            GROUP BY city
                          """)
    city_freq = {}
    for row in data.fetchall():
        print(dict(row))
    cursor.close()


def filter_by_time_on_game(db, min_time_on_game, limit=10):
    """
    Функция возвращает отфильтрованные строки по time_on_game,
    отсортированные по min_rating
    """
    cursor = db.cursor()
    data = cursor.execute("""
                        SELECT *
                        FROM task1
                        WHERE time_on_game > ?
                        ORDER BY min_rating
                        LIMIT ?
                          """, [min_time_on_game, limit])
    items = []
    for row in data.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items

def main():
    VAR = 10
    #data = parse_data("task_1_var_10_item.json")
    conn = connect_db("task1.db")
    #insert_data(conn, data)
    top_min_rate = get_top_min_rating(conn, VAR + 10) # Вариант 10

    with open("out_task1_1.json", "w", encoding="UTF-8") as f:
        f.write(json.dumps(top_min_rate, ensure_ascii=False))

    get_stat_by_tours_count(conn)
    get_freq_by_city(conn)

    filtered_time_on_game = filter_by_time_on_game(conn, 100, VAR + 10) # Вариант 10

    with open("out_task1_2.json", "w", encoding="UTF-8") as f:
        f.write(json.dumps(filtered_time_on_game, ensure_ascii=False))

if __name__ == "__main__":
    main()