import http.client
import json

conn = http.client.HTTPSConnection("v3.football.api-sports.io")

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "f4a54bf55925e1a6e1eb0957979c199b"
    }


conn.request("GET", "/players/topscorers?season=2021&league=61", headers=headers)

top_scorers_res = conn.getresponse()
top_scorers_data = top_scorers_res.read()

# Parse JSON data correctly
top_scorers_json = json.loads(top_scorers_data.decode("utf-8"))

# Write formatted JSON to file
with open("top_scorers.json", "w", encoding='utf-8') as outfile:
    json.dump(top_scorers_json, outfile, indent=2, ensure_ascii=False)

################################################# TOP ASSISTS ############################################################
conn.request("GET", "/players/topassists?season=2021&league=61", headers=headers)

top_assists_res = conn.getresponse()
top_assists_data = top_assists_res.read()

# Parse JSON data correctly
top_assists_json = json.loads(top_assists_data.decode("utf-8"))

# Write formatted JSON to file
with open("top_assists.json", "w", encoding='utf-8') as outfile:
    json.dump(top_assists_json, outfile, indent=2, ensure_ascii=False)


