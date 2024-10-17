FROM python:bookworm
WORKDIR /usr/src/app
RUN pip install discord && pip install audioop-lts
COPY . .
CMD ["python3", "./src/main.py"]