from drf_yasg import openapi

login_res_schema = {
    "200": openapi.Response(
        description="로그인 성공",
        examples={
            "application/json": {
                "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwOTk0MzE3LCJpYXQiOjE3MDA5OTA3MTcsImp0aSI6IjhmYzlmYTJiYjY1ZjQwOTZiNjAwMmNlNGRkMTM2ZjViIiwidXNlcl9pZCI6MX0.MSba1A62OUdY3l8wvsNuIyQFxTobBMO1TfZDQ67dB70",
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

access_res_schema = {
    "200": openapi.Response(
        description="액세스토큰 재발급 및 유저닉네임 반환",
        examples={
            "application/json": {
                "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwOTk0MzE3LCJpYXQiOjE3MDA5OTA3MTcsImp0aSI6IjhmYzlmYTJiYjY1ZjQwOTZiNjAwMmNlNGRkMTM2ZjViIiwidXNlcl9pZCI6MX0.MSba1A62OUdY3l8wvsNuIyQFxTobBMO1TfZDQ67dB70",
                "username": "고기먹는판다",
            }
        },
    ),
    "401": openapi.Response(description="권한없음(refresh token 없음)"),
}

random_nickname_res_schema = {
    "200": openapi.Response(
        description="랜덤 닉네임 발급",
        examples={
            "application/json": {
                "nickname": "더운학자",
            }
        },
    ),
}
