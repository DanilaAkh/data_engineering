from db_connection import connect_db
import json
import msgpack


def parse_data(json_fn, msgpack_fn):
    items = []
    with open(msgpack_fn, "rb") as f:
        data = msgpack.load(f, raw=False)
        for d in data:
            d["duration_ms"] = int(d["duration_ms"])
            d["year"] = int(d["year"])
            d["tempo"] = float(d["tempo"])
            del d["speechiness"]
            del d["acousticness"]
            del d["instrumentalness"]
            items.append(d)
    with open(json_fn, "r", encoding="UTF-8") as f:
        data = json.load(f)
        for d in data:
            d = dict(d)
            d["duration_ms"] = int(d["duration_ms"])
            d["year"] = int(d["year"])
            d["tempo"] = float(d["tempo"])
            del d["explicit"]
            del d["popularity"]
            del d["danceability"]
            items.append(d)
    return items


def create_table(db):
    cursor = db.cursor()
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS task3
                    (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        artist TEXT,
                        song TEXT,
                        duration_ms INTEGER,
                        year INTEGER,
                        tempo FLOAT,
                        genre TEXT
                    )
    """)
    cursor.close()


def insert_data_to_table(db, data):
    cursor = db.cursor()
    cursor.executemany("""
                    INSERT INTO task3 
                    (
                        artist,
                        song,
                        duration_ms,
                        year,
                        tempo,
                        genre
                    )
                    VALUES
                    (:artist, :song, :duration_ms, :year, :tempo, :genre)
    """, data)
    db.commit()


def get_top_by_year(db, limit=10):
    cursor = db.cursor()
    data = cursor.execute("""
                    SELECT * FROM task3 ORDER BY year DESC LIMIT ?
    """, [limit])
    items = []
    for row in data.fetchall():
        items.append(dict(row))
    cursor.close()
    return items


def get_stat_by_tempo(db):
    cursor = db.cursor()
    data = cursor.execute("""
                        SELECT
                            SUM(tempo) as sum,
                            AVG(tempo) as avg,
                            MIN(tempo) as min,
                            MAX(tempo) as max
                          from task3
                          """)
    items = []
    for row in data.fetchall():
        items.append(dict(row))
    return items


def get_freq_by_year(db):
    cursor = db.cursor()
    data = cursor.execute("""
                            SELECT year, COUNT(*) as count
                            FROM task3
                            GROUP BY year
                          """)
    items = []
    for row in data.fetchall():
        items.append(dict(row))
    return items 
    

def filter_by_duration_ms(db, duration_ms, limit=10):
    cursor = db.cursor()
    data = cursor.execute("""
                        SELECT *
                        FROM task3
                        WHERE duration_ms > ?
                        ORDER BY year
                        LIMIT ?
                          """, [duration_ms, limit])
    items = []
    for row in data.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    return items


def main():
    VAR = 10
    #data = parse_data("task_3_var_10_part_2.json", "task_3_var_10_part_1.msgpack") # Получение данных из файлов
    conn = connect_db("task3.db") # Соединение с базой данных
    #create_table(conn) # Создание таблицы
    #insert_data_to_table(conn, data) # Занесение данных в таблицу из файлов


    # Получение первых 20 строк строк по годам и запись их в json
    top_by_year = get_top_by_year(conn, VAR + 10) # 10 вариант
    with open(f"task3_top20_by_year.json", "w") as f:
        f.write(json.dumps(top_by_year))

    stat_tempo = get_stat_by_tempo(conn)
    print(stat_tempo)

    freq_by_year = get_freq_by_year(conn)
    print(freq_by_year)

    filtered_data = filter_by_duration_ms(conn, 170000, VAR + 15) # 10 вариант
    with open(f"task3_filtered_data.json", "w") as f:
        f.write(json.dumps(filtered_data))

if __name__ == "__main__":
    main()