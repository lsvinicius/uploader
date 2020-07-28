FROM python:3.8.5-alpine AS base
RUN adduser --disabled-password uploader_app &&\
    apk add --no-cache sudo libmagic &&\
    sudo -u uploader_app mkdir -m744 /home/uploader_app/.uploader
WORKDIR /uploader
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .


FROM base AS stg
USER uploader_app
ENV ENVIRONMENT 'stg'
ENTRYPOINT ["python"]
CMD ["server.py"]

FROM base AS prod
RUN pip install gunicorn
USER uploader_app
ENV ENVIRONMENT 'prod'
ENV APP_PORT 8000
EXPOSE ${APP_PORT}
CMD gunicorn -b 0.0.0.0:${APP_PORT} server:app