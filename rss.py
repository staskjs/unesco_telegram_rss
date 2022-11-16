import feedparser
import asyncio
import telegram
import time
import os
from bs4 import BeautifulSoup as Soup

token = os.environ['TOKEN']
chat_id = os.environ['CHATID']
feed_url = os.environ['FEEDURL']

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
            feed = feedparser.parse(feed_url)
            id = feed.entries[i].id
            print('latest id is {id}'.format(id=id))
            if id in ids:
                print('{id} exists'.format(id=id))
                time.sleep(10)
                continue

            # Вытаскиваем картинку
            soup = Soup(feed.entries[i].summary, features="html.parser")
            # Вытаскиваем контент
            photo_url = soup.a.img['src']
            soup2 = Soup(feed.entries[i].summary_detail.value, features="html.parser")
            strs = []
            for string in soup.strings:
                strs.append(str(string))
            content = ' '.join(strs)

            # Подготавливаем описание
            caption = '<b>' + feed.entries[i].title + '</b>\n\n' + content
            link = feed.entries[i].link
            link = '\n<a href="' + link + '">ru.unesco.kz</a>'
            # Ссылка должна влезать всегда, независимо от лимита
            maxlen = 1021 - len(link)
            # Лимит на количество символов, ограничиваем и добавляем троеточие если превышен
            caption = (caption[:maxlen] + '...') if len(caption) > maxlen else caption
            caption += link

            await bot.send_photo(chat_id, photo_url, caption, parse_mode='HTML')

            print('handled id {id}'.format(id=id))

            ids_file = open('db/ids.txt', 'a')
            ids_file.write('\n' + id)
            ids_file.close()

            time.sleep(10)

if __name__ == '__main__':
    asyncio.run(main())
