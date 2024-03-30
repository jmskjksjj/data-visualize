import requests
import folium
import environ

# pip install python-environ
env = environ.Env()
env.read_env()


def get_building_info(building_name, api_key):
    url = f"https://dapi.kakao.com/v2/local/search/keyword.json?query={building_name}"
    headers = {"Authorization": f"KakaoAK c9729f11ed53ad49c639ec07d649d56c"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if "documents" in data and len(data["documents"]) > 0:
            building_info = data["documents"][0]
            return building_info
    return None


def get_nearby_buildings(lat, lng, api_key):
    url = f"https://dapi.kakao.com/v2/local/search/keyword.json?category_group_code=PO3&x={lng}&y={lat}&radius=1000"
    headers = {"Authorization": f"KakaoAK c9729f11ed53ad49c639ec07d649d56c"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if "documents" in data:
            return data["documents"]
    return []


def visualize_building(building_info, nearby_buildings):
    lat = building_info["y"]
    lng = building_info["x"]
    building_name = building_info["place_name"]
    building_address = building_info["address_name"]

    m = folium.Map(location=[lat, lng], zoom_start=15)
    folium.Marker([lat, lng], popup=f"{building_name}<br>{building_address}").add_to(m)

    # 주변 건물 표시
    for nearby_building in nearby_buildings:
        nearby_lat = nearby_building["y"]
        nearby_lng = nearby_building["x"]
        nearby_name = nearby_building["place_name"]
        # 미술관인 경우 빨간색으로 마킹
        if nearby_building["category_group_code"] == "AT4":
            folium.Marker(
                [nearby_lat, nearby_lng],
                popup=nearby_name,
                icon=folium.Icon(color="red", icon_size=(100, 100)),
            ).add_to(m)
        else:
            folium.Marker(
                [nearby_lat, nearby_lng],
                popup=nearby_name,
                icon=folium.Icon(color="green"),
            ).add_to(m)

    m.save("building_location_with_nearby.html")
    print(
        "지도를 생성했습니다. 'building_location_with_nearby.html' 파일을 열어 확인하세요."
    )


if __name__ == "__main__":
    kakao_api_key = env("KAKAO_API_KEY")
    building_name = input("검색할 건물 이름을 입력하세요: ")

    building_info = get_building_info(building_name, kakao_api_key)
    if building_info:
        lat = building_info["y"]
        lng = building_info["x"]
        nearby_buildings = get_nearby_buildings(lat, lng, kakao_api_key)
        if nearby_buildings is not None:
            visualize_building(building_info, nearby_buildings)
        else:
            print("주변 건물 정보를 가져오지 못했습니다.")
    else:
        print("해당하는 건물을 찾을 수 없습니다.")
