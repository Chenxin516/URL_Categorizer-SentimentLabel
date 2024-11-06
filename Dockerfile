FROM python:3.12.0-bookworm

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN playwright install
RUN playwright install-deps
COPY . .
CMD ["python3"]
