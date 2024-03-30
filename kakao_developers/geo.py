import requests
import openpyxl
import environ

# pip install python-environ
env = environ.Env()
env.read_env()
# 카카오 REST API 키
KAKAO_API_KEY = env("KAKAO_API_KEY")

# 검색할 건물 이름들
building_names = ["국립중앙박물관", "서울시청", "롯데월드타워"]


def get_location(name):
    url = f"https://dapi.kakao.com/v2/local/search/keyword.json?query={name}"
    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
    response = requests.get(url, headers=headers)
    data = response.json()
    if data.get("documents"):
        location = data["documents"][0]
        return location["y"], location["x"]
    else:
        return None, None


def export_to_excel(building_data):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Name", "Latitude", "Longitude"])
    for building in building_data:
        ws.append([building["name"], building["latitude"], building["longitude"]])
    wb.save("building_locations.xlsx")


def main():
    building_data = []
    for name in building_names:
        latitude, longitude = get_location(name)
        if latitude and longitude:
            building_data.append(
                {"name": name, "latitude": latitude, "longitude": longitude}
            )
            print(
                f"위도: {latitude}, 경도: {longitude}를 가진 건물의 정보를 저장했습니다."
            )
        else:
            print(f"{name}의 정보를 찾을 수 없습니다.")

    export_to_excel(building_data)
    print("모든 건물 정보를 엑셀 파일로 저장했습니다.")


if __name__ == "__main__":
    main()
