import csv
import json
from pymongo import MongoClient
from common_func import write_json, insert_data


def connect():
    client = MongoClient()
    db = client["test-database"]
    return db.reporting, db.incidents


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
    """
    with open(file_name, "r") as f:
        items1 = [] 
        items2 = []      
        reader = csv.DictReader(f, delimiter=",")        
        for row in reader:
            item1 = {}              
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
    return items1


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


def get_records_incidents(coll):
    items = []
    for c in coll.find(limit=10).sort({"records":-1}):
        del c["_id"]
        items.append(c)
    write_json("records_incidents", items, 4)


def get_route_type(coll):
    items = []
    for c in coll.find({"Route_Type": {"$in" : ["County"]}}, limit=15).sort({"Crash_Date_Time": 1}):
        del c["_id"]
        items.append(c)
    write_json("route_type", items, 4)


def filter_weather(coll, weather : list):
    items = []
    for c in coll.find({"Weather": {"$in" : weather}}, limit=15):
        del c["_id"]
        items.append(c)
    write_json("filter_weather", items, 4)


def counter(coll):
    res = coll.count_documents({
            "Hit_Run" : {"$eq" : "Yes"}, 
            "At_Fault": {"$eq": "DRIVER"}}
        )
    write_json("counter", {"count" : res}, 4)


def count_same_veh(coll):
    res = coll.count_documents({
        "vehicle1" : "SPORT UTILITY",
        "vehicle2" : "SPORT UTILITY"
        })
    write_json("count_same_veh", {"count" : res}, 4)


def get_stat_records(coll):
    items = []
    req = [
        {
            "$group":{
                "_id": "result",
                "max":{"$max":"$records"},
                "min":{"$min":"$records"},
                "avg":{"$avg":"$records"}
            }
        }
    ]
    for c in coll.aggregate(req):
        items.append(c)
    write_json("stat_records", items, 4)


def get_freq_by_weather(coll):
    items = []
    req = [
        {
            "$group": {
                "_id": "$Weather",
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
    write_json("freq_by_weather", items, 4)


def get_stat_latitude_by_weather(coll):
    items = []
    req = [
        {
            "$group" : {
                "_id": "$Weather",
                "max": {"$max": "$Latitude"},
                "min": {"$min": "$Latitude"},
                "avg": {"$avg": "$Latitude"}
            }
        }
    ]
    for c in coll.aggregate(req):
        items.append(c)
    write_json("stat_stat_latitude_by_weather", items, 4)


def get_max_lon2_with_min_lat2(coll):
    items = []
    req = [
        {
            "$group":{
                "_id": "$lat2",
                "min_lat2" : {"$min": "$lat2"}

            }
        },
        {
            "$group" : { 
                "_id": "result",
                "max_lon2": {"$max": "$_id"},
                "min_lat2": {"$min": "$min_lat2"},
            }
        }
    ]
    for c in coll.aggregate(req):
        items.append(c)
    write_json("max_lon2_with_min_lat2", items, 4)


def big_req(coll):
    items = []
    req = [
        {
            "$match":{
                "Weather" : "CLEAR",
                "Hit_Run"  : "No",
                "$or" : [
                    {"Latitude": {"$gt": 39.15, "$lt": 39.45}},
                    {"Longitude": {"$gt": -77.40, "$lt": -77.10}}
                ]
            }
        },
        {
            "$group": {
                "_id" : "result",
                "max": {"$max": "$Latitude"},
                "min": {"$min": "$Latitude"},
                "avg": {"$avg": "$Latitude"}
            }
        }
    ]
    for c in coll.aggregate(req):
        items.append(c)
    write_json("big_req", items, 4)


def delete_by_records(coll):
    res = coll.delete_many({
        "$or" : [
            {"records" : {"$lt" : 1000}},
            {"records" : {"$gt" : 20000}}
        ]
    })
    print(res)


def incr_records(coll):
    coll.update_many({}, {
        "$inc" : {
            "records" : 1
        } 
    })


def incr_salary_by_weather(coll):
    filter = {
        "Weather": {"$in": ["CLOUDY", "RAINING"]}
    }
    update = {
        "$mul" : {"Latitude" : 1.05},
        "$mul" : {"Longitude" : 1.1}
    }
    coll.update_many(filter, update)


def main():
    coll_reporting, coll_incidents = connect()
    #data_csv = parse_data_csv("crash_reporting.csv")
    #data_json = parse_data_json("crash_incidents.json")

    #insert_data(coll_reporting, data_csv)
    #insert_data(coll_incidents, data_json)

    # Задание 1
    get_records_incidents(coll_incidents)
    get_route_type(coll_reporting)
    filter_weather(coll_reporting, ["CLOUDY", "CLEAR"])
    count_same_veh(coll_incidents)
    counter(coll_reporting)

    # Задание 2
    get_stat_records(coll_incidents)
    get_freq_by_weather(coll_reporting)
    get_stat_latitude_by_weather(coll_reporting)
    get_max_lon2_with_min_lat2(coll_incidents)
    big_req(coll_reporting)
    
    # Задание 3
    delete_by_records(coll_incidents)
    incr_records(coll_incidents)
    incr_salary_by_weather(coll_reporting)
    

if __name__ == "__main__":
    main()