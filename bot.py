import csv, re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from time import sleep

class Bot():
    def __init__(self):

        #Configurando Opções do Chrome
        options = Options()

        #Rotate UA
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
        user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)

        options.add_argument(f'user-agent={user_agent_rotator.get_random_user_agent()}')

        #Rotate Proxy
        #proxy = ''
        #options.add_argument(f'--proxy-server={proxy}')

        #Automated Browser setting off:
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        #Headless Browser:
        #options.headless = True
        #options.add_argument("--no-sandbox")
        #options.add_argument("--window-size=1920x1080")
        #options.add_argument("--disable-gpu")
        #options.add_argument('--ignore-certificate-errors')
        #options.add_argument('--allow-running-insecure-content')
        #options.add_argument("--disable-extensions")
        #options.add_argument("--start-maximized")
        #options.add_argument('--disable-dev-shm-usage')
        #options.add_argument('--remote-debuggin-port=9222')

        self.driver = webdriver.Chrome(executable_path=r'./chromedriver.exe', options=options)

        self.profileUrl = []
        self.profileName = []
        self.fullName = []
        self.postsCount =[]
        self.followersCount = []
        self.followingCount = []
        self.Bio = []
        self.Website = []
        self.button_post = None
        self.botao_more = None
        self.botao_next = None
        
    def open_driver(self):
        self.importar_cookies()

        self.driver.get('https://www.instagram.com/')
        sleep(3) 
        try:
            WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Agora não")]')))
            print("Cookies carregado com sucesso!")
        except TimeoutException:
            print("Cookies não carregado. Logando...")
            self.login()
            sleep(5)
            self.exportar_cookies()
        sleep(3)

    def login(self):
        
        usuario = input("Insira o seu nome de Usuário: ")
        senha = input("Insira a sua senha: ")

        try:
            button_cookies = self.driver.find_element_by_xpath("//button[@class='aOOlW  bIiDR  ']").click()
        except:
            pass
        
        sleep(5)
        login = self.driver.find_element_by_css_selector("input[name='username']")
        password = self.driver.find_element_by_css_selector("input[name='password']")
        botao_enviar = self.driver.find_element_by_css_selector("button[type='submit']")

        login.clear()
        password.clear()

        login.send_keys(usuario)
        password.send_keys(senha)

        botao_enviar.click()
        sleep(10)

        try :
            self.driver.find_element_by_xpath("//p[@id='slfErrorAlert']")
            print("Usuário ou senha incorretos. Por favor, tente novamente.")
            self.driver.quit()
        except:
            print("login successful!")

        not_now = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Agora não")]'))).click()
        not_now1 = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Agora não")]'))).click()

    def importar_cookies(self):
        cookies = []
        with open('cookies.txt', 'r') as file:
            for row in file:
                cookies.append(row)
        
        cookies = [eval(cookie) for cookie in cookies]

        self.driver.get('https://www.instagram.com/')
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        sleep(3)
    
    def exportar_cookies(self):
        cookies = self.driver.get_cookies()

        with open('cookies.txt', 'a+') as file:
            file.truncate(0)
            for cookie in cookies:
                file.write(str(cookie) + '\n')
        
        print("Cookies armazenado com sucesso.")

    def tagged_posts(self,link,limite):
        button_tagged = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//span[@class='_08DtY']"))).click()
        button_post = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='_9AhH0']"))).click()

        sleep(3)
        self.profileUrl.append(WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,"//a[@class='sqdOP yWX7d     _8A5w5   ZIAjV ']"))).get_attribute('href'))

        verificador = 0
        contador_novo = 1
        while verificador == 0:
            try:
                button_next = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,"//a[@class=' _65Bje  coreSpriteRightPaginationArrow']"))).click()
                sleep(3)
                self.profileUrl.append(WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,"//a[@class='sqdOP yWX7d     _8A5w5   ZIAjV ']"))).get_attribute('href'))

                contador_novo += 1
                
                if contador_novo == limite: #Limit the total of users to extract.
                    verificador = 1
                
            except (NoSuchElementException, TimeoutException) :
                verificador = 1
    
    def importar(self, nome_arquivo, url):
        try :
            with open(nome_arquivo, 'r') as file:
                pass
        except :
            with open(nome_arquivo, 'a+', newline='', encoding='utf-8') as file :
                write = csv.writer(file, delimiter=';')
                header = ['profileUrl','profileName','fullName','postsCount','followersCount','followingCount','Bio','Website']
                write.writerow(header)
        
        with open(nome_arquivo, 'a+', newline='', encoding='utf-8') as file :
            write = csv.writer(file, delimiter=';')
            write.writerow([url,self.profileName[-1],self.fullName[-1],self.postsCount[-1],self.followersCount[-1],self.followingCount[-1],self.Bio[-1],self.Website[-1]])
    
    def coleta_dados(self, url):
        self.driver.get(url)
        sleep(3)
        
        try:
            self.profileName.append(WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.XPATH,"//div[@class='nZSzR']/h1"))).text)
        except TimeoutException :
            self.profileName.append(WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.XPATH,"//div[@class='nZSzR']/h2"))).text)
        
        try :
            self.fullName.append(WebDriverWait(self.driver,3).until(EC.presence_of_element_located((By.XPATH,"//div[@class='-vDIg']/h1"))).text)
        except TimeoutException :
            self.fullName.append('')

        self.Bio.append(WebDriverWait(self.driver,3).until(EC.presence_of_element_located((By.XPATH,"//div[@class='-vDIg']"))).text)
        self.Bio[-1] = self.Bio[-1].replace(self.fullName[-1],'')
        
        self.Website.append(self.Find(self.Bio[-1]))

        try:
            posts = self.driver.find_element_by_xpath("//ul[@class='k9GMp ']/li/span/span")
        except NoSuchElementException:
            posts = self.driver.find_element_by_xpath("//ul[@class='k9GMp ']/li/a/span")
        try:
            followers = self.driver.find_element_by_xpath("//ul[@class='k9GMp ']//li[2]/a/span")
        except NoSuchElementException:
            followers = self.driver.find_element_by_xpath("//ul[@class='k9GMp ']//li[2]/span/span")

        try:
            following = self.driver.find_element_by_xpath("//ul[@class='k9GMp ']//li[3]/a/span")
        except NoSuchElementException :
            following = self.driver.find_element_by_xpath("//ul[@class='k9GMp ']//li[3]/span/span")
            
        if posts.get_attribute('title') == '' :
            self.postsCount.append(posts.text.replace('.',''))
        else :
            self.postsCount.append(posts.get_attribute('title').replace('.',''))
        
        if followers.get_attribute('title') == '' :
            self.followersCount.append(followers.text.replace('.',''))
        else :
            self.followersCount.append(followers.get_attribute('title').replace('.',''))
        
        if following.get_attribute('title') == '' :
            self.followingCount.append(following.text.replace('.',''))
        else :
            self.followingCount.append(following.get_attribute('title').replace('.',''))

        for i in range(0,len(self.Bio)):
            self.Bio[i] = self.Bio[i].replace('\n',' ')

    def set_variables(self):
        self.profileUrl = []
        self.profileName = []
        self.fullName = []
        self.postsCount = []
        self.followersCount = []
        self.followingCount = []
        self.Bio = []
        self.Website = []

        return self.profileUrl,self.profileName,self.fullName,self.postsCount,self.followersCount,self.followingCount,self.Bio,self.Website
    
    def Find(self,string):
        # findall() has been used 
        # with valid conditions for urls in string
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        url = re.findall(regex,string)      
        return [x[0] for x in url]
    
    def commented_posts(self, link, limite_post, limite_user):
        self.button_post = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='_9AhH0']"))).click()
        sleep(3)
        
        posts_scrapped = 0
        
        while posts_scrapped < limite_post:
            self.scrolldown_iframe(limite_user, limite_post, link)
            posts_scrapped += 1
        
    def scrolldown_iframe(self,limite_user, limite_post, link):
        users = []
        iframe = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,"//ul[@class='XQXOT    pXf-y ']")))
        x, y = 0, 1000
        verificador = 0

        while verificador == 0:
            users = WebDriverWait(self.driver,10).until(EC.presence_of_all_elements_located((By.XPATH,"//ul[@class='Mr508 ']//a[@class='sqdOP yWX7d     _8A5w5   ZIAjV ']")))
            users = list(filter(lambda user: user.get_attribute('href') != link, users))
            print(f"{len(users)}  {[user.get_attribute('href') for user in users]}")

            if len(users) > limite_user:
                break

            self.driver.execute_script('arguments[0].scrollTo({},{})'.format(x,y), iframe)
            try:
                self.botao_more = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='                     Igw0E     IwRSH        YBx95       _4EzTm                                                                                                            NUiEW  ']/button"))).click()
            except (ElementClickInterceptedException, TimeoutException):
                self.driver.execute_script('arguments[0].scrollTo({},{})'.format(x+1000,y+1000), iframe)
                try:
                    self.botao_more = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='                     Igw0E     IwRSH        YBx95       _4EzTm                                                                                                            NUiEW  ']/button"))).click()                        
                except (ElementClickInterceptedException, TimeoutException):
                    users = WebDriverWait(self.driver,10).until(EC.presence_of_all_elements_located((By.XPATH,"//ul[@class='Mr508 ']//a[@class='sqdOP yWX7d     _8A5w5   ZIAjV ']")))
                    users = list(filter(lambda user: user.get_attribute('href') != link, users))
                    verificador = 1

        while len(users) > limite_user :
            del users[-1]
        
        for user in users:
            self.profileUrl.append(user.get_attribute('href'))

        self.button_next = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,"//a[@class=' _65Bje  coreSpriteRightPaginationArrow']"))).click()

    def hashtags_posts(self, link, limite_post):
        button_post = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,"//div[@class='_9AhH0']"))).click()
        sleep(3)
        while len(self.profileUrl) < limite_post:
            self.profileUrl.append(WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,"//a[@class='sqdOP yWX7d     _8A5w5   ZIAjV ']"))).get_attribute('href'))
            try:
                button_next = WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,"//a[@class=' _65Bje  coreSpriteRightPaginationArrow']"))).click()
                sleep(3)
            except NoSuchElementException:
                break
