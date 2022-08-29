import requests 
from geopy import Nominatim   # GPS 좌표 처리


class GPSCoordinate:
    '''지도 좌표(위도, 경도) 처리 담당 클래스'''
    
    def __init__(self, config):
        '''사용자 설정에 따라 GPS 정보 초기화
        1. 파일에서 좌표 로딩:
            --from_file 선택된 경우 파일로부터 gps 값 로딩 (파일 기본위치: './location.txt')
        2. 사용자 입력받아 로딩 (--from_file 설정이 없는 경우)
            --lat, --lang 값이 입력된 경우 터미널에서 전달 받은 값으로 초기화
        '''
        self.current_loc_lat: float = None # 현재 위도
        self.current_loc_lng: float = None # 현재 경도
        self.geo_fn = config.geo_fn
        
        if config.from_file:
            self.current_loc_lat, self.current_loc_lng = self.get_current_coordinate_from_file()
        elif config.from_ip:
            self.current_loc_lat, self.current_loc_lng = self.get_current_coordinate_from_ip()
        else:
            if config.lat <= -90.0 or config.lat >= 90.0:
                print(f'\n입력한 위도(latitude) 좌표: --lat {config.lat}\n >>> 위도(latitude) 좌표의 첫 번째 숫자는 -90과 90 사이여야 합니다.\n')
                exit(-1)
            elif config.lng <= -180.0 or config.lng >= 180.0:
                print(f'\n입력한 경도(longitude) 좌표: --lng {config.lat}\n >>> 경도(longitude) 좌표의 첫 번째 숫자는 -180과 180 사이여야 합니다.\n')
                exit(-1)
            else:
                self.current_loc_lat = config.lat # 현재 위도
                self.current_loc_lng = config.lng # 현재 경도

    def get_current_coordinate_from_file(self, file_path: str = None):
        '''저장된 파일로부터 현재 GPS 좌표 가져오기
        파일에 저장 좌표 양식: 위도(실수), 경도(실수)
        '''
        if not file_path:
            file_path = self.geo_fn
        
        with open(file_path, 'r') as f:
            coordinate = f.read()
            lat, lng = coordinate.split(',')
            lat = float(lat.strip())
            lng = float(lng.strip())
        return (lat, lng)
    
    
    def get_current_coordinate_from_ip(self,):
        '''컴퓨터 IP 주소를 이용하여  현재 GPS 좌표 가져오기
        파일에 저장 좌표 양식: 위도(실수), 경도(실수)
        '''
        resp1 = requests.get('https://api64.ipify.org?format=json').json()
        ip_address = resp1['ip']
        resp2 = requests.get(f'https://ipapi.co/{ip_address}/json/').json()

        # print(f'접속 IP 정보\n{resp2}')
        print(f"\n>>> 현재 컴퓨터의 접속 정보")
        print(f"컴퓨터의 IP 주소: {resp2['ip']}")
        print(f"접속 위치: {resp2['country_name']} {resp2['region']} {resp2['city']}")
        print(f"접속 기관: {resp2['org']}")
        print(f"위도: {resp2['latitude']}, 경도: {resp2['longitude']}")

        lat = float(resp2['latitude'])
        lng = float(resp2['longitude'])
        return (lat, lng)
    

    def get_geo_info_by_coordiation(self,):
        '''현재 gps 좌표에 해당하는 장소 이름 반환'''
        geolocator = Nominatim(user_agent='cju emergency_path_finder',)
        geo_info = geolocator.reverse(f'{self.current_loc_lat}, {self.current_loc_lng}')
        if geo_info:
            location_name = geo_info.address
            if ',' in location_name:
                temp_string = location_name.replace(' ', '').split(',')
                temp_string = temp_string[::-1]
                location_name = ' '.join(temp_string)
            print(f'\n>>> 현재 좌표 위치(이름): {location_name}')
        else:
            location_name = ''
            print('\n>>> 현재 GPS에 해당하는 지명을 찾을 수 없습니다.')
        
        return location_name

    
    def print_gps_coordinate(self,):
        '''GPS 좌표 출력'''
        print(f'\n>>> 현재 GPS 좌표: 위도: {self.current_loc_lat} \t 경도: {self.current_loc_lng}')
    