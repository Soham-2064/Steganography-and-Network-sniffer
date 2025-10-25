# this module is analyzes the packets

import sqlite3
import pandas as pd

conn = sqlite3.connect('traffic.db')

# show protocol counts
df = pd.read_sql_query("SELECT protocol, COUNT(*) as count FROM packets GROUP BY protocol", conn)

proto_map = {6: 'TCP', 17: 'UDP', 1: 'ICMP'}
df['protocol_name'] = df['protocol'].map(proto_map).fillna(df['protocol'].astype(str))
df = df[['protocol', 'protocol_name', 'count']]
print(df)
print("")
# top 5 active IPs
df2 = pd.read_sql_query("SELECT src_ip, COUNT(*) as packets FROM packets GROUP BY src_ip ORDER BY packets DESC LIMIT 5", conn)
print(df2)


