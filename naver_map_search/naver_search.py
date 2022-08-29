import requests 
import argparse
import json
from gps_coordinate import GPSCoordinate


class NaverMapSearch:
    
    def __init__(self, config, gps: GPSCoordinate) -> None:
        self.config: argparse = config
        self.keyword: str = config.keyword
        self.lat: float = float(gps.current_loc_lat)
        self.lng: float = float(gps.current_loc_lng)
        self.max_list: int = config.max_list
    
    def print_gps_location(self,) -> None:
        '''GPS 좌표 출력'''
        print(f'\n>>> 현재 GPS 좌표:  위도: {self.lat} \t 경도: {self.lng}')
        
    def print_search_method(self,):
        if self.config.from_file:
            print(f'\n파일에 저장된 GPS 좌표를 사용하여 검색합니다.')
        elif self.config.from_ip: 
            print(f'\n현재 컴퓨터가 사용하고 있는 IP를 참고하여 검색합니다.\n주의!!! IP기반 추적은 오차가 존재합니다..')
        elif (self.config.lat is not None) and (self.config.lng is not None):
            print(f'\n사용자가 터미널에 입력한 GPS 좌표값을 사용하여 검색합니다.')
            
        
    def get_nearest_location(self,):
        '''현재 gps 좌표에서 가장 가까운 장소 추출
        - 가까운 장소 검색 기준: --keyword <검색어> (입력 안할 경우 default '지구대')
        - 장소 추출 갯수: --max_list <검색결과 갯수> (입력 안할 경우 default 5)
        '''
        
        url = 'https://map.naver.com/v5/api/search'
   
        payload = {
            'caller': 'pcweb',
            'query': self.keyword,
            'type': 'all',
            'searchCoord': f'{self.lng};{self.lat}',
            'page': '1',
            'displayCount': self.max_list,
            'isPlaceRecommendationReplace': 'true',
            'lang': 'ko',
        }
            
        headers = {
            'cache-control': 'no-cache, no-store, max-age=0, must-revalidate',
        }
        
        resp = requests.get(url, headers=headers, params=payload)
        resp.encoding = 'utf-8'
        
        if resp.status_code == 200:
            result = json.loads(resp.content)
            place_list = result['result']['place']['list']
            print(f'\n>>> 입력 키워드: "{self.keyword}" --> 검색 결과({self.max_list})개')
            with open(self.config.save_fn, 'w') as f:
                f.write('no,name, latitude, longitude, phone, distance, address\n')
                for idx, place in enumerate(place_list):
                    name = place['name'].replace('</br>', '').replace('</b>', '').replace('<b>', '').replace(',', '')
                    latitude = place['y']
                    longitude = place['x']
                    phone = place['tel']
                    distance = float(place['distance'])
                    address = place['roadAddress']
                    
                    print(
                        '{} 이름: {}\t위도: {}\t경도: {}\t전화번호: {}\t현위치로부터의 거리: {} Km\t주소: {}'.format(
                            idx+1, name, 
                            latitude, longitude, 
                            phone, round(distance/1000, 2), 
                            address
                        )
                    )
                    
                    f.write(
                        '{},{},{},{},{},{},{}\n'.format(
                            idx+1, name, 
                            latitude, longitude, 
                            phone, round(distance/1000, 2), 
                            address
                        )
                    )
            print(f'\n>>> 검색 결과는 현재 디렉토리 {self.config.save_fn}로 저장되었습니다.')
        else:
            print(f'\n>>> 정보를 가져올 수 없습니다. HTTP 상태코드: {resp.status_code}')
         