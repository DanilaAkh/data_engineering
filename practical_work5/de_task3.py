import pickle
from common_func import write_json, insert_data
from pymongo import MongoClient


def connect():
    client = MongoClient()
    db = client["test-database"]
    return db.person

def parse_data(file_name):
    items = []
    with open(file_name, "rb") as f:
        data = pickle.load(f)
        for d in data:
            items.append(d)
    return items


def delete_by_salary(coll):
    res = coll.delete_many({
        "$or" : [
            {"salary" : {"$lt" : 25000}},
            {"salary" : {"$gt" : 175000}}
        ]
    })
    print(res)


def incr_age(coll):
    coll.update_many({}, {
        "$inc" : {
            "age" : 1
        } 
    })


def incr_salary(coll):
    filter = {
        "job": {"$in": ["Программист", "Повар", "Врач", "Продавец", "Инженер"]}
    }
    update = {
        "$mul" : {"salary" : 1.05}
    }
    coll.update_many(filter, update)


def incr_salary_by_city(coll):
    filter = {
        "city": {"$in": ["Ташкент", "Москва", "Прага"]}
    }
    update = {
        "$mul" : {"salary" : 1.07}
    }
    coll.update_many(filter, update)


def incr_salary_by_everything(coll):
    filter = {
        "city": {"$in": ["Ташкент", "Москва", "Прага"]},
        "job": {"$in": ["Программист", "Повар", "Врач", "Продавец", "Инженер"]},
        "age": {"$gt": 55, "$lte" : 20}
    }
    update = {
        "$mul" : {"salary" : 1.1}
    }
    coll.update_many(filter, update)


def delete_by_predicate(coll):
    filter = {
        "$or" : [
            {"age" : {"$lt" : 20}},
            {"salary" : {"$gt" : 165000}},
            {"job": {"$in" : ["Оператор call-центра"]}}
        ]
    }
    res = coll.delete_many(filter)
    print(res)


def main():
    #data = parse_data("task_3_item.pkl")
    coll = connect()
    #insert_data(coll, data)
    
    # Удаление из коллекции документы по предикату
    #delete_by_salary(coll)

    # увеличение возраст (age) всех документов на 1
    #incr_age(coll)

    # поднять заработную плату на 5% для произвольно выбранных профессий
    #incr_salary(coll)

    # поднять заработную плату на 7% для произвольно выбранных городов
    #incr_salary_by_city(coll)

    # поднять заработную плату на 10% для выборки по сложному предикату 
    #incr_salary_by_everything(coll)

    # Удалить по произвольному признаку
    delete_by_predicate(coll)


if __name__ == "__main__":
    main()