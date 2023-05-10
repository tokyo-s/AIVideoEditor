FROM python:3.8

WORKDIR /
# ENV FLASK_APP=app.py
# ENV FLASK_RUN_HOST=0.0.0.0

COPY ./requirements.txt ./requirements.txt
COPY ./scripts ./scripts

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
EXPOSE 8002

COPY . .
CMD [ "python", "./app.py"]