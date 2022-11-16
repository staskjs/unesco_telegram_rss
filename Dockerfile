FROM python:3.10
RUN pip install bs4 feedparser
RUN pip install python-telegram-bot --pre
WORKDIR /app
RUN mkdir /app/db
COPY . .
VOLUME /app/db
CMD python3 -u rss.py
