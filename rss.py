import feedparser
import asyncio
import telegram
import time
import os
from bs4 import BeautifulSoup as Soup

token = os.environ['TOKEN']
chat_id = os.environ['CHATID']
feed_url = os.environ['FEEDURL']

feed = feedparser.parse(feed_url)

async def main():
    bot = telegram.Bot(token)
    async with bot:
        while True:
            try:
                ids_file = open('db/ids.txt', 'r')
            except:
                ids_file = open('db/ids.txt', 'a')
                ids_file.close()
                ids_file = open('db/ids.txt', 'r')
            ids = ids_file.read().split('\n')
            i = 0
            id = feed.entries[i].id
            if id in ids:
                continue

            soup = Soup(feed.entries[i].summary, features="html.parser")
            photo_url = soup.a.img['src']
            soup2 = Soup(feed.entries[i].summary_detail.value, features="html.parser")
            strs = []
            for string in soup.strings:
                strs.append(str(string))
            content = ' '.join(strs)
            caption = feed.entries[i].title + '\n' + content
            caption = (caption[:1021] + '...') if len(caption) > 1021 else caption

            await bot.send_photo(chat_id, photo_url, caption)

            ids_file = open('db/ids.txt', 'a')
            ids_file.write('\n' + id)
            ids_file.close()

            time.sleep(10)

if __name__ == '__main__':
    asyncio.run(main())