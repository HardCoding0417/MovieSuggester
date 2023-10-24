from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from time import sleep
import os


# 중복방지 보조
def load_titles_from_csv(filename):
    try:
        if os.path.getsize(filename) == 0:
            return set()
        df = pd.read_csv(filename)
        return set(df['Title'])
    except FileNotFoundError:
        return set()
def save_titles_to_csv(titles, filename):
    df = pd.DataFrame(list(titles), columns=["Title"])
    df.to_csv(filename, index=False)


# 몇 년도 몇 월까지 긁을 지 범위를 지정하면, 거기에 해당하는 url들을 리턴해주는 함수
def scrape_range(years, months):
    # years = range(2017, 2019)     # months = range(1, 13)
    month_pages = []
    for year in years:
        for month in months:
            year_str  = str(year)
            month_str = str(month).zfill(2)
            start_page = ('https://movie.daum.net/ranking/boxoffice/monthly?date={}'
                          .format(year_str + month_str))
            month_pages.append(start_page)
    print(f"{years[0]}년 {str(months[0]).zfill(2)}월부터 {years[-1]}년 {str(months[-1]).zfill(2)}월까지 스크래핑 하겠습니다.")
    return month_pages


# 리뷰 긁는 함수
def contents_pages(month_page):
    global crawled_titles  # 전역 변수 사용

    reviews = []
    title = []
    for i in range(1,31):
        try:
            driver.get(month_page)
            sleep(1)
            driver.find_element(by='xpath', value=f'/html/body/div[2]/main/article/div/div[2]/ol/li[{i}]/div/div[2]/strong/a').click()
            sleep(1)
            title = driver.find_element(by='xpath', value=f'/html/body/div[2]/main/article/div/div[1]/div[2]/div[1]/h3/span[1]').text
            # 이미 수집한 타이틀이면 스킵
            if title in crawled_titles:
                print(f"이미 수집한 타이틀입니다: {title}")
                driver.back()
                continue
            driver.find_element(by='xpath', value=f'/html/body/div[2]/main/article/div/div[2]/div[1]/ul/li[4]/a/span').click()
            sleep(1)
            driver.find_element(by='xpath', value='/html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/div[1]/button').click()
            sleep(1)
            for k in range(1, 40):
                try:
                    review = driver.find_element('xpath', f'/html/body/div[2]/main/article/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/ul[2]/li[{k}]/div/p').text
                    reviews.append(review)
                except:
                    pass
            data_save(title, reviews)
            # 중복방지
            crawled_titles.add(title)

        except:
            print(title,"은 평점이 10개 미만입니다.")
        save_titles_to_csv(crawled_titles, 'crawled_titles.csv')
    return title, reviews

def data_save(title, reviews):
    df = pd.DataFrame({
        'Title': [title] * len(reviews),
        'Reviews': reviews
    })
    df.to_csv('2017-2018.csv', mode='a', index=False)
    df.info()
    return df

if __name__ == '__main__':
    user_agent = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60"}
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    crawled_titles = load_titles_from_csv('crawled_titles.csv')
    urls = scrape_range(range(2017, 2019), range(1, 13)) # 범위 안의 url들을 반환
    for url in urls:
        my_title, my_reviews = contents_pages(url)



# 타이틀과 리뷰가 동시에 append 되어야 짝이 잘 맞게 들어간다
# 나는 매번 새로 저장해서 짝이 안 맞는 문제가 없지만, 너무 이렇게 저장하는 것도 좋지 않다...
# 매 영화마다 파일을 만들도록 했으면 문제를 파악하기가 더 쉬웠을 것 같다.
# 제목을 통해서 어떤 영화가 스킵됐는지 파악할 수 있었을 테니까









