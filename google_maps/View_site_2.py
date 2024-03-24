import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

import os
import time
import folium
from selenium import webdriver
import googlemaps
import environ

# pip install python-environ
env = environ.Env()
env.read_env()


############################################################################################################
class CoordinateFinder:
    def __init__(self, api_key):
        self.api_key = api_key
        self.gmaps = googlemaps.Client(key=api_key)

    def get_place_coordinates(self, place):
        try:
            autocomplete_result = self.gmaps.places_autocomplete(place, language="ko")
            if autocomplete_result:
                corrected_place = autocomplete_result[0]["description"]
                geocode_result = self.gmaps.geocode(corrected_place)
                location = geocode_result[0]["geometry"]["location"]
                return location["lat"], location["lng"]
            else:
                print("장소에 대한 결과를 찾을 수 없습니다.")
                return None
        except Exception as e:
            print("오류:", e)
            return None


class MapGenerator:
    def __init__(self, api_key):
        self.api_key = api_key

    def generate_map(
        self, center, zoom_level=20, map_type="Stamen Terrain", place_name=""
    ):
        m = folium.Map(location=center, zoom_start=zoom_level, tiles=map_type)
        folium.Marker(location=center, popup=place_name).add_to(m)
        html_file_name = f"{place_name}.html" if place_name else "map.html"
        m.save(html_file_name)
        return os.path.abspath(html_file_name)


class ScreenshotTaker:
    def convert_html_to_jpg(self, html_file_path, output_image_path):
        driver = webdriver.Chrome()
        driver.get("file://" + html_file_path)
        time.sleep(3)
        driver.save_screenshot(output_image_path)
        driver.quit()


class MyApp(QWidget):
    def __init__(self, api_key):
        super().__init__()
        self.api_key = api_key
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        # 이미지 라벨 초기화 (이미지는 나중에 로드됨)
        self.lbl_img = QLabel()
        self.lbl_size = QLabel("Width: 0 Height: 0")
        self.lbl_size.setAlignment(Qt.AlignCenter)

        self.pnuInput = QLineEdit(self)
        self.pnuInput.setPlaceholderText("장소를 입력하세요")

        submitButton = QPushButton("제출", self)
        submitButton.clicked.connect(self.onSubmit)

        self.layout.addWidget(self.pnuInput)
        self.layout.addWidget(submitButton)
        self.layout.addWidget(self.lbl_img)
        self.layout.addWidget(self.lbl_size)

        self.setLayout(self.layout)
        self.setWindowTitle("주소, 이미지, 지도 표시하기")
        self.setGeometry(600, 600, 600, 400)

    def onSubmit(self):
        place = self.pnuInput.text()
        coordinate_finder = CoordinateFinder(self.api_key)
        coordinates = coordinate_finder.get_place_coordinates(place)

        if coordinates:
            map_generator = MapGenerator(self.api_key)
            html_file_path = map_generator.generate_map(
                coordinates, map_type="OpenStreetMap", place_name=place
            )

            screenshot_taker = ScreenshotTaker()
            output_image_path = f"{place}.jpg"
            screenshot_taker.convert_html_to_jpg(html_file_path, output_image_path)

            # 이미지를 로드하고 화면에 표시
            self.displayImage(output_image_path)
        else:
            print("장소의 좌표를 가져오는 데 실패했습니다.")

    def displayImage(self, image_path):
        pixmap = QPixmap(image_path)
        resized_pixmap = pixmap.scaled(
            200, 200, Qt.KeepAspectRatio, Qt.FastTransformation
        )
        self.lbl_img.setPixmap(resized_pixmap)
        self.lbl_size.setText(
            "Width: "
            + str(resized_pixmap.width())
            + " Height: "
            + str(resized_pixmap.height())
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    api_key = env("GOOGLE_API_KEY")
    ex = MyApp(api_key)
    ex.show()
    sys.exit(app.exec_())
