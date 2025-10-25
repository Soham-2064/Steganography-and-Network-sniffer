# this module is alert mechanism

from collections import defaultdict
from typing import Tuple, Optional
from trafficdb import get_connection, now_ts

class AlertManager:
    def __init__(self, threshold: int = 50, repeat_interval: Optional[int] = None):
        self.threshold = threshold
        self.repeat_interval = repeat_interval
        self.counts: defaultdict[str, int] = defaultdict(int)
        self.alerted: set[str] = set()  
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def process_packet(self, src_ip: str) -> Tuple[bool, Optional[str]]:
        self.counts[src_ip] += 1
        cnt = self.counts[src_ip]

        if cnt > self.threshold:
            ts = now_ts()
            msg = f"⚠️ ALERT: Suspicious activity from {src_ip} (Sent {cnt} packets)"
            # log alert in DB
            self.cursor.execute(
                "INSERT INTO alerts (src_ip, count, timestamp) VALUES (?, ?, ?)",
                (src_ip, cnt, ts)
            )
            self.conn.commit()
            return (True, msg)

        return (False, None)

    def _register_alert(self, src_ip: str, count: int) -> Tuple[bool, str]:
        ts = now_ts()
        msg = f"⚠️ ALERT: Suspicious activity from {src_ip} (Sent {count} packets)"
        self.cursor.execute(
            "INSERT INTO alerts (src_ip, count, timestamp) VALUES (?, ?, ?)",
            (src_ip, count, ts)
        )
        self.conn.commit()
        if not self.repeat_interval:
            self.alerted.add(src_ip)
        return (True, msg)

    def close(self) -> None:
        self.conn.close()

