# Crawling-and-Extracting-Data
Extracting Data through Crawling in interpark
interpark tour 대상으로 keyword '로마' 를 이용하여 검색하고 패키지상품 창으로 들어간다.
 selenium으로 keyword를 검색 및 구동하고 원하는 데이터를 추출했다. 
추출한 데이터는 각 상품의 [썸네일, 링크, 상품명, 코멘트, 가격]이며 146개의 패키지상품 모두를 대상으로 한다.
이렇게 얻은 데이터를 pandas를 이용하여 csv형태로 정렬 및 병합한다.
Maria DB를 시도하였지만 SQL서버를 설정하는것이 용이하지 않다.
