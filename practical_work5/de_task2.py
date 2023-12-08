import csv
from pymongo import MongoClient
from common_func import write_json, insert_data


def connect():
    client = MongoClient()
    db = client["test-database"]
    return db.person


def parse_data(file_name):
    items = []
    with open(file_name, "r", encoding="UTF-8")as f:
        reader = csv.DictReader(f, delimiter=";")
        for item in reader:
            for key in item.keys():
                if item[key].isdigit():
                    item[key] = int(item[key])
            items.append(item)
    return items


def get_stat_res(coll):
    items = []
    req = [
        {
            "$group":{
                "_id": "result",
                "max":{"$max":"$salary"},
                "min":{"$min":"$salary"},
                "avg":{"$avg":"$salary"}
            }
        }
    ]
    for c in coll.aggregate(req):
        items.append(c)
    write_json("stat_res", items, 2)
    

def get_freq_by_job(coll):
    items = []
    req = [
        {
            "$group": {
                "_id": "$job",
                "count": {"$sum":1}
            }
        },
        {
            "$sort":{
                "count":-1
            }
        }
    ]
    for c in coll.aggregate(req):
        items.append(c)
    write_json("freq_by_job", items, 2)


def get_stat_salary_by_city(coll):
    items = []
    req = [
        {
            "$group" : {
                "_id": "$city",
                "max": {"$max": "$salary"},
                "min": {"$min": "$salary"},
                "avg": {"$avg": "$salary"}
            }
        }
    ]
    for c in coll.aggregate(req):
        items.append(c)
    write_json("stat_salary_by_city", items, 2)


def get_stat_salary_by_job(coll):
    items = []
    req = [
        {
            "$group" : {
                "_id": "$job",
                "max": {"$max": "$salary"},
                "min": {"$min": "$salary"},
                "avg": {"$avg": "$salary"}
            }
        }
    ]
    for c in coll.aggregate(req):
        items.append(c)
    write_json("stat_salary_by_job", items, 2)


def get_stat_age_by_city(coll):
    items = []
    req = [
        {
            "$group" : {
                "_id": "$city",
                "max": {"$max": "$age"},
                "min": {"$min": "$age"},
                "avg": {"$avg": "$age"}
            }
        }
    ]
    for c in coll.aggregate(req):
        items.append(c)
    write_json("stat_age_by_city", items, 2)


def get_stat_age_by_job(coll):
    items = []
    req = [
        {
            "$group" : {
                "_id": "$job",
                "max": {"$max": "$age"},
                "min": {"$min": "$age"},
                "avg": {"$avg": "$age"}
            }
        }
    ]
    for c in coll.aggregate(req):
        items.append(c)
    write_json("stat_age_by_job", items, 2)


def get_max_salary_with_min_age(coll):
    items = []
    req = [
        {
            "$group":{
                "_id": "$salary",
                "min_age" : {"$min": "$age"}

            }
        },
        {
            "$group" : { 
                "_id": "result",
                "max_salary": {"$max": "$_id"},
                "min_age": {"$min": "$min_age"},
            }
        }
    ]
    for c in coll.aggregate(req):
        items.append(c)
    write_json("get_max_salary_with_min_age", items, 2)


def get_max_age_with_min_salary(coll):
    items = []
    req = [
        {
            "$group":{
                "_id": "$age",
                "min_salary" : {"$min": "$salary"}

            }
        },
        {
            "$group" : { 
                "_id": "result",
                "max_age": {"$max": "$_id"},
                "min_salary": {"$min": "$min_salary"},
            }
        }
    ]
    for c in coll.aggregate(req):
        items.append(c)
    write_json("max_age_with_min_salary", items, 2)


def get_stat_age_by_salary_ge_50k(coll):
    req = [
        {
            "$match": {
                "salary" : {"$gt": 50000}
            }
        },
        {
            "$group": {
                "_id"     : "$city",
                "max_age" : {"$max":"$age"},
                "min_age" : {"$min":"$age"},
                "avg_age" : {"$avg":"$age"}
            }
        },
        {
            "$sort":
            {
                "avg_age": -1
            }
        }
    ]
    items = []
    for c in coll.aggregate(req):
        items.append(c)
    write_json("stat_age_by_salary_ge_50k", items, 2)


def big_req(coll):
    items = []
    req = [
        {
            "$match":{
                "city" : {"$in": ["Ташкент", "Москва", "Прага"]},
                "job"  : {"$in": ["Программист", "Повар", "Врач", "Продавец", "Инженер"]},
                "$or" : [
                    {"age": {"$gt": 18, "$lt": 25}},
                    {"age": {"$gt": 50, "$lt": 65}}
                ]
            }
        },
        {
            "$group": {
                "_id" : "result",
                "max": {"$max": "$salary"},
                "min": {"$min": "$salary"},
                "avg": {"$avg": "$salary"}
            }
        }
    ]
    for c in coll.aggregate(req):
        items.append(c)
    write_json("big_req", items, 2)


def my_req(coll):
    items = []
    req = [
        {
            "$match":{
                "city" : {"$in" : ["Москва", "Ташкент"]},
                "age"  : {"$gt" : 30, "$lt": 50}
            }
        },
        {
            "$group":{
                "_id"     : "result",
                "max_sal" : {"$max":"$salary"},
                "min_sal" : {"$min":"$salary"},
                "avg_sal" : {"$avg":"$salary"}
            }
        },
        {
            "$sort":{
                "age": -1
            }
        }
    ]
    for c in coll.aggregate(req):
        items.append(c)
    write_json("my_req", items, 2)


def main():
    coll = connect()
    #data = parse_data("task_2_item.csv")    
    #insert_data(coll, data)

    # вывод минимальной, средней, максимальной salary
    get_stat_res(coll)

    # вывод количества данных по представленным профессиям
    get_freq_by_job(coll)
    
    # вывод минимальной, средней, максимальной salary по городу
    get_stat_salary_by_city(coll)
    
    # вывод минимальной, средней, максимальной salary по профессии
    get_stat_salary_by_job(coll)
    
    # вывод минимального, среднего, максимального возраста по городу
    get_stat_age_by_city(coll)
    
    # вывод минимального, среднего, максимального возраста по профессии
    get_stat_age_by_job(coll)
    
    # вывод максимальной заработной платы при минимальном возрасте
    get_max_salary_with_min_age(coll)
    
    # вывод минимальной заработной платы при максимальной возрасте
    get_max_age_with_min_salary(coll)

    # вывод минимального, среднего, максимального возраста по городу, при условии, что заработная плата больше 50 000
    get_stat_age_by_salary_ge_50k(coll)

    # вывод минимальной, средней, максимальной salary в произвольно заданных диапазонах по городу, профессии, и возрасту
    big_req(coll)

    # Произвольный запрос
    my_req(coll)


if __name__ == "__main__":
    main()