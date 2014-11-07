__author__ = 'jay'

import logging
import asyncio # 작업을 비동기로 처리하기 위한 패키지
import aiohttp # asyncio와함께 network io 작업을 비동기로 처리하기 위한 패키지
import requests
from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup

# 디버그 정보를 표
logging.basicConfig(level=logging.DEBUG)


flickr_url = "https://www.flickr.com/photos/tags/flicker/"

def extract_links_from_page(page):
    # BeautifulSoup 객체로부터 Flickr 페이지 리스트의 제너레이터를 반환
    page_urls = [urljoin(flickr_url, link['href']) for link in
                 (list_body.find('a', href=True) for list_body in page.find_all(class_="StreamList"))]
    return page_urls

@asyncio.coroutine # asyncio를 통해서 실행하는 펑션은 모두 coroutine 데코레이터가 필요함
def body_from_url(url):
    # URL의 컨텐츠를 반환
    response = yield from aiohttp.request('GET', url)
    return (yield from response.read_and_close())

@asyncio.coroutine
def extract_img_link_from_page(page):
    # BeautifulSoup 객체로 부터 flickr 이미지 url을 검색
    img_url = page.find('img', attrs={"aria-describedby":"title_div"})
    return img_url['src']

@asyncio.coroutine
def search_img_per_link(link):
    body = yield from body_from_url(link)   # 1. 링크의 컨텐츠를 습득
    bs = BeautifulSoup(body)                # 2. 컨텐츠를 BeautifulSoup객체로 만들어 파싱
    img_src = yield from extract_img_link_from_page(bs) # 3. 이미지 링크를 검색
    img_url = urljoin(link, img_src)

    img_name = urlsplit(img_url).path.split('/')[-1]    # 4. 이미지의 파일명을 반환
    with open(img_name, 'wb') as img_file:              # 5. 이미지를 받아오는 동시에 파일로 저장
        img = yield from body_from_url(img_url)
        img_file.write(img)
    print(img_name + ' writed')

main_body = requests.get(flickr_url).content    # 해당 flickr 링크의 컨텐츠를 습득
main_bs = BeautifulSoup(main_body)              # BeautifulSoup 객체 생성
page_urls = extract_links_from_page(main_bs)    # 페이지 링크 리스트의 제너레이터 생성

loop = asyncio.get_event_loop()                 # ayncio 이벤트 루프 습득
loop.run_until_complete(asyncio.wait([search_img_per_link(link) for link in page_urls])) # 이미지 다운로드 비동기 요청
