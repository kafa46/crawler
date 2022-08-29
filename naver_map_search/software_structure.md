# 네이버 근거리 좌표 검색

프로그램의 진입점인 main 모듈(`main.py`)과 2개의 클래스구성된 모듈로 구성되어 있습니다.

각 모듈의 구성과 역할은 다음과 같습니다.

- `gps_coordinate.py` 모듈
  - 지도상에서 필요한 좌표(위도, 경도) 처리를 담당하는 `GPSCoordinate` 클래스를 가지고 있습니다. 클래스의 구조는 다음과 같습니다.

    ```mermaid
    classDiagram
        class GPSCoordinate{
            +float current_loc_lat
            +float current_loc_lng
            +get_current_coordinate_from_file(file_path)
            +get_current_coordinate_from_ip()
            +get_geo_info_by_coordiation()
            +print_gps_coordinate()
        }
    ```

  - 사용자의 선택에 따라 위도/경도 좌표를 업로드 합니다.
    - `from_file` 옵션: 이 옵션이 선택된 경우 지정한 파일에서 위도, 경도 값을 읽어서 저장합니다. 설정하지 않을 경우 현재 디렉토리에서 `location.txt` 파일을 읽어옵니다. 파일 경로/이름을 별도로 지정하고 싶을 때는 `--geo_fn` 설정을 사용합니다. 읽어올 파일에는 반드시 `위도, 경도`와 같은 형태로 데이터가 저장되어 있어야 합니다.
    - `from_ip` 옵션: 현재 사용하고 있는 컴퓨터의 IP를 검사하고, 해당 IP가 접속하고 있는 장소을 확인합니다. IP가 접속하는 장소의 위도 경도를 확인하여 장소 정보를 제공합니다.  IP 추적을 통한 옵션은 시/군/동 단위까지는 정확하게 찾을 수 있지만 동 단위는 다를 수 있습니다. 사용자의 접속 위치는 컴퓨터가 접속하는 가까운 무선 기지국이나 서비스사업자의 지역 Router 주소이기 때문입니다.
    - `--lat`, `--lng` 사용자 입력 옵션: 사용자가 직접 위도(`latitude`), 경도(`longitude`)를 입력할 경우 사용합니다.

- `naver_search.py` 모듈
  - `GPSCoordinate` 클래스로부터 좌표(위도, 경도) 정보를 받아 사용자가 `--keyword` 옵션을 통해 전달한 키워드에 해당하는 좌표를 검색하는 `NaverMapSearch` 클래스를 가지고 있습니다. 클래스의 구조는 다음과 같습니다.

    ```mermaid
    classDiagram
        class NaverMapSearch{
            +obj config
            +str keyword
            +folat lat
            +float lng
            +int max_list
            +get_nearest_location()
            +print_search_method()
            +print_gps_location()

        }
    ```

    - 탐색한 결과는 사용자가 `--save_fn` 옵션을 통해 전달한 이름으로 파일로 저장합니다. 사용자가 입력하지 않을 경우 `result.csv`라는 이름으로 저장됩니다. 저장되는 정보는 다음과 같습니다.
      - `no`: 검색결과 순서
      - `name`: 검색된 장소의 지명[또는 상호, 또는 기관명]
      - `latitude`: 검색된 장소의 위도
      - `longitude`: 검색된 장소의 경도
      - `phone`: 검색된 장소의 전화번호 (국가번호는 생략됨)
      - `distance`: 현재 위치와 검색된 장소의 거리 (단위: Km)
      - `distance`: 검색된 장소의 주소
- `main.py` 모듈
  - 프로그램의 진입점 역할을 합니다.
  - `argparse` 함수를 이용하여 사용자로부터 프로그램에 필요한 정보를 전달 받습니다.
  - `main` 함수 내부에서 필요한 객체를 생성하고 연산을 수행합니다.

프로그램의 전체 구조는 다음과 같습니다.

```mermaid
classDiagram

    class argparser{
        parsing commandline
        arguments
    }
    class main{
        main function
        (entry point)
    }

    class GPSCoordinate{
        +float current_loc_lat
        +float current_loc_lng
        +get_current_coordinate_from_file(file_path)
        +get_current_coordinate_from_ip()
        +get_geo_info_by_coordiation()
        +print_gps_coordinate()
    }

    class NaverMapSearch{
        +obj config
        +str keyword
        +folat lat
        +float lng
        +int max_list
        +get_nearest_location()
        +print_search_method()
        +print_gps_location()
    }
    argparser <..main: Dependency
    GPSCoordinate <..NaverMapSearch: Dependency
    NaverMapSearch <--main: Association
```
