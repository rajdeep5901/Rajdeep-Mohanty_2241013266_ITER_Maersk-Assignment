import requests, datetime
from .config import C
def iso(dt):
    return dt.replace(microsecond=0).isoformat()
def fetch(since):
    if C.NDAC_MOCK:
        return [
            {"id":"A1","sev":"CRITICAL","typ":"LinkDown","elem":"gNodeB-12","msg":"Backhaul down","ts":iso(datetime.datetime.utcnow())},
            {"id":"A2","sev":"MAJOR","typ":"HighLatency","elem":"CU-UP-3","msg":"Latency > 200ms","ts":iso(datetime.datetime.utcnow())},
            {"id":"A3","sev":"MINOR","typ":"TempHigh","elem":"RU-7","msg":"Temp 65C","ts":iso(datetime.datetime.utcnow())}
        ]
    h={"Authorization":"Bearer "+C.NDAC_TOKEN}
    u=f"{C.NDAC_BASE_URL}/alarms"
    p={"since":iso(since)}
    r=requests.get(u,headers=h,params=p,timeout=30)
    r.raise_for_status()
    x=r.json()
    return x if isinstance(x,list) else []