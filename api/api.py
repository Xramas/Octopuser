from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from bson import ObjectId
import os

app = FastAPI()

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
db = client["octopuser"]
collection = db["hosts"]

@app.get("/ip/{ip}")
def get_ip(ip: str):
    result = collection.find_one({"ip": ip})
    if not result:
        raise HTTPException(status_code=404, detail="IP not found")
    result["_id"] = str(result["_id"])
    return result

@app.get("/port/{port}")
def get_by_port(port: int):
    results = collection.find({"ports.port": port})
    return [{"ip": r["ip"], "ports": r["ports"]} for r in results]

@app.get("/ip")
def list_ips():
    return [r["ip"] for r in collection.find({}, {"ip": 1})]
