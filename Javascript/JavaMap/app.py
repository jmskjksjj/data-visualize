from flask import Flask, render_template, request
import requests
import folium

app = Flask(__name__)

def get_coordinates(building_name):
    # 카카오 맵 API 요청을 위한 URL과 API 키 설정
    kakao_api_url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    kakao_api_key = "APIKEY"  # 여기에 본인의 API 키를 입력하세요

    # 요청 파라미터 설정
    params = {
        "query": building_name,
        "page": 1,
        "size": 1  # 검색 결과 중 첫 번째 결과만 가져옴
    }

    # 헤더 설정 (API 키를 포함)
    headers = {
        "Authorization": f"KakaoAK {kakao_api_key}"
    }

    # API 호출
    response = requests.get(kakao_api_url, params=params, headers=headers)
    data = response.json()

    # 결과 확인
    if 'documents' in data and len(data['documents']) > 0:
        # 첫 번째 검색 결과의 위도와 경도 추출
        latitude = data['documents'][0]['y']
        longitude = data['documents'][0]['x']
        return latitude, longitude
    else:
        return None, None

def search_hospitals(latitude, longitude, radius=None):
    # 카카오 맵 API 요청을 위한 URL과 API 키 설정
    kakao_api_url = "https://dapi.kakao.com/v2/local/search/category.json"
    kakao_api_key = "c9729f11ed53ad49c639ec07d649d56c"  # 여기에 본인의 API 키를 입력하세요

    # 요청 파라미터 설정
    params = {
        "category_group_code": "HP8",  # 병원 카테고리 코드
        "radius": radius,
        "x": longitude,
        "y": latitude
    }

    # 헤더 설정 (API 키를 포함)
    headers = {
        "Authorization": f"KakaoAK {kakao_api_key}"
    }

    # API 호출
    response = requests.get(kakao_api_url, params=params, headers=headers)
    data = response.json()

    # 결과 확인 및 처리
    hospitals = []
    if 'documents' in data and len(data['documents']) > 0:
        for hospital in data['documents']:
            name = hospital['place_name']
            lat = hospital['y']
            lng = hospital['x']
            hospitals.append((name, lat, lng))
    return hospitals

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        building_name = request.form['building_name']
        latitude, longitude = get_coordinates(building_name)
        if latitude is not None and longitude is not None:
            hospitals = search_hospitals(latitude, longitude)
            if hospitals:
                map_hospitals = folium.Map(location=[latitude, longitude], zoom_start=10, tiles='CartoDB positron')
                folium.Marker(location=[latitude, longitude], popup=building_name).add_to(map_hospitals)
                for hospital in hospitals:
                    folium.CircleMarker(location=(hospital[1], hospital[2]), radius=10, color='red', fill=True, fill_color='pink', fill_opacity=0.7, popup=hospital[0]).add_to(map_hospitals)
                map_hospitals.save('templates/hospitals_map.html')
                return render_template('index.html', map_exists=True)
            else:
                return render_template('index.html', error_message="No hospitals found in the vicinity.")
        else:
            return render_template('index.html', error_message="Could not find coordinates for the provided building name.")
    return render_template('index.html', map_exists=False)

if __name__ == "__main__":
    app.run(debug=True)
