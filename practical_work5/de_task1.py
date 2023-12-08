import msgpack
from pymongo import MongoClient
from common_func import write_json, insert_data


def connect():
    client = MongoClient()
    db = client["test-database"]
    return db.person


def get_from_msgpack(file_name):
    items = []
    with open(file_name, "rb") as f:
        items = msgpack.load(f, raw=False)
    return items


def sort_by_salary(coll):
    items = []
    for c in coll.find(limit=10).sort({"salary":-1}):
        del c["_id"]
        items.append(c)
    write_json("sort_by_salary", items, 1)


def filter_by_age(coll):
    items = []
    for c in coll.find({"age":{"$lt":30}}, limit=10).sort({"salary" : -1}):
        del c["_id"]
        items.append(c)
    write_json("filter_by_age", items, 1)


def filter_predicate(coll):
    items = []
    for c in coll.find({"city":"Ташкент", "job": {"$in" : ["Программист", "Повар", "Врач", "Продавец", "Инженер"]}}, limit=10).sort({"age":1}):
        del c["_id"]
        items.append(c)
    write_json("filter_predicate", items, 1)


def count_notes(coll):    
    res = coll.count_documents({
        "age":{"$gt":25, "$lt":35},
        "year": {"$gte": 2019, "$lte": 2022},
        "$or": [
            {"salary": {"$gt": 50000, "$lte": 75000}},
            {"salary": {"$gt": 125000, "$lt": 150000}}
        ]
    })
    write_json("count_notes", {"count":res}, 1)


def main():
    coll = connect()
    #data = get_from_msgpack("task_1_item.msgpack")
    #insert_data(coll, data)

    sort_by_salary(coll)
    filter_by_age(coll)
    filter_predicate(coll)
    count_notes(coll)


if __name__ == "__main__":
    main()