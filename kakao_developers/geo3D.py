import requests
import openpyxl
import folium

# 카카오 REST API 키
KAKAO_API_KEY = 'c9729f11ed53ad49c639ec07d649d56c'

# 검색할 건물 이름들
building_names = [
    "국립중앙박물관",
    "서울시청",
    "롯데월드타워"
]

def get_location(name):
    url = f'https://dapi.kakao.com/v2/local/search/keyword.json?query={name}'
    headers = {'Authorization': f'KakaoAK {KAKAO_API_KEY}'}
    response = requests.get(url, headers=headers)
    data = response.json()
    if data.get('documents'):
        location = data['documents'][0]
        return float(location['y']), float(location['x'])  # 문자열을 실수형으로 변환하여 반환
    else:
        return None, None

def export_to_excel(building_data):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['Name', 'Latitude', 'Longitude'])
    for building in building_data:
        ws.append([building['name'], building['latitude'], building['longitude']])
    wb.save('building_locations.xlsx')

def main():
    building_data = []
    for name in building_names:
        latitude, longitude = get_location(name)
        if latitude and longitude:
            building_data.append({'name': name, 'latitude': latitude, 'longitude': longitude})
            print(f"위도: {latitude}, 경도: {longitude}를 가진 건물의 정보를 저장했습니다.")
        else:
            print(f"{name}의 정보를 찾을 수 없습니다.")
    
    # 엑셀 파일로 저장
    export_to_excel(building_data)
    print("모든 건물 정보를 엑셀 파일로 저장했습니다.")

    # 지도타입에 따른 타일사용하기
    m = folium.Map(location=[37.5665, 126.9780], zoom_start=12,tiles='Stamen Terrain')

    for building in building_data:
        folium.CircleMarker(
            location=[building['latitude'], building['longitude']],
            radius=50,
            color='coral',
            fill=True,
            fill_color='coral'
        ).add_to(m)

    # 중심점을 잇는 선 추가
    center_point = [sum(coord)/len(coord) for coord in zip(*[[building['latitude'], building['longitude']] for building in building_data])]
    for building in building_data:
        folium.PolyLine([center_point, [building['latitude'], building['longitude']]], color="red").add_to(m)

    m.save('building_locations_map.html')
    print("지도를 HTML 파일로 저장했습니다.")

if __name__ == "__main__":
    main()
