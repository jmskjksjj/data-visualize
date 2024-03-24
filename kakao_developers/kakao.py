import folium
import requests

def get_places(query, api_key):
    url = f"https://dapi.kakao.com/v2/local/search/keyword.json?query={query}"
    headers = {"Authorization": f"KakaoAK {api_key}"}
    response = requests.get(url, headers=headers)
    
    # API 요청이 성공했는지 확인
    if response.status_code != 200:
        print("API 요청이 실패했습니다.")
        return None
    
    data = response.json()
    
    # 'documents' 필드가 있는지 확인
    if 'documents' not in data:
        print("검색 결과가 없습니다.")
        return None
    
    places = data['documents']
    return places

def main():
    # Kakao Developers에서 발급받은 API 키를 입력하세요
    api_key = "c9729f11ed53ad49c639ec07d649d56c"

    # 검색할 장소의 키워드를 입력하세요
    query = input("검색할 장소 키워드를 입력하세요: ")

    places = get_places(query, api_key)

    if places:
        # 첫 번째 결과의 좌표를 기준으로 지도를 생성합니다
        center_lat = places[0]['y']
        center_lng = places[0]['x']
        map_center = [center_lat, center_lng]
        m = folium.Map(location=map_center, zoom_start=15)

        # 검색 결과의 모든 장소를 지도에 추가합니다
        for place in places:
            name = place['place_name']
            lat = place['y']
            lng = place['x']
            folium.Marker([lat, lng], popup=name).add_to(m)

        # HTML 파일로 지도를 저장하고 열기
        m.save("map.html")
        print("지도를 생성했습니다. 'map.html' 파일을 열어 확인하세요.")
    else:
        print("검색 결과가 없습니다.")

if __name__ == "__main__":
    main()
