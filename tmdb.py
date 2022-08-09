import requests

api_key = "4a8701d372bc34afefe25162a4b71cff"
drama_name = "Game of Thrones"

drama_url = f"https://api.themoviedb.org/3/search/tv?api_key=4a8701d372bc34afefe25162a4b71cff&query={drama_name}"
drama_res = requests.request("GET", drama_url)
results = drama_res.json()['results']

print(results)
