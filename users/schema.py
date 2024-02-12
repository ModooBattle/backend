from drf_yasg import openapi

login_res_schema = {
    "200": openapi.Response(
        description="로그인 성공",
        examples={
            "application/json": {
                "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwOTk0MzE3LCJpYXQiOjE3MDA5OTA3MTcsImp0aSI6IjhmYzlmYTJiYjY1ZjQwOTZiNjAwMmNlNGRkMTM2ZjViIiwidXNlcl9pZCI6MX0.MSba1A62OUdY3l8wvsNuIyQFxTobBMO1TfZDQ67dB70",
                "user": {
                    "id": 4,
                    "username": "테스트",
                    "weight": {"id": 1, "name": "미니멈", "min_weight": 46},
                    "age": "20",
                    "gender": "F",
                    "years": 4,
                    "last_login": "2024-02-12T13:10:59.224503",
                    "gym": {
                        "id": 1,
                        "name": "알로하복싱짐",
                        "address": "서울 강남구 논현동 90-6",
                        "latitude": 37.51558108296889,
                        "longitude": 127.0350141685017,
                        "sport": 1,
                    },
                    "current_location": "대구 동구 신암동 1881",
                },
            }
        },
    ),
    "401": openapi.Response(
        description="회원가입 필요", examples={"application/json": {"detail": "need to register", "email": "user@gmail.com"}}
    ),
    "404": openapi.Response(
        description="유효하지 않은 카카오 리다이렉트 코드", examples={"application/json": {"detail": "Not found."}}
    ),
    "403": openapi.Response(description="차단된 유저", examples={"application/json": {"detail": "blocked user"}}),
}

register_res_schema = {
    "201": openapi.Response(
        description="회원가입/로그인 성공",
        examples={
            "application/json": {
                "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwOTk0MzE3LCJpYXQiOjE3MDA5OTA3MTcsImp0aSI6IjhmYzlmYTJiYjY1ZjQwOTZiNjAwMmNlNGRkMTM2ZjViIiwidXNlcl9pZCI6MX0.MSba1A62OUdY3l8wvsNuIyQFxTobBMO1TfZDQ67dB70",
                "user": {
                    "id": 4,
                    "username": "테스트",
                    "weight": {"id": 1, "name": "미니멈", "min_weight": 46},
                    "age": "20",
                    "gender": "F",
                    "years": 4,
                    "last_login": "2024-02-12T13:10:59.224503",
                    "gym": {
                        "id": 1,
                        "name": "알로하복싱짐",
                        "address": "서울 강남구 논현동 90-6",
                        "latitude": 37.51558108296889,
                        "longitude": 127.0350141685017,
                        "sport": 1,
                    },
                },
            }
        },
    ),
    "403": openapi.Response(description="차단된 유저", examples={"application/json": {"detail": "blocked user"}}),
}

access_res_schema = {
    "200": openapi.Response(
        description="액세스토큰 재발급 및 유저정보 반환",
        examples={
            "application/json": {
                "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwOTk0MzE3LCJpYXQiOjE3MDA5OTA3MTcsImp0aSI6IjhmYzlmYTJiYjY1ZjQwOTZiNjAwMmNlNGRkMTM2ZjViIiwidXNlcl9pZCI6MX0.MSba1A62OUdY3l8wvsNuIyQFxTobBMO1TfZDQ67dB70",
                "user": {
                    "id": 4,
                    "username": "테스트",
                    "weight": {"id": 1, "name": "미니멈", "min_weight": 46},
                    "age": "20",
                    "gender": "F",
                    "years": 4,
                    "last_login": "2024-02-12T13:24:47.579491",
                    "gym": {
                        "id": 1,
                        "name": "알로하복싱짐",
                        "address": "서울 강남구 논현동 90-6",
                        "latitude": 37.51558108296889,
                        "longitude": 127.0350141685017,
                        "sport": 1,
                    },
                    "current_location": "대구 동구 신암동 1881",
                },
            }
        },
    ),
    "401": openapi.Response(description="unauthorized"),
}

random_nickname_res_schema = {
    "200": openapi.Response(
        description="랜덤 닉네임 발급",
        examples={
            "application/json": {
                "nickname": "고기먹는판다",
            }
        },
    ),
}
