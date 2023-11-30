from db_connection import connect_db
import json
import csv


"""
Предметная область: автоаварии
Создание бд в файле db_connection.py
Исходные файлы: crash_incidents.json / crash_reporting.csv
Функция инициализации таблиц: create_tables
Функции для загрузки данных из файлов: parse_data_csv, parse_data_json
Файлы баз данных в папке db_collection
Запросы в функциях с имени get
"""


def parse_data_csv(file_name : str) -> list:
    """
    Считывание полей item1:
        Crash Date/Time,
        Hit/Run,
        Route Type,
        Lane Type,
        Weather,
        At Fault,
        Latitude,
        Longitude
    item2:
        Agency Name,
        ACRS Report Type,
        Number of Lanes,
        Mile Point,
        Light,
        Traffic Control,
        Cross-Street Type
    """
    with open(file_name, "r") as f:
        items1 = [] 
        items2 = []      
        reader = csv.DictReader(f, delimiter=",")        
        for row in reader:
            item1, item2 = {}, {}              
            item1["Crash_Date_Time"] = row["Crash Date/Time"]
            item1["Hit_Run"] = row["Hit/Run"]
            item1["Route_Type"] = row["Route Type"]
            item1["Lane_Type"] = row["Lane Type"]
            item1["Weather"] = row["Weather"]
            item1["At_Fault"] = row["At Fault"]
            item1["Latitude"] = float(row["Latitude"])
            item1["Longitude"] = float(row["Longitude"])

            # Обработка пустых результатов            
            if '' in item1.values():
                for key, value in item1.items():
                    if value == "":
                        item1[key] = "-"

            items1.append(item1)

            item2["Agency_Name"] = row["Agency Name"]
            item2["ACRS_Report_Type"] = row["ACRS Report Type"]
            item2["Number_of_Lanes"] = int(row["Number of Lanes"])
            item2["Mile_Point"] = float(row["Mile Point"]) if row["Mile Point"] != '' else 0.
            item2["Light"] = row["Light"]
            item2["Traffic_Control"] = row["Traffic Control"]
            item2["Cross_Street_Type"] = row["Cross-Street Type"]

            # Обработка пустых результатов            
            if '' in item2.values():
                for key, value in item2.items():
                    if value == "":
                         item2[key] = "-"
            items2.append(item2)

    return items1, items2


def parse_data_json(file_name : str) -> list:
    """
    Считывание полей:
        "location_description",
        "lat",
        "lon",
        "lat2",
        "lon2",
        "vehicle1",
        "vehicle2",
        "crash_date",
        "records"
    """
    with open(file_name, "r") as f:
        items = []
        data = json.load(f)
        for row in data:
            item = {}
            item["location_description"] = row["location_description"]
            item["lat"] = float(row["lat"]) if row["lat"] != None else 0.
            item["lon"] = float(row["lon"]) if row["lon"] != None else 0.
            item["lat2"] = float(row["lat2"]) if row["lat2"] != None else 0.
            item["lon2"] = float(row["lon2"]) if row["lon2"] != None else 0.
            item["vehicle1"] = row["vehicle1"]
            item["vehicle2"] = row["vehicle2"]
            item["crash_date"] = row["crash_date"]
            item["records"] = int(row["records"])
            # Обработка пустых результатов            
            if '' in item.values():
                for key, value in item.items():
                    if value == "":
                         item[key] = "-"
            items.append(item)
    return items


def create_tables(db):
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS csv_table1
                   (
                        id              INTEGER PRIMARY KEY AUTOINCREMENT,
                        Crash_Date_Time TEXT,
                        Hit_Run         TEXT,
                        Route_Type      TEXT,
                        Lane_Type       TEXT,
                        Weather         TEXT,
                        At_Fault        TEXT,
                        Latitude        FLOAT,
                        Longitude       FLOAT
                    )  """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS csv_table2
                   (
                        id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                        Agency_Name         TEXT,
                        ACRS_Report_Type    TEXT,
                        Number_of_Lanes     TEXT,
                        Mile_Point          FLOAT,
                        Light               TEXT,
                        Traffic_Control     TEXT,
                        Cross_Street_Type   TEXT
                    )  """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS json_table
                   (
                        id                      INTEGER PRIMARY KEY AUTOINCREMENT,
                        location_description    TEXT,
                        lat                     FLOAT,
                        lon                     FLOAT,
                        lat2                    FLOAT,
                        lon2                    FLOAT,
                        vehicle1                TEXT,
                        vehicle2                TEXT,
                        crash_date              TEXT,
                        records                 INTEGER
                    )  """)
    db.commit


def insert_data_to_tables(db, csv_1, csv_2, json_):
    cursor = db.cursor()
    cursor.executemany("""
                    INSERT INTO csv_table1 
                    (         
                        Crash_Date_Time,
                        Hit_Run,        
                        Route_Type,     
                        Lane_Type,      
                        Weather,        
                        At_Fault,       
                        Latitude,       
                        Longitude         
                    )
                    VALUES
                    (            
                        :Crash_Date_Time,
                        :Hit_Run,        
                        :Route_Type,     
                        :Lane_Type,      
                        :Weather,        
                        :At_Fault,       
                        :Latitude,       
                        :Longitude   
                    )""", csv_1)
    db.commit()
    cursor.executemany("""
                    INSERT INTO csv_table2 
                    (              
                        Agency_Name,     
                        ACRS_Report_Type,
                        Number_of_Lanes,
                        Mile_Point,       
                        Light,            
                        Traffic_Control,
                        Cross_Street_Type          
                    )
                    VALUES
                    (            
                        :Agency_Name,
                        :ACRS_Report_Type,
                        :Number_of_Lanes,
                        :Mile_Point,
                        :Light,
                        :Traffic_Control,
                        :Cross_Street_Type  
                    )""", csv_2)
    db.commit()
    cursor.executemany("""
                    INSERT INTO json_table 
                    (              
                        location_description,
                        lat,          
                        lon,           
                        lat2,           
                        lon2,          
                        vehicle1,       
                        vehicle2,       
                        crash_date,      
                        records                     
                    )
                    VALUES
                    (            
                        :location_description,
                        :lat,             
                        :lon,               
                        :lat2,           
                        :lon2,          
                        :vehicle1,       
                        :vehicle2,      
                        :crash_date,     
                        :records             
                    )""", json_)
    db.commit()


def write_json(file_name, data): 
    # Запись в json файл
    with open(file_name, "w") as f:
        f.write(json.dumps(data))


def get_stats(db) -> list:
    """
    Запрос на получение статистических данных по количеству полос с таблицы csv_table2
    """
    items = []
    cursor = db.cursor()
    data = cursor.execute("""
                            SELECT 
                                SUM(Number_of_Lanes) as sum,
                                MAX(Number_of_Lanes) as max,
                                MIN(Number_of_Lanes) as min,
                                AVG(Number_of_Lanes) as avg
                            FROM csv_table2
""")
    for row in data.fetchall():
        row = dict(row)
        items.append(row)
    return items


def get_count_weather(db, limit=10):
    """
    Запрос на получение количества встречаемости разных погодных условий из таблицы csv_table1
    """
    cursor = db.cursor()
    data = cursor.execute("""
                            SELECT weather, COUNT(weather) as count
                            FROM csv_table1
                            GROUP BY weather
                            LIMIT ?
                          """, [limit])
    items = []
    for row in data.fetchall():
        row = dict(row)
        items.append(row)
    return items 


def get_same_vehicle(db, limit=50):
    """
    Запрос на получение строчек с одинаковым видом транспортного средства
    """
    cursor = db.cursor()
    data = cursor.execute("SELECT * FROM json_table WHERE vehicle1 = vehicle2 LIMIT ?", [limit])
    items = []
    for row in data.fetchall():
        row = dict(row)
        items.append(row)
    return items


def get_order_by_mile_point(db, limit=50) -> list:  
    """
    Запрос на получение строк в порядке убывания по полю Mile_point
    """
    items = []
    cursor = db.cursor()
    data = cursor.execute("""
                            SELECT 
                                *
                            FROM csv_table2
                            ORDER BY Mile_Point DESC
                            LIMIT ?
""", [limit])
    for row in data.fetchall():
        row = dict(row)
        items.append(row)
    return items


def get_stats_by_mile_point_gr(db) -> list:
    """
    Запрос на получение статистических данных группированных по источнику света
    """
    items = []
    cursor = db.cursor()
    data = cursor.execute("""
                            SELECT 
                                light,
                                SUM(mile_point) as sum,
                                MAX(mile_point) as max,
                                MIN(mile_point) as mix,
                                AVG(mile_point) as avg  
                            FROM csv_table2
                            GROUP BY light
""")
    for row in data.fetchall():
        row = dict(row)
        items.append(row)
    return items


def get_route_and_hnr(db, limit=50) -> list:
    """
    Запрос на получение статистических данных группированных по источнику света
    """
    items = []
    cursor = db.cursor()
    data = cursor.execute("""
                            SELECT 
                                * 
                            FROM csv_table1
                            WHERE (Route_Type = "County") AND (Hit_Run = "Yes")
                            LIMIT ?
""", [limit])
    for row in data.fetchall():
        row = dict(row)
        items.append(row)
    return items


def main():
    #data_csv1, data_csv2 = parse_data_csv("crash_reporting.csv")
    #data_json = parse_data_json("crash_incidents.json")
    conn = connect_db("car_crash.db")
    #create_tables(conn)
    #insert_data_to_tables(conn, data_csv1, data_csv2, data_json)

    # Запросы к БД
    data = get_stats(conn)
    write_json(".\\out_task5\\out_stats_csv_table2.json", data)

    data = get_count_weather(conn, 5)
    write_json(".\\out_task5\\out_weather_csv_table1.json", data)

    data = get_same_vehicle(conn)
    write_json(".\\out_task5\\out_same_vehicles_json_table.json", data)

    data = get_order_by_mile_point(conn)  
    write_json(".\\out_task5\\out_order_by_mile_point_csv_table2.json", data)

    data = get_stats_by_mile_point_gr(conn)
    write_json(".\\out_task5\\out_stats_by_mile_point_gr_csv_table2.json", data)

    data = get_route_and_hnr(conn)
    write_json(".\\out_task5\\out_stats_by_route_and_hnr_csv_table1.json", data)


if __name__ == "__main__":
    main()