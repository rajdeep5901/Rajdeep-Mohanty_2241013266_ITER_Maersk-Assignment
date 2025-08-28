import datetime, time, logging
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import select
from .config import C
from .db import S, Alm, Notif, Kv, Rec
from .ndac_client import fetch
from .emailer import send_mail
log=logging.getLogger("ndac")
sch=BackgroundScheduler()
def now():
    return datetime.datetime.utcnow()
def last_poll(s):
    kv=s.get(Kv,"last_poll")
    if kv and kv.v:
        try:
            return datetime.datetime.fromisoformat(kv.v)
        except:
            pass
    return now()-datetime.timedelta(minutes=C.POLL_INTERVAL_MIN+1)
def set_last_poll(s,t):
    s.merge(Kv(k="last_poll",v=t.replace(microsecond=0).isoformat()))
def handle():
    with S() as s:
        lp=last_poll(s)
        x=fetch(lp)
        got=0; sent=0
        rc=[r.email for r in s.query(Rec).filter_by(active=True).all()]
        for a in x:
            got+=1
            if a.get("sev") not in ("CRITICAL","MAJOR"):
                continue
            if s.get(Alm,a["id"]) is None:
                s.merge(Alm(id=a["id"],sev=a.get("sev"),typ=a.get("typ"),elem=a.get("elem"),msg=a.get("msg"),ts=datetime.datetime.fromisoformat(a.get("ts"))))
            try:
                ok=send_mail(rc, a)
                s.add(Notif(alarm_id=a["id"],to_e=",".join(rc),status="SENT" if ok else "FAIL"))
                if ok:
                    sent+=1
            except Exception as e:
                s.add(Notif(alarm_id=a["id"],to_e=",".join(rc),status="ERROR"))
            s.commit()
        set_last_poll(s,now())
        s.commit()
        log.info(f"polled={got} sent={sent}")
def start():
    sch.add_job(handle,"interval",minutes=C.POLL_INTERVAL_MIN, id="poll")
    sch.start()