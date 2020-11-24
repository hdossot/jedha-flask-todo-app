FROM python:3.8-slim

ENV PORT 5000

RUN mkdir /app
WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["bash", "start.sh"]