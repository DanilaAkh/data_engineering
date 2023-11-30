import sqlite3


def connect_db(file_name : str):
    connection = sqlite3.connect(f".\\db_collection\\{file_name}")
    connection.row_factory = sqlite3.Row
    return connection