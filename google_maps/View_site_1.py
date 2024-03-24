import os
from selenium import webdriver
import time
import folium
import warnings


warnings.filterwarnings(action="ignore")
import googlemaps
import environ

# pip install python-environ
env = environ.Env()
env.read_env()


# 장소 경위도값 알아내는 함수
def get_place_coordinates(api_key, place):
    gmaps = googlemaps.Client(key=api_key)
    try:
        autocomplete_result = gmaps.places_autocomplete(place, language="ko")
        # 장소명 자동완성 기능 사용하기
        if autocomplete_result:
            corrected_place = autocomplete_result[0]["description"]

            geocode_result = gmaps.geocode(corrected_place)

            location = geocode_result[0]["geometry"]["location"]
            latitude = location["lat"]
            longitude = location["lng"]
            return latitude, longitude
        else:
            print("장소에 대한 결과를 찾을 수 없습니다.")
            return None
    except Exception as e:
        print("오류:", e)
        return None


# selenium을 이용해 웹 지도를 캡쳐해서 저장하는 함수
def convert_html_to_jpg(html_file_path, output_image_path):
    # 웹드라이버 초기화
    driver = webdriver.Chrome()

    # file:// 프로토콜을 사용하여 HTML 파일 열기
    driver.get("file://" + html_file_path)

    # 렌더링 로딩 시간 주기
    time.sleep(3)

    # 스크린샷 캡처하고 JPG 파일로 저장
    driver.save_screenshot(output_image_path)

    # 웹드라이버 종료
    driver.quit()


# folium 맵을 제작
def generate_map(api_key, center, zoom_level=20, map_type="Stamen Terrain"):
    m = folium.Map(location=center, zoom_start=zoom_level, tiles=map_type)
    folium.Marker(location=center).add_to(m)
    return m


def main():
    # Google 지도 API 키 입력
    api_key = env("GOOGLE_API_KEY")

    # 사용자로부터 장소 입력 받기
    place = input("검색할 장소를 입력하세요: ")

    # 위도와 경도 가져오기
    coordinates = get_place_coordinates(api_key, place)

    if coordinates is not None:
        latitude, longitude = coordinates
        center = [latitude, longitude]
        # Folium 맵 객체 생성
        m = generate_map(
            api_key, center, map_type="OpenStreetMap"
        )  # OpenStreetMap을 사용하도록 수정
        folium.Marker(location=center, popup=place).add_to(m)
        m.save(place + ".html")

        # 파일 이름 지정하기
        current_directory = os.getcwd()
        print(current_directory)
        html_file_path = current_directory + "\\" + place + ".html"
        output_image_path = place + ".jpg"

        convert_html_to_jpg(html_file_path, output_image_path)
    else:
        print("장소의 좌표를 가져오는 데 실패했습니다.")


# 메인 함수 실행
if __name__ == "__main__":
    main()
