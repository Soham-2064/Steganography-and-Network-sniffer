# this module handles packet logging

from scapy.all import Packet, IP
from trafficdb import get_connection, now_ts

class PacketLogger:
    def __init__(self, db_path=None):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def log_packet(self, packet: Packet):
        if IP in packet:
            src = packet[IP].src
            dst = packet[IP].dst
            proto = packet[IP].proto
            size = len(packet)
            ts = now_ts()
            self.cursor.execute(
                "INSERT INTO packets (src_ip, dst_ip, protocol, size, timestamp) VALUES (?, ?, ?, ?, ?)",
                (src, dst, proto, size, ts)
            )
            self.conn.commit()
            return (src, dst, proto, size, ts)
        return None

    def close(self):
        self.conn.close()
