import requests
import json

api_key = "4a8701d372bc34afefe25162a4b71cff"
drama_name = "Squid Game"

drama_url = f"https://api.themoviedb.org/3/search/tv?api_key=4a8701d372bc34afefe25162a4b71cff&query={drama_name}"
drama_response = requests.request("GET", drama_url)
results = drama_response.json()['results']

filter_results = [x for x in results if x['original_language'] == 'ko']

genre_options = {
        35:"Comedy",
        18:"Drama",
        9648:"Mystery",
        10751:"Family",
        80:"Crime",
        10759:"Action & Adventure",
        10765:"Sci-Fi & Fantasy",
        10749:"Romance",
        10768:"War & Politics",
        10762:"Kids",
        None: None
}

filter_json = {
    'name': filter_results[0]['name'],
    'year': filter_results[0]['first_air_date'][:4],
    'description': filter_results[0]['overview'],
    'genres': [genre_options.get(i) for i in filter_results[0]['genre_ids'] if i is not None],
    'poster_path': f"https://image.tmdb.org/t/p/original{filter_results[0]['poster_path']}",
}

final_json = json.dumps(filter_json)
print(final_json)
