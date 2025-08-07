import subprocess, json, os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["octopuser"]
collection = db["hosts"]

def run(cmd):
    print(f"$ {' '.join(cmd)}")
    return subprocess.check_output(cmd).decode()

def scan(ip_range):
    # 1. masscan
    output = run(["masscan", "-p80,443", ip_range, "--rate", "1000"])
    open_ips = set()
    for line in output.splitlines():
        if line.startswith("Discovered"):
            ip = line.split()[-1]
            open_ips.add(ip)

    for ip in open_ips:
        # 2. naabu check
        try:
            result = run(["naabu", "-host", ip])
            ports = [int(line.split(":")[-1]) for line in result.splitlines() if line.startswith("[")]
            services = []
            for port in ports:
                url = f"http{'s' if port == 443 else ''}://{ip}:{port}"
                try:
                    httpx_out = run(["httpx", "-u", url, "-json"])
                    httpx_data = json.loads(httpx_out)
                    services.append({
                        "port": port,
                        "protocol": "https" if port == 443 else "http",
                        "service": {
                            "title": httpx_data.get("title"),
                            "status_code": httpx_data.get("status_code"),
                            "tls": httpx_data.get("tls_dns_names"),
                        },
                        "source": ["httpx"]
                    })
                except:
                    continue
            collection.update_one({"ip": ip}, {"$set": {"ip": ip, "ports": services}}, upsert=True)
        except:
            continue

if __name__ == "__main__":
    scan("192.168.0.0/24")
