```
sudo docker build -t staskjs/unesco_telegram_rss .
sudo docker run -e "TOKEN=" -e "CHATID=" -e "FEEDURL=" --name unesco_telegram_rss -v "/opt/unesco_telegram_rss/db:/app/db" -d unesco_telegram_rss
```
