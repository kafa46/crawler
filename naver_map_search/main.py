'''
작성자: 노기섭, 청주대학교
License: MIT License

Function Dirsciption:
    네이버 맵을 이용하여 현재 위치에서 가장 가까운 장소 추출
    - 현재위치: 사용자가 입력한 키워드
    - 가까운 장소: 네이버 맵의 키워드 검색 결과 단거리 순으로 추출

Reference List:
    - 네이버 지도 크롤링 관련 질문 ->  https://www.inflearn.com/questions/435531 
    - geopy official -> https://geopy.readthedocs.io/en/stable/
    - 컴퓨터 IP 주소를 이용한 위치 정보 추출 -> https://www.freecodecamp.org/news/how-to-get-location-information-of-ip-address-using-python/
'''

import argparse
from gps_coordinate import GPSCoordinate
from naver_search import NaverMapSearch


def argparser():
    parser = argparse.ArgumentParser(description='네이버 맴 검색 사용법입니다.')
    parser.add_argument('--keyword', default='지구대', help='검색할 키워드')
    parser.add_argument('--from_file', action='store_true', help='파일로부터 좌표 읽어오기 (기본값 False)')
    parser.set_defaults(from_file=True)
    parser.add_argument('--geo_fn', default='./location.txt', help='위도/경도가 저장된 파일 경로/이름')
    parser.add_argument('--from_ip', action='store_true', help='컴퓨터 IP 주소를 활용해 좌표 읽어오기 (기본값 False)')
    parser.add_argument('--lat', type=float, help='GPS 위도(latitude) 값')
    parser.add_argument('--lng', type=float, help='GPS 경도(longitude) 값')
    parser.add_argument('--max_list', type=int, default=10, help='위치 검색할 최대 갯수')
    parser.add_argument('--save_fn', type=str, default='result.csv', help='검색 결과를 저장할 파일 이름')
    
    # --from_file과 --from_ip는 동시에 사용 불가
    # group = parser.add_mutually_exclusive_group(required=True)
    # group.add_argument('--from_file', action='store_true', help='파일로부터 좌표 읽어오기 (기본값 False)')
    # group.add_argument('--from_ip', action='store_true', help='컴퓨터 IP 주소를 활용해 좌표 읽어오기 (기본값 False)')
    
    config = parser.parse_args()
    return config


def main(config):
    gps = GPSCoordinate(config)
    gps.get_geo_info_by_coordiation()
    
    naver = NaverMapSearch(config, gps)
    naver.print_search_method()
    naver.print_gps_location()
    naver.get_nearest_location()
       
            
if __name__=='__main__':
    config = argparser()
    main(config)
    
    
    