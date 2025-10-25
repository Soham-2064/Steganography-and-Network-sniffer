from scapy.all import sniff, IP
from trafficdb import init_db
from packet_logger import PacketLogger
from packet_alert import AlertManager

def main():
    init_db()

    logger = PacketLogger()
    alert_mgr = AlertManager(threshold=15, repeat_interval=None)  #here the threshold is fixed

    def packet_callback(packet):
        logged = logger.log_packet(packet)
        if logged:
            src, dst, proto, size, ts = logged
            count = alert_mgr.counts.get(src, 0) + 1
            print(f"{src} → {dst} | Proto {proto} | Size {size} | Count {count}")

            should_alert, msg = alert_mgr.process_packet(src)
            if should_alert and msg:
                print("\n" + msg + "\n")

    try:
        print("...Sniffer with Alert System started! (Press Ctrl+C to stop)...")
        sniff(prn=packet_callback, store=False)
    except KeyboardInterrupt:
        print("\nStopping sniffer...")
    finally:
        logger.close()
        alert_mgr.close()
        print("...All DB connections closed. Exiting...")

if __name__ == "__main__":
    main()
