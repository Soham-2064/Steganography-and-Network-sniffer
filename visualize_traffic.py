import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect('traffic.db')

# 1️⃣ Protocol distribution
df_proto = pd.read_sql_query(
    "SELECT protocol, COUNT(*) as count FROM packets GROUP BY protocol", conn
)
proto_map = {6: 'TCP', 17: 'UDP', 1: 'ICMP'}
df_proto['Protocol'] = df_proto['protocol'].map(proto_map).fillna(df_proto['protocol'].astype(str))

plt.figure(figsize=(6, 5))
plt.bar(df_proto['Protocol'], df_proto['count'])
plt.title("📊 Packet Count by Protocol")
plt.xlabel("Protocol")
plt.ylabel("Number of Packets")
plt.tight_layout()
plt.show()

# 2️⃣ Top 5 Active Source IPs
df_src = pd.read_sql_query(
    "SELECT src_ip, COUNT(*) as packets FROM packets GROUP BY src_ip ORDER BY packets DESC LIMIT 5",
    conn
)

plt.figure(figsize=(7, 5))
plt.barh(df_src['src_ip'], df_src['packets'], color='teal')
plt.title("🌐 Top 5 Source IPs by Packet Count")
plt.xlabel("Packets Sent")
plt.ylabel("Source IP")
plt.tight_layout()
plt.show()

# 3️⃣ Packet size over time (optional)
df_time = pd.read_sql_query(
    "SELECT timestamp, size FROM packets ORDER BY timestamp ASC", conn
)
if not df_time.empty:
    df_time['timestamp'] = pd.to_datetime(df_time['timestamp'])
    plt.figure(figsize=(9, 5))
    plt.plot(df_time['timestamp'], df_time['size'], marker='o', linewidth=1)
    plt.title("⏱️ Packet Size Over Time")
    plt.xlabel("Time")
    plt.ylabel("Packet Size (bytes)")
    plt.tight_layout()
    plt.show()

conn.close()
