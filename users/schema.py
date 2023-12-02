from drf_yasg import openapi

login_res_schema = {
    "200": openapi.Response(
        description="로그인 성공",
        examples={
            "application/json": {
                "tokens": {
                    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwMTA3NzExNywiaWF0IjoxNzAwOTkwNzE3LCJqdGkiOiI2YmQ3MTg1ODQ0YTU0YmFhYjc4ZWI1MmVlNDYyNjk3MiIsInVzZXJfaWQiOjF9.EsDomw9EImTUaJtxAZmiSehflagY62OR7m_vvZev0OY",
                    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAwOTk0MzE3LCJpYXQiOjE3MDA5OTA3MTcsImp0aSI6IjhmYzlmYTJiYjY1ZjQwOTZiNjAwMmNlNGRkMTM2ZjViIiwidXNlcl9pZCI6MX0.MSba1A62OUdY3l8wvsNuIyQFxTobBMO1TfZDQ67dB70",
                },
                "user": {"username": "admin"},
            }
        },
    ),
    "401": openapi.Response(
        description="회원가입 필요", examples={"application/json": {"detail": "need to register", "kakao_nickname": "파이터"}}
    ),
    "404": openapi.Response(
        description="유효하지 않은 카카오 리다이렉트 코드", examples={"application/json": {"detail": "Not found."}}
    ),
    "403": openapi.Response(description="차단된 유저", examples={"application/json": {"detail": "blocked user"}}),
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
