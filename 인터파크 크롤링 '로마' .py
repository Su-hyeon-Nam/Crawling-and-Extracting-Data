from selenium import webdriver as wd

from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
#명시적 대기를 위해
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymysql as my #디비 입력 > pip install pymysql
import time
# 사전에 필요한 정보를 로드
from Tour import TourInfo  #Tour로 Tourinfo가져와서 객채들을 tour_list에 담아

main_url = "http://tour.interpark.com/"
tour_list = []  #상품 정보를 담는 리스트 TourInfo
#드라이버 로드
driver = wd.Chrome(executable_path="/Users/user/Desktop/PYTHON/chromedriver_win32/chromedriver")
#차후 - 옵션 부여하여 (프록시, 에이전트 조작, 이미지 배제)
#임시파일들 쌓이므로 자주 삭제
#사이트 접속 (get)
driver.get(main_url)
#검색창 찾아서 검색어 입력 id : SearchGNBText
#수정할 경우 뒤에 내용이 붙어버림. .clear() -> send_keys('내용')
driver.find_element_by_xpath('//*[@id="SearchGNBText"]').send_keys('로마')

driver.find_element_by_css_selector('button.search-btn').click()
#잠시 대기
#명시적대기 : 특정 요소 로케이트 대기
try:
    element = WebDriverWait(driver, 10).until(
        #지정한 한개 요소가 올라오면 웨이트 종료
        EC.presence_of_element_located( (By.CLASS_NAME, 'oTravelBox') )
        )
except Exception as e:
    print( '오류 발생', e)
#암묵적대기 : DOM이 다 로드 될때까지 대기 하고 먼저 로드되면 바로 진행
driver.implicitly_wait( 10)
#절대적대기 : time.sleep(10) -> 클라우드 페어(디도스 방어 솔루션)
#더보기 눌러서 게시판 진입
driver.find_element_by_xpath('/html/body/div[3]/div/div/div[6]/div[4]/ul/li[6]/button').click()

#게시판에서 데이터를 가져올때 데이터 많으면 세션관리
#특정 단위별로 로그아웃 로그인 계속 시도
#팝업처리 검토
#게시판 스캔시 > 임계점을 모름
#복사한 스캔 메타정보 획득 / loop 돌려서 일괄적으로 방문 접근

# searchModule.SetCategoryList(1, '') 스크립트 실행

for page in range(1, 2):
    try: #자바스크립트 구동
        driver.execute_script("searchModule.SetCategoryList(%s, '')" % page) #n페이지 = %
        time.sleep(2)
        print("%s 페이지 이동" % page)

        boxItems = driver.find_elements_by_css_selector('.oTravelBox>.boxList>li')

        for li in boxItems:
            print( '썸네임', li.find_element_by_css_selector('img').get_attribute('src') )
            print( '링크', li.find_element_by_css_selector('a').get_attribute('onclick') )
            print( '상품명', li.find_element_by_css_selector('h5.proTit').text )
            print( '코멘트', li.find_element_by_css_selector('.proSub').text )
            print( '가격', li.find_element_by_css_selector('.proPrice').text )
            for info in li.find_elements_by_css_selector('.info-row .proInfo'):
                print( info.text )
            print('='*100)
            # 데이터 모음
            # li.find_elements_by_css_selector('.info-row .proInfo')[1].text
            # 데이터가 부족하거나 없을수도 있어서 직접 인덱스 표현은 위험성 있
            obj = TourInfo(
                li.find_element_by_css_selector('h5.proTit').text,
                li.find_element_by_css_selector('.proPrice').text,
                li.find_elements_by_css_selector('.info-row .proInfo')[1].text,
                li.find_element_by_css_selector('a').get_attribute('onclick'),
                li.find_element_by_css_selector('img').get_attribute('src')
            )
            tour_list.append( obj )


    except Execption as e1:
        print( '오류', e1 )

print( tour_list, len(tour_list) )

#수집한 정보 개수를 루프 > 페이지 방문 > 컨텐츠 획득
for tour in tour_list:
    # tour > TourIfo 임
    print( type(tour) ) # 타입확인
    # 링크 데이터에서 실데이터 획득 / 클릭하면 새창뜸, 그 창 들어가서 데이터획득
    arr = tour.link.split(',')
    
    if arr:
        # 대체
        link = arr[0].replace('searchModule.OnClickDetail(','')
        # 슬라이싱 > 앞에 ', 뒤에 ' 제거
        detail_url = link[1:-1]
        #상세 페이지 이동 : URL 값이 완성된 형태인지 확인 (http~)
        driver.get( detail_url )
        time.sleep(2)
        #bs4 설치 / 현재 패이지를 beautifulsoup 의 DOM으로 구성
        soup = bs( driver.page_source, 'html.parser') #현재 패이지를 뷰티플숩 으로 올림
        #현재 상세 정보 페이지에서 스케줄 정보 획득
        soup.select('.tip-cover')
        #디비 입력 > pip install pymysql / maria DB 설치
        
import pandas as pd

df = pd.DataFrame([[p.title, p.price, p.area, p.link, p.img, p] for p in tour_list],columns=list('ABCDEF'))

df.to_csv("/Users/user/Desktop/여행정보 도식화.csv", header=False, index =False
