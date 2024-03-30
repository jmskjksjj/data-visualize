import requests
import folium
import environ

# pip install python-environ
env = environ.Env()
env.read_env()


def get_building_info(building_name, api_key):
    # Kakao 로컬 API를 사용하여 건물 정보를 가져오는 함수
    url = f"https://dapi.kakao.com/v2/local/search/keyword.json?query={building_name}"
    headers = {"Authorization": f"KakaoAK {api_key}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # 검색 결과에서 첫 번째 건물의 정보를 반환
        if "documents" in data and len(data["documents"]) > 0:
            building_info = data["documents"][0]
            return building_info
    return None


def visualize_building(building_info):
    # 건물 정보에서 위도와 경도 가져오기
    lat = building_info["y"]
    lng = building_info["x"]
    # 건물 이름과 주소 가져오기
    building_name = building_info["place_name"]
    building_address = building_info["address_name"]

    # 지도 생성 및 건물 위치 표시
    m = folium.Map(location=[lat, lng], zoom_start=15)
    folium.Marker([lat, lng], popup=f"{building_name}<br>{building_address}").add_to(m)

    # HTML 파일로 지도 저장
    m.save("building_location.html")
    print("지도를 생성했습니다. 'building_location.html' 파일을 열어 확인하세요.")


if __name__ == "__main__":
    # Kakao Developers에서 발급받은 API 키를 입력하세요
    kakao_api_key = env("KAKAO_API_KEY")

    # 건물 이름 입력
    building_name = input("검색할 건물 이름을 입력하세요: ")

    # 건물 정보 가져오기
    building_info = get_building_info(building_name, kakao_api_key)
    if building_info:
        # 건물 시각화
        visualize_building(building_info)
    else:
        print("해당하는 건물을 찾을 수 없습니다.")
