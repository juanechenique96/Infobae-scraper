import requests
import lxml.html as html
import os
import datetime
import time

HOME_URL = 'https://www.infobae.com'
XPATH_LINK_TO_ARTICLE = '//a[@data-pb-field="headlines.basic"]/@href'
XPATH_TITLE = '//div[@class="row"]/header/h1/text()'
XPATH_SUMMARY = '//div[@class="row"]/header/span[@class="subheadline"]/text()'
XPATH_BODY = '//div[@id="article-content"]/div[@class="row pb-content-type-text"]//text()'


def parse_notice(link, today):
    '''Funcion que guarda los titulos, subtitulos y cuerpos de una noticia en un archivo'''
    try:
        response = requests.get(HOME_URL + link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"', '')
                title = title.replace('?', '')
                title = title.replace('¿', '')
                title = title.replace('!', '')
                title = title.replace('¡', '')
                title = title.replace(':', '')
                title = title.replace('"', '')
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
                for p in body :
                    p = p.strip(' \n')
            except IndexError:
                return
            
            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    if not p.isspace():
                        f.write(p)
                        if p.endswith('.') or p.endswith(':'):
                            f.write('\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)
    except requests.exceptions.ConnectionError:
        time.sleep(0.1)



def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            '''Traemos el documento html de la pagina como tipo string'''
            home = response.content.decode('utf-8')
            '''Convertimos el documento string a un documento tipo html al cual poder realizarle xpath'''
            parsed = html.fromstring(home)
            '''Creo una lista de links hacia las noticias'''
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            '''Creamos una carpeta donde guardar las noticias de la fecha'''
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)
            for link in links_to_notices:
                parse_notice(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == "__main__":
    run()
