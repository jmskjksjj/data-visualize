import requests

searching = '스타벅스 경복궁역점'
url = f'https://dapi.kakao.com/v2/local/search/keyword.json?query={searching}'

headers = {
    "Authorization": "KakaoAK c9729f11ed53ad49c639ec07d649d56c"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    places = data['documents']
    if places:
        for place in places:
            print(place)
    else:
        print("검색 결과가 없습니다.")
else:
    print("API 요청이 실패했습니다.")
