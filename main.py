import os
import time
import re
import requests
import json
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from chatterbot import ChatBot
from selenium import webdriver



class WhatsAppBot():

    
    
    dir_path = os.getcwd()
    

    def __init__(self, nome_bot):
        self.nome_bot = ChatBot(nome_bot,storage_adapter='chatterbot.storage.SQLStorageAdapter')

        print(self.dir_path)
        
        self.chrome = self.dir_path+'\chromedriver.exe'

        self.options = webdriver.ChromeOptions()
        self.options.add_argument(r"user-data-dir="+self.dir_path+"\profile\wpp")
        self.driver = webdriver.Chrome(self.chrome, chrome_options=self.options)

    def inicia(self,nome_contato):

        self.driver.get('https://web.whatsapp.com/')
        self.driver.implicitly_wait(15)

        self.caixa_de_pesquisa = self.driver.find_element_by_class_name('_2_1wd')


        self.caixa_de_pesquisa.send_keys(nome_contato)
        time.sleep(2)
        print(nome_contato)
        self.contato = self.driver.find_element_by_xpath('//span[@title = "{}"]'.format(nome_contato))
        self.contato.click()
        time.sleep(2)



    def saudacao(self,frase_inicial):
        self.caixa_de_mensagem = self.driver.find_element_by_xpath("//div[@class='_2A8P4']/div[@class='_1JAUF _2x4bz focused']/div[@class='_2_1wd copyable-text selectable-text']")

        if type(frase_inicial) == list:
            for frase in frase_inicial:
                self.caixa_de_mensagem.send_keys(frase)
                time.sleep(1)
                self.botao_enviar = self.driver.find_element_by_class_name('_1E0Oz')
                self.botao_enviar.click()
                time.sleep(1)
        else:
            return False

    def escuta(self):
        post = self.driver.find_elements_by_class_name('_24wtQ')
        ultimo = len(post) - 1
        texto = post[ultimo].find_element_by_css_selector('span.selectable-text').text
        return texto

    def aprender(self,ultimo_texto,frase_inicial,frase_final,frase_erro):
        self.caixa_de_mensagem = self.driver.find_element_by_class_name('_2S1VP')
        self.caixa_de_mensagem.send_keys(frase_inicial)
        time.sleep(1)
        self.botao_enviar = self.driver.find_element_by_class_name('_35EW6')
        self.botao_enviar.click()
        self.x = True
        while self.x == True:
            texto = self.escuta()

            if texto != ultimo_texto and re.match(r'^::', texto):
                if texto.find('?') != -1:
                    ultimo_texto = texto
                    texto = texto.replace('::', '')
                    texto = texto.lower()
                    texto = texto.replace('?', '?*')
                    texto = texto.split('*')
                    novo = []
                    for elemento in texto:
                        elemento = elemento.strip()
                        novo.append(elemento)

                    self.bot.train(novo)
                    self.caixa_de_mensagem.send_keys(frase_final)
                    time.sleep(1)
                    self.botao_enviar = self.driver.find_element_by_class_name('_35EW6')
                    self.botao_enviar.click()
                    self.x = False
                    return ultimo_texto
                else:
                    self.caixa_de_mensagem.send_keys(frase_erro)
                    time.sleep(1)
                    self.botao_enviar = self.driver.find_element_by_class_name('_35EW6')
                    self.botao_enviar.click()
                    self.x = False
                    return ultimo_texto
            else:
                ultimo_texto = texto

    def noticias(self):

        req = requests.get('https://newsapi.org/v2/top-headlines?sources=globo&pageSize=5&apiKey=f6fdb7cb0f2a497d92dbe719a29b197f')
        noticias = json.loads(req.text)

        for news in noticias['articles']:
            titulo = news['title']
            link = news['url']
            new = 'bot: ' + titulo + ' ' + link + '\n'

            self.caixa_de_mensagem.send_keys(new)
            time.sleep(1)

    def responde(self,texto):
        resposta = self.nome_bot.get_response(texto)
        resposta = str(resposta)
        resposta = 'bot: ' + resposta
        self.caixa_de_mensagem = self.driver.find_element_by_xpath("//div[@class='_2A8P4']/div[@class='_1JAUF _2x4bz focused']/div[@class='_2_1wd copyable-text selectable-text']")
        self.caixa_de_mensagem.send_keys(resposta)
        time.sleep(1)
        self.botao_enviar = self.driver.find_element_by_class_name('_1E0Oz')
        self.botao_enviar.click()

    def treina(self):
        conversa = ListTrainer(self.nome_bot)
        for treino in os.listdir('treino/'):
            train = open('treino/'+treino, 'r', encoding='UTF-8').readlines()
            conversa.train(train)
        trainer = ChatterBotCorpusTrainer(self.nome_bot)
        trainer.train('chatterbot.corpus.portuguese')


bot = WhatsAppBot("Gandalf")

bot.treina()


bot.inicia('Teste bot')

bot.saudacao(['Bot: Ola, eu sou o grande mago branco.'])
ultimo_texto = ''

while True:
    text = bot.escuta()
    if text != ultimo_texto and re.match(r'^::', text):
        ultimo_texto = text
        text = text.replace('::', '')
        text = text.lower()
        bot.responde(text)


