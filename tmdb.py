import requests
import json

api_key = "4a8701d372bc34afefe25162a4b71cff"
drama_name = ""

drama_url = f"https://api.themoviedb.org/3/search/tv?api_key=4a8701d372bc34afefe25162a4b71cff&query={drama_name}"
drama_response = requests.request("GET", drama_url)
results = drama_response.json()['results']

filter_results = [x for x in results if x['original_language'] == 'ko']
final_json = json.dumps(filter_results)

print(final_json)
