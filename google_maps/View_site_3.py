import sys  # sys 모듈은 파이썬 인터프리터와 관련된 함수와 변수들을 제공
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
)  # PyQt5의 주요 위젯을 임포트
from PyQt5.QtCore import QUrl  # URL 관리를 위한 클래스
from PyQt5.QtWebEngineWidgets import QWebEngineView  # 웹 페이지를 보여주기 위한 위젯

import os  # 운영 체제와 상호작용하기 위한 모듈
import folium  # 지도를 만들기 위한 라이브러리
import googlemaps  # Google Maps API 클라이언트
import environ

# pip install python-environ
env = environ.Env()
env.read_env()


# Google Maps API를 이용하여 장소의 좌표를 얻어내는 클래스
class CoordinateFinder:
    def __init__(self, api_key):
        self.api_key = api_key  # Google Maps API 키 저장
        self.gmaps = googlemaps.Client(key=api_key)  # Google Maps 클라이언트 객체 생성

    # 장소의 이름을 받아 좌표(위도, 경도)를 반환하는 메서드
    def get_place_coordinates(self, place):
        try:
            # 장소 이름으로 자동완성 결과를 얻어옴
            autocomplete_result = self.gmaps.places_autocomplete(place, language="ko")
            if autocomplete_result:
                # 첫 번째 자동완성 결과의 장소명을 사용
                corrected_place = autocomplete_result[0]["description"]
                # 수정된 장소명으로 지오코딩하여 좌표 정보를 얻음
                geocode_result = self.gmaps.geocode(corrected_place)
                location = geocode_result[0]["geometry"]["location"]
                return location["lat"], location["lng"]  # 위도, 경도 반환
            else:
                print("장소에 대한 결과를 찾을 수 없습니다.")
                return None
        except Exception as e:
            print("오류:", e)
            return None


# folium을 이용해 지도를 생성하고 HTML 파일로 저장하는 클래스
class MapGenerator:
    def __init__(self, api_key):
        self.api_key = api_key

    # 지도 생성 및 HTML 파일로 저장하는 메서드
    def generate_map(
        self, center, zoom_level=20, map_type="Stamen Terrain", place_name=""
    ):
        m = folium.Map(
            location=center, zoom_start=zoom_level, tiles=map_type
        )  # folium으로 지도 객체 생성
        folium.Marker(location=center, popup=place_name).add_to(m)  # 지도에 마커 추가
        html_file_name = (
            f"{place_name}.html" if place_name else "map.html"
        )  # 저장할 HTML 파일 이름
        m.save(html_file_name)  # 지도를 HTML 파일로 저장
        return os.path.abspath(html_file_name)  # 저장된 파일의 절대 경로 반환


# PyQt5 기반의 애플리케이션 메인 윈도우 클래스
class MyApp(QWidget):
    def __init__(self, api_key):
        super().__init__()
        self.api_key = api_key  # Google Maps API 키
        self.initUI()  # UI 초기화

    def initUI(self):
        self.layout = QVBoxLayout()  # 수직 박스 레이아웃 생성
        self.pnuInput = QLineEdit(self)  # 사용자 입력을 받을 QLineEdit 위젯 생성
        self.pnuInput.setPlaceholderText(
            "장소를 입력하세요"
        )  # 플레이스홀더 텍스트 설정
        self.layout.addWidget(self.pnuInput)  # 레이아웃에 입력 필드 추가

        submitButton = QPushButton("제출", self)  # 제출 버튼 생성
        submitButton.clicked.connect(self.onSubmit)  # 버튼 클릭 시 onSubmit 메서드 연결
        self.layout.addWidget(submitButton)

        self.webView = QWebEngineView()  # 웹 페이지를 표시할 QWebEngineView 위젯 생성
        self.layout.addWidget(self.webView)  # 레이아웃에 웹 뷰 위젯 추가

        self.setLayout(self.layout)  # 위젯에 레이아웃 설정
        self.setWindowTitle("주소, 이미지, 지도 표시하기")  # 윈도우 타이틀 설정
        self.setGeometry(600, 600, 800, 600)  # 윈도우의 위치와 크기 설정

    # '제출' 버튼 클릭 시 실행되는 메서드
    def onSubmit(self):
        place = self.pnuInput.text()  # 사용자 입력에서 텍스트(장소 이름) 추출
        coordinate_finder = CoordinateFinder(self.api_key)  # 좌표 찾기 객체 생성
        coordinates = coordinate_finder.get_place_coordinates(
            place
        )  # 장소의 좌표를 얻음

        # 좌표가 성공적으로 얻어진 경우
        if coordinates:
            map_generator = MapGenerator(self.api_key)  # 지도 생성 객체 생성
            # 지도를 생성하고, 그 결과로 얻은 HTML 파일의 경로를 저장
            html_file_path = map_generator.generate_map(
                coordinates, map_type="OpenStreetMap", place_name=place
            )
            # QWebEngineView를 사용해 해당 HTML 파일을 띄움
            self.webView.setUrl(QUrl.fromLocalFile(html_file_path))
        else:
            print("장소의 좌표를 가져오는 데 실패했습니다.")


# 프로그램의 진입점
if __name__ == "__main__":
    app = QApplication(sys.argv)  # QApplication 객체 생성
    api_key = env("GOOGLE_API_KEY")  # Google Maps API 키 (실제 키로 교체 필요)
    ex = MyApp(api_key)  # 메인 윈도우 객체 생성
    ex.show()  # 메인 윈도우 보여주기
    sys.exit(app.exec_())  # 애플리케이션 실행
