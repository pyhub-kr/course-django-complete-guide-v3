import sqlite3

query = "1' OR 1=1 --"

print("검색어:", query)

connection = sqlite3.connect("melon-20230906.sqlite3")
cursor = connection.cursor()
connection.set_trace_callback(print)

param = '%' + query + '%'
# sql = f"SELECT * FROM songs WHERE 가수 LIKE '{param}' OR 곡명 LIKE '{param}'"
sql = "SELECT * FROM songs WHERE 가수 LIKE ? OR 곡명 LIKE ?"
cursor.execute(sql, [param, param])

column_names = [desc[0] for desc in cursor.description]

song_list = cursor.fetchall()

print("list size :", len(song_list))

for song_tuple in song_list:
    song_dict = dict(zip(column_names, song_tuple))
    # print(song_dict["곡명"], song_dict["가수"])
    print("{곡명} {가수}".format(**song_dict))

connection.close()
