from flask import Flask, request, jsonify
import datetime, random
a=Flask(__name__)
@a.get("/alarms")
def alarms():
    since=request.args.get("since")
    now=datetime.datetime.utcnow().replace(microsecond=0).isoformat()
    s=[
        {"id":"A"+str(random.randint(1000,9999)),"sev":random.choice(["CRITICAL","MAJOR","MINOR"]),"typ":random.choice(["LinkDown","HighLatency","PacketLoss"]),"elem":random.choice(["gNodeB-1","RU-2","CU-UP-3"]),"msg":"auto-gen","ts":now}
    ]
    return jsonify(s)
if __name__=="__main__":
    a.run(host="0.0.0.0",port=5055)