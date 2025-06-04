import json

# Read 2 jons files
# Opening JSON file
file_assists = open('top_assists.json')

# returns JSON object as a dictionary
data_assists = json.load(file_assists)

# Print the data
print(data_assists)

# Opening JSON file
file_scorers= open('top_scorers.json')

# returns JSON object as a dictionary
data_scorers= json.load(file_scorers)

# Print the data
print(data_scorers)

#Create new field "contribution"

