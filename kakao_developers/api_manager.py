import requests
import openpyxl
import environ
import folium
from enum import Enum
class OptionEnum(Enum):
    MARKER = 1
    EXCEL = 2

class SoYoonManager:
    """쏘윤 매니져"""
    def __init__(self):
        self.api_key = self.load_api_key()
        # 검색할 건물 이름들
        self.building_names = ["국립중앙박물관", "서울시청", "롯데월드타워"]

    def search(self, option:OptionEnum):
        if option == "excel":
            return self.search_all_to_excel()
        if option == "marker":
            return self.search_all_and_mark()
        
    def search_all_to_excel(self):
        """복수개의 건물 이름을 가지고 위도 경도를 탐색하고, 위도 경도가 있는 경우들만 모아서 엑셀로 저장"""
        building_data = self.get_building_data()
        self.export_to_excel(building_data)
        print("모든 건물 정보를 엑셀 파일로 저장했습니다.")

    def add_marker(self, building_data, map):
        for building in building_data:
            folium.CircleMarker(
                location=[building["latitude"], building["longitude"]],
                radius=50,
                color="blue",
                fill=True,
                fill_color="blue",
            ).add_to(map)

    def search_all_and_mark(self):
        building_data = self.get_building_data()

        # 지도에 CircleMarker로 표시
        map = folium.Map(
            location=[37.5665, 126.9780], zoom_start=12
        )  # 서울 시청을 기준으로 지도 표시
        self.add_marker(building_data, map)
        
        map.save("building_locations_map.html")
        print("지도를 HTML 파일로 저장했습니다.")

    def search_all_draw_line(self):
        building_data = self.get_building_data()

        # 지도에 CircleMarker로 표시
        map = folium.Map(
            location=[37.5665, 126.9780], zoom_start=12
        )  # 서울 시청을 기준으로 지도 표시
        self.add_marker(building_data, map)
        
        # 중심점을 잇는 선 추가
        center_point = [
            sum(coord) / len(coord)
            for coord in zip(
                *[
                    [building["latitude"], building["longitude"]]
                    for building in building_data
                ]
            )
        ]
        for building in building_data:
            folium.PolyLine(
                [center_point, [building["latitude"], building["longitude"]]], color="red"
            ).add_to(map)
        map.save("building_locations_map.html")
        print("지도를 HTML 파일로 저장했습니다.")

    def load_api_key(self):
        # pip install python-environ
        env = environ.Env()
        env.read_env()
        # 카카오 REST API 키
        return env("KAKAO_API_KEY")

    def get_location(self, name):
        """name을 가지고 위도 경도 리턴"""
        url = f"https://dapi.kakao.com/v2/local/search/keyword.json?query={name}"
        headers = {"Authorization": f"KakaoAK {self.api_key}"}
        response = requests.get(url, headers=headers)
        data = response.json()
        if data.get("documents"):
            location = data["documents"][0]
            return location["y"], location["x"]
        else:
            return None, None


    def export_to_excel(self, building_data):
        """위도 경도, 건물 이름 저장하기"""
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["Name", "Latitude", "Longitude"])
        for building in building_data:
            ws.append([building["name"], building["latitude"], building["longitude"]])
        wb.save("building_locations.xlsx")

    def get_building_data(self):
        building_data = []
        for name in self.building_names:
            latitude, longitude = self.get_location(name)
            if latitude and longitude:
                building_data.append(
                    {"name": name, "latitude": latitude, "longitude": longitude}
                )
                print(
                    f"위도: {latitude}, 경도: {longitude}를 가진 건물의 정보를 저장했습니다."
                )
            else:
                print(f"{name}의 정보를 찾을 수 없습니다.")
        return building_data
    