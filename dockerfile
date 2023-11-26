FROM python:3.9

# 기본 운영체제 시간을 Asia/Seoul로 설정하기 위한 코드
RUN apt-get update -y
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul
RUN apt-get install -y tzdata

# RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# RUN pip install -U 'Twisted[tls,http2]'

COPY ./ /app
WORKDIR /app

# CMD daphne -b 0.0.0.0 -p 5317 config.asgi:application
CMD python manage.py runserver 0.0.0.0:5317

EXPOSE 53171


# #wsgi.py
# from app import app

# if __name__ == '__main__':
#     app.run()