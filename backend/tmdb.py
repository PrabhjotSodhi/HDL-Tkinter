import requests
import json

class TMDB:
    def __init__(self):
        self.api_key = "4a8701d372bc34afefe25162a4b71cff"

        self.genre_options = {
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

    def search_drama(self, drama):
        drama_url = f"https://api.themoviedb.org/3/search/tv?api_key={self.api_key}&query={drama}"
        drama_response = requests.request("GET", drama_url)
        results = drama_response.json()['results']

        filter_results = [x for x in results if x['original_language'] == 'ko']
        try:
            genres = ','.join([self.genre_options.get(i) for i in filter_results[0]['genre_ids'] if i is not None])
        except: #TypeError
            genres = "Drama"

        filter_json = {
            "id": filter_results[0]['id'],
            "name": filter_results[0]['name'],
            "year": filter_results[0]['first_air_date'][:4],
            "description": filter_results[0]['overview'],
            "genres": genres,
            "poster_path": f"http://image.tmdb.org/t/p/original{filter_results[0]['poster_path']}",
        }
        #final_json = json.dumps(filter_json)
        #print(filter_json["genres"])
        return filter_json
