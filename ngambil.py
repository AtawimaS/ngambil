from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
import pandas as pd
import datetime

class Chrome:

    class threads:
        user_css = (
            ".x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x193iq5w.xeuugli.x1fj9vlw."
            "x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty."
            "x1943h6x.x1i0vuye.xjohtrz.x1s688f.xp07o12.x1yc453h"
        )

        pesan_css = (
            ".x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x193iq5w.xeuugli.x1fj9vlw."
            "x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty."
            "x1943h6x.x1i0vuye.xjohtrz.xo1l8bm.xp07o12.x1yc453h."
            "xat24cr.xdj266r"
        )


        date_css = (
            "time.x1rg5ohu.xnei2rj.x2b8uid.xuxw1ft"
        )
        
        def __init__(self, find):
            self.find = find
            self.link  = f"https://www.threads.net/search?q=%23{find}&serp_type=default"
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            self.driver = webdriver.Chrome(options=options)
            self.driver = webdriver.Chrome()
            self.driver.get(self.link)

        def all(self):
            try:
                username = self.driver.find_element(By.CSS_SELECTOR, self.user_css).text
                pesannya = self.driver.find_element(By.CSS_SELECTOR, self.pesan_css).text
                time_element = self.driver.find_element(By.CSS_SELECTOR, self.date_css)
                datetime_value = time_element.get_attribute("datetime")
                dt = datetime.datetime.strptime(datetime_value, "%Y-%m-%dT%H:%M:%S.%fZ")

                return {
                    'username': username,
                    'message': pesannya,
                    'datetime': dt
                }
            except Exception as e:
                print(f"An error occurred: {e}")
                return None

        def loop(self, dataframe=False, n=1):
            user_value = []
            pesan_value = []
            date_value = []
            try:
                for i in range(n):
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '.xrvj5dj.xd0jker.x1wxlsmb'))
                    )
                    articles = self.driver.find_elements(By.CSS_SELECTOR, '.xrvj5dj.xd0jker.x1wxlsmb')
                    for article in articles:
                        try:
                            username = article.find_element(By.CSS_SELECTOR, self.user_css).text
                            message = article.find_element(By.CSS_SELECTOR, self.pesan_css).text
                            time_element = article.find_element(By.CSS_SELECTOR, self.date_css)
                            datetime_value = time_element.get_attribute("datetime")
                            dt = datetime.datetime.strptime(datetime_value, "%Y-%m-%dT%H:%M:%S.%fZ")
                            user_value.append(username)
                            pesan_value.append(message)
                            date_value.append(dt)
                        except Exception as e:
                            print(f"Error processing article: {e}")
                data = {
                    'username': user_value,
                    'message': pesan_value,
                    'datetime': date_value
                }
                if dataframe:
                    return pd.DataFrame(data)
                else:
                    return data
            except Exception as e:
                print(f"Error looping: {e}")

        def login(self, username, password):
            try:
                login_button = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".x6ikm8r.x10wlt62.xlyipyv"))
                )
                login_button.click()
            except Exception as e:
                print(f"Error clicking login button: {e}")

            try:
                userid = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,
                                                    ".x1i10hfl.x9f619.xggy1nq.x1s07b3s.x1kdt53j.x1a2a7pz.x90nhty.x1v8p93f.xogb00i.x16stqrj.x1ftr3km.xyi19xy.x1ccrb07.xtf3nb5.x1pc53ja.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x178xt8z.xm81vs4.xso031l.xy80clv.xp07o12.xjohtrz.x1a6qonq.xyamay9.x1pi30zi.x1l90r2v.x1swvt13.x1yc453h.xh8yej3.x1e899rk.x1sbm3cl.x1rpcs5s.x1c5lum3.xd5rq6m"))
                )
                userid.send_keys(username)
            except Exception as e:
                print(f"Error finding username field: {e}")

            try:
                passid = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Password"]'))
                )
                passid.send_keys(password)
                passid.send_keys(Keys.ENTER)
            except Exception as e:
                print(f"Error finding password field: {e}")

            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".xl1xv1r.x14yjl9h.xudhj91.x18nykt9.xww2gxu.xvapks4.x1bgq0ue"))
            )
            self.driver.get(self.link)

        def get_value(self, *args):
            all_values = self.all()
            if all_values:
                result = {arg: all_values[arg] for arg in args if arg in all_values}
                return result
            else:
                return None
            
        def info(self):
            return {
                'Available Attributes': ['username', 'message', 'datetime']
            }
    class twitter:
        user_xpath = (
            './/div[@data-testid="User-Name"]'
        )

        pesan_xpath = (
            './/div[@data-testid="tweetText"]'
        )


        date_xpath = (
            './/time'
        )

        
        def __init__(self, find):
            self.find = find
            link  = f"https://x.com/search?q=%23{find}&src=typed_query&f=live"
            self.link = link
            # options = Options()
            # options.add_argument('--headless')
            # options.add_argument('--disable-gpu')
            # self.driver = webdriver.Chrome(options=options)
            self.driver = webdriver.Chrome()
            self.driver.get('https://x.com/i/flow/login')

        def all(self):
            try:
                wait = WebDriverWait(self.driver, 10)
                
                username = wait.until(
                    EC.presence_of_element_located((By.XPATH, self.user_xpath))
                ).text
                
                pesannya = wait.until(
                    EC.presence_of_element_located((By.XPATH, self.pesan_xpath))
                ).text
                
                time_element = wait.until(
                    EC.presence_of_element_located((By.XPATH, self.date_xpath))
                ).get_attribute('datetime')
                
                dt = datetime.datetime.strptime(time_element, "%Y-%m-%dT%H:%M:%S.%fZ")
                
                print(dt)
                return {
                    'username': username,
                    'message': pesannya,
                    'datetime': dt
                }
            except Exception as e:
                print(f"An error occurred: {e}")
                return None

        def loop(self, dataframe=False, n=1):
            user_value = []
            pesan_value = []
            date_value = []
            n= n*2
            try:
                for i in tqdm(range(n), desc="Scraping page"):
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    scroll_height = self.driver.execute_script("return document.body.scrollHeight")
                    self.driver.execute_script(f"window.scrollTo(0, {scroll_height / 2});")
                    WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, './/article[@data-testid="tweet"]'))
                    )
                    articles = self.driver.find_elements(By.XPATH, './/article[@data-testid="tweet"]')
                    print(articles)
                    for article in articles:
                        try:
                            data_all = all()

                            user_value.append(data_all['username'])
                            pesan_value.append(data_all['message'])
                            date_value.append(data_all['datetime'])
                        except Exception as e:
                            print(f"Error processing article: {e}")
                data = {
                    'username': user_value,
                    'message': pesan_value,
                    'datetime': date_value
                }
                if dataframe:
                    return pd.DataFrame(data)
                else:
                    return data
            except Exception as e:
                print(f"Error looping: {e}")

        def login(self, username, password):
            try:
                userid = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,
                                                    ".r-30o5oe.r-1dz5y72.r-13qz1uu.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-fdjqy7"))
                )
                userid.send_keys(username)
            except Exception as e:
                print(f"Error finding username field: {e}")

            try:
                next_button = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".css-175oi2r.r-sdzlij.r-1phboty.r-rs99b7.r-lrvibr.r-ywje51.r-184id4b.r-13qz1uu.r-2yi16.r-1qi8awa.r-3pj75a.r-1loqt21.r-o7ynqc.r-6416eg.r-1ny4l3l"))
                )
                next_button.click()
            except Exception as e:
                print(f"Error of next button : {e}")

            try:
                passid = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.r-30o5oe.r-1dz5y72.r-13qz1uu.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-fdjqy7'))
                )
                passid.send_keys(password)
                passid.send_keys(Keys.ENTER)
            except Exception as e:
                alert = WebDriverWait(self.driver,5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.css-175oi2r.r-1awozwy.r-l5o3uw.r-18u37iz.r-1wtj0ep.r-xyw6el.r-105ug2t.r-yz1j6i'))
                )
                print(f"Error finding password field: {e}\n{alert}")

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".css-175oi2r.r-15zivkp.r-1bymd8e.r-13qz1uu.r-1awozwy"))
                
            )
            self.driver.get(self.link)

        def get_value(self, *args):
            all_values = self.all()
            if all_values:
                result = {arg: all_values[arg] for arg in args if arg in all_values}
                return result
            else:
                return None
            
        def info(self):
            return {
                'Available Attributes': ['username', 'message', 'datetime']
            }
    class kompas:
        print("still development")
    class bola_net:
        print("still development")
#testing
scraper = Chrome.twitter('btc-usd')
scraper.login('*','*')
ini = scraper.all()