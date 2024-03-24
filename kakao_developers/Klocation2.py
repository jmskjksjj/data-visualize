import requests
import pandas as pd

# 검색할 여러 개의 키워드 설정
searching_list = ['스타벅스 경복궁역', '대구 맛집', '홍대 카페']

# DataFrame을 저장할 빈 리스트 생성
dfs = []

# Kakao Developers API에 요청을 보내어 검색 결과를 가져오는 함수
def get_places(searching):
    url = f'https://dapi.kakao.com/v2/local/search/keyword.json?query={searching}'
    headers = {"Authorization": "KakaoAK c9729f11ed53ad49c639ec07d649d56c"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get('documents', [])
    else:
        print(f"API 요청이 실패했습니다. ({searching})")
        return []

# 각 검색어에 대해 검색을 수행하고 DataFrame에 저장
for searching in searching_list:
    places = get_places(searching)
    if places:
        df = pd.DataFrame(places)
        dfs.append(df)

# 모든 DataFrame을 하나로 합치기
result_df = pd.concat(dfs, ignore_index=True)

# 결과를 엑셀 파일로 저장
result_df.to_excel("search_results.xlsx", index=False)
print("검색 결과를 search_results.xlsx 파일로 저장했습니다.")
