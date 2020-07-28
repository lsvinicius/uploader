FROM python:3.8.5 AS base
WORKDIR /uploader
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN useradd --create-home uploader_app
RUN mkdir -m644 /home/uploader_app/.uploader &&\
    chown uploader_app:uploader_app /home/uploader_app/.uploader

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