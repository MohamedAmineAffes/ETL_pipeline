import http.client
import json

conn = http.client.HTTPSConnection("v3.football.api-sports.io")

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "f4a54bf55925e1a6e1eb0957979c199b"
    }


conn.request("GET", "/players/topscorers?season=2021&league=61", headers=headers)

res = conn.getresponse()
data = res.read()

json_data = data.decode("utf-8")

# Serializing json
json_object = json.dumps(json_data)

# Writing to sample.json
with open("top_scorers.json", "w") as outfile:
    outfile.write(json_object)

################################################# TOP ASSISTS ############################################################
conn.request("GET", "/players/topassists?season=2021&league=61", headers=headers)
res = conn.getresponse()
data = res.read()

json_data2 = data.decode("utf-8")

# Serializing json
json_object2 = json.dumps(json_data2)

# Writing to sample.json
with open("top_assists.json", "w") as outfile:
    outfile.write(json_object2)



