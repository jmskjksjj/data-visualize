import requests
import urllib.parse

def get_building_info(keyword):
    # SGIS API 엔드포인트 URL
    api_url = "https://sgisapi.kostat.go.kr/OpenAPI3/auth/authentication.json"

    # API 키
    api_key = "8f2108d175da4b86a0da"

    # 주소를 URL 인코딩
    encoded_address = urllib.parse.quote(keyword)

    # 요청 파라미터 설정
    params = {
        "pageUnit": 10,  # 한 페이지에 포함되는 건물 정보 수
        "address": encoded_address,  # 검색 키워드
        # 다른 요청 파라미터도 필요한 경우 여기에 추가
        "apiKey": api_key  # API 키 추가
    }

    try:
        # API 호출
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # 오류가 발생하면 예외를 발생시킴

        # JSON 응답 파싱
        data = response.json()

        # 결과 확인
        if 'resultList' in data:
            building_list = data['resultList']
            for building in building_list:
                name = building.get('BULD_NM', '')
                latitude = building.get('LAT', '')
                longitude = building.get('LNG', '')
                address = building.get('ADDRESS', '')
                print(f"Name: {name}, Latitude: {latitude}, Longitude: {longitude}, Address: {address}")
            return building_list
        else:
            print("No building information found.")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return []

def main():
    keyword = input("검색할 키워드를 입력하세요: ")
    building_info = get_building_info(keyword)
    

if __name__ == "__main__":
    main()
