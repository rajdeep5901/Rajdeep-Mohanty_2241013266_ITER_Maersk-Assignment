import os, logging
from flask import Flask, jsonify, request, render_template, redirect, url_for
from .config import C
from .db import init_db, S, Rec, Alm, Notif
from .scheduler import start, handle
def create_app():
    a=Flask(__name__)
    a.config["SECRET_KEY"]=C.SECRET_KEY
    logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(), logging.FileHandler("logs/app.log")])
    init_db()
    start()
    @a.get("/health")
    def health():
        return {"ok":True}
    @a.get("/metrics")
    def metrics():
        with S() as s:
            ac=s.query(Alm).count()
            nc=s.query(Notif).count()
            rc=s.query(Rec).count()
        return {"alarms":ac,"notifications":nc,"recipients":rc}
    @a.post("/trigger")
    def trigger():
        t=request.headers.get("Authorization","")
        if not t.startswith("Bearer "): 
            return jsonify({"error":"unauthorized"}),401
        if t.split(" ",1)[1]!=C.ADMIN_TOKEN:
            return jsonify({"error":"unauthorized"}),401
        handle()
        return {"ok":True}
    @a.get("/dashboard")
    def dash():
        with S() as s:
            ns=s.query(Notif).order_by(Notif.id.desc()).limit(50).all()
            as_=[s.get(Alm,n.alarm_id) for n in ns]
            z=list(zip(ns,as_))
        return render_template("dashboard.html", rows=z)
    @a.get("/recipients")
    def recipients():
        t=request.headers.get("Authorization","")
        if not t.startswith("Bearer ") or t.split(" ",1)[1]!=C.ADMIN_TOKEN:
            return jsonify({"error":"unauthorized"}),401
        with S() as s:
            rs=[{"email":r.email,"name":r.name,"active":r.active} for r in s.query(Rec).all()]
        return {"recipients":rs}
    @a.post("/recipients")
    def add_recipient():
        t=request.headers.get("Authorization","")
        if not t.startswith("Bearer ") or t.split(" ",1)[1]!=C.ADMIN_TOKEN:
            return jsonify({"error":"unauthorized"}),401
        j=request.get_json(silent=True) or {}
        e=j.get("email","").strip()
        n=j.get("name")
        if not e: 
            return {"error":"email"},400
        with S() as s:
            s.merge(Rec(email=e,name=n,active=True)); s.commit()
        return {"ok":True}
    @a.delete("/recipients/<email>")
    def del_recipient(email):
        t=request.headers.get("Authorization","")
        if not t.startswith("Bearer ") or t.split(" ",1)[1]!=C.ADMIN_TOKEN:
            return jsonify({"error":"unauthorized"}),401
        with S() as s:
            r=s.get(Rec,email)
            if r: 
                s.delete(r); s.commit()
        return {"ok":True}
    return a