
import matplotlib.pyplot as plt
import pandas as pd

import geopandas as gpd #geojson 데이터 읽기
import folium   # 웹 기반 지도 시각화
from folium.plugins import HeatMap  

df = gpd.read_file('neighbourhoods.geojson', encoding='cp949')


## 기본 시각화
# fig, ax = plt.subplots(figsize=(10, 10))  # 그래프 크기 설정
# df.plot(ax=ax, color='lightblue', edgecolor='black')  # 지역별 색상 및 경계선 색상 설정
# ax.set_title('Neighbourhoods in Tokyo')  # 그래프 타이틀 설정
# plt.show()

### 지도위에 표시

# 지도 생성 (도쿄의 중심좌표를 예로 들었습니다)
m = folium.Map(location=[35.6895, 139.6917], zoom_start=12)

# GeoDataFrame을 GeoJSON으로 변환 후 Folium 지도에 추가
folium.GeoJson(df, name='geojson').add_to(m)

# 지도 표시
m.save('map.html')  # HTML 파일로 저장


### 다른 데이터를 불러와서 지도에 표시해봅시다. 데이터 전처리도 합시다
df_list_summary = pd.read_csv('listings_summary.csv') # 주요 컬럼
# df_list = pd.read_csv('listings.csv')   # 전체 컬럼 

print(df_list_summary.info())

# neighborhood는 데이터가 없어서 삭제
df_list_summary.drop('neighbourhood_group', axis=1, inplace=True)

# float으로 변환, coerce:변환 안되는 행은 NaN으로 처리 
df_list_summary['longitude'] = pd.to_numeric(df_list_summary['longitude'], errors='coerce')

# 위도 경도 데이터 없는 행 삭제
df_cleaned = df_list_summary.dropna(subset=['latitude', 'longitude'])

# 지도 생성 (도쿄의 중심좌표를 예로 들었습니다)
# 웹 기반으로 좋으나, 많은 데이터를 보여주는 것에는 한계있음, 예시는 10개만 포인트 출력
m2 = folium.Map(location=[35.6895, 139.6917], zoom_start=12)

# 데이터프레임의 각 행에 대해 마커 추가
for idx, row in df_cleaned[:10].iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"{row['name']}",  # 팝업에 표시할 이름
        tooltip=row['name']  # 마우스 오버시 표시할 이름
    ).add_to(m2)

# 지도 표시
m2.save('tokyo_map.html')  # HTML 파일로 저장


# 히트맵으로 시각화
m3 = folium.Map(location=[35.6895, 139.6917], zoom_start=12)

# 히트맵 레이어 추가
heat_data = [[row['latitude'], row['longitude']] for index, row in df_cleaned.iterrows()]
HeatMap(heat_data).add_to(m3)

# 지도 저장
m3.save('heatmap.html')


# 가격 정보를 시각화
import plotly.io as pio
import plotly.express as px
pio.renderers.default='browser'

df = df_cleaned
df.dropna(subset=['price'], inplace=True)

# Plotly Express를 사용한 3D 지도 그래프 생성
fig = px.scatter_3d(df, x='longitude', y='latitude', z='price',
                    color='price', size='price', color_continuous_scale='Viridis',
                    title='3D Visualization of Prices by Latitude and Longitude')

fig.show()


# Folium 지도 생성
map_tokyo = folium.Map(location=[35.6895, 139.6917], zoom_start=11)

# 각 지점에 CircleMarker 추가
for idx, row in df.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=row['price'] / 10000,  # 가격을 반영한 원의 크기 조절
        color='crimson',
        fill=True,
        fill_color='crimson',
        fill_opacity=0.6,
        popup=folium.Popup(f"Neighbourhood: {row['neighbourhood']}<br>Price: {row['price']}", max_width=200)
    ).add_to(map_tokyo)

# 지도 저장 및 표시
map_tokyo.save("map_tokyo_circle.html")