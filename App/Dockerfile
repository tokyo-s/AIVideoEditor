FROM python:3.10
#
WORKDIR /app

#
COPY ./requirements.txt ./requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

#
COPY . .

EXPOSE 8000
#
CMD [ "python3", "app.py"]