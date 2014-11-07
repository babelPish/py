### 작성자 ###
- 최광훈

### 비고 ###
* python 3.4(only)
* 비동기처리를 위해 ayncio, aiohttp 사용
* html 파싱을 위해 BeautifulSoup 사용

### Process ###
1. https://www.flickr.com/photos/tags/flicker/ 의 html 정보 습득
2. 링크의 컨텐츠에서 각 페이지의 url을 검색
3. 검색한 각 페이지의 링크로부터 이미지 링크 추출
4. 추출한 이미지 링크를 이미지 파일명으로 저장