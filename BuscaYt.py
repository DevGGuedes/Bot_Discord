import seleniumwire.webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
import lxml.html as lhtml
import requests
import selenium_util
#importlib.reload(selenium_util)
from selenium_util import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


async def BuscaMusicaPorLink(url):
        '''options = wd.ChromeOptions()
        options.add_experimental_option("prefs", {
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing_for_trusted_sources_enabled": False,
                "safebrowsing.enabled": False,
                "profile.default_content_setting_values.notifications": 2
        })
        options.add_argument("--disable-notifications")'''
        #options.add_argument("--headless")

        #headless = True
        #if headless:
        #    options.add_argument("--headless")
        options = Options()
        options.add_argument('--headless')
        options.add_argument("--disable-notifications")
        options.add_argument('--disable-gpu')  # Last I checked this was necessary.

        driver = seleniumwire.webdriver.Chrome(executable_path=r'chromedriver.exe', chrome_options=options)

        #driver.get('https://www.youtube.com/watch?v=oBXs2z2HUd0')
        driver.get(url)

        body = driver.find_element_by_tag_name('html').get_attribute('outerHTML')
        body = lhtml.fromstring(body)

        nomeMusica = body.xpath('//*[@id="container"]/h1/yt-formatted-string/text()')
        nomeMusica = nomeMusica[0]
        #print(f'Musica Consultada - {nomeMusica}')
        driver.close()

        '''driver = seleniumwire.webdriver.Chrome(chrome_options=options,
                                        seleniumwire_options={
                                                'backend': 'mitmproxy'
                                                })'''

        #if headless:
        #    driver.set_window_size(1920, 1080)
        #else:
        #    driver.maximize_window()
        return nomeMusica

async def BuscaPorMusica(nome):

        options = Options()
        options.add_argument('--headless')
        options.add_argument("--disable-notifications")
        options.add_argument('--disable-logging')
        options.add_argument('--disable-gpu')  # Last I checked this was necessary.
        linkYt = 'https://www.youtube.com'

        driver = seleniumwire.webdriver.Chrome(executable_path=r'chromedriver.exe', chrome_options=options)

        driver.get(linkYt)

        body = driver.find_element_by_tag_name('html').get_attribute('outerHTML')
        body = lhtml.fromstring(body)

        txtBusca = aguardar_query(Query(driver).by_id('search'))
        #txtBusca.clear()
        #txtBusca.send_keys("mc hariel torcicolo")
        txtBusca.send_keys(nome)

        #click btn search-icon-legacy
        aguardar_query(Query(driver).by_id('search-icon-legacy')).click()

        body = driver.find_element_by_tag_name('html').get_attribute('outerHTML')
        body = lhtml.fromstring(body)

        linkMusica = body.xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/ytd-thumbnail/a/@href')

        nomeMusica = body.xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/div/div[1]/div/h3/a/yt-formatted-string/text()')

        nomeMusica = nomeMusica[0]
        #print(f'Nome da Musica Consultada - {nomeMusica}')

        linkMusica = linkMusica[0]
        linkYt += linkMusica
        #print(f'Link da Musica Consultada - {linkYt}')

        driver.close()
        return nomeMusica, linkYt

#primeiro link
#

#nomeMusica, linkYt = BuscaPorMusica("mc davi bye bye")

#pega o primeiro link

#text = "mc hariel torcicolo"
#text = "https://www.youtube.com/watch?v=oBXs2z2HUd0"

# se igual a 0 pq achou a frase, s -1 nao achou
#result = text.find('http')
#print(result)

#if text.find('http') < 0:
#        print('sem link. Nome musica BuscaPorMusica')
#else:
        #print('com link BuscaMusicaPorLink')