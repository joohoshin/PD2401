import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import folium

df = gpd.read_file('neighbourhoods.geojson', encoding='cp949')


# 기본 시각화
fig, ax = plt.subplots(figsize=(10, 10))  # 그래프 크기 설정
df.plot(ax=ax, color='lightblue', edgecolor='black')  # 지역별 색상 및 경계선 색상 설정
ax.set_title('Neighbourhoods in Tokyo')  # 그래프 타이틀 설정
plt.show()

# 지도위에 표시

# 지도 생성 (도쿄의 중심좌표를 예로 들었습니다)
m = folium.Map(location=[35.6895, 139.6917], zoom_start=12)

# GeoDataFrame을 GeoJSON으로 변환 후 Folium 지도에 추가
folium.GeoJson(df, name='geojson').add_to(m)

# 지도 표시
m.save('map.html')  # HTML 파일로 저장
m  # Jupyter Notebook에서 바로 표시


# 다른 데이터를 불러와서 지도에 표시해봅시다
df_list_summary = pd.read_csv('listings_summary.csv') # 주요 컬럼
# df_list = pd.read_csv('listings.csv')   # 전체 컬럼

# neighborhood는 데이터가 없어서 삭제
df_list_summary.drop('neighbourhood_group', axis=1, inplace=True)
