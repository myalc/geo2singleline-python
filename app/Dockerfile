FROM python:latest
COPY . /usr/src/myapp
WORKDIR /usr/src/myapp
RUN pip install -r requirements.txt
CMD ["python", "-u", "__init__.py"]
