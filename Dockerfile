FROM python:3-onbuild



WORKDIR /usr/src/app
COPY requirements.txt ./
CMD ["ECHO","INSTALLING REQS"]
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "manage.py", "runserver", "127.0.0.1:8000"]

EXPOSE 8000
