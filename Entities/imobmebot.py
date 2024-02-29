from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from Entities.credencital_load import Credential
from time import sleep
from datetime import datetime
from dateutil.relativedelta import relativedelta

class ImobmeBot:
    def __init__(self, *, user, password, url) -> None:
        self.browser: webdriver.Chrome = webdriver.Chrome()
        self.__url_principal = url
        self.browser.get(self.__url_principal)
        
        self.__user = user
        self.__password = password
        
        self._login()
    
    def _find_element(self, by, target:str, browser=None, timeout:int=10, force:bool=False) -> WebElement:
        for _ in range(timeout):
            try:
                if browser == None:
                    result: WebElement = self.browser.find_element(by, target)
                else:
                    browser_temp: WebElement = browser
                    result = browser_temp.find_element(by, target)
                #print(f"{target=}")
                return result
            except:
                sleep(1)
        
        if force:
            #print(f"target='html'")
            return self.browser.find_element(By.TAG_NAME, 'html')
        
        raise Exception(f"{by=}, {target=} | não foi encontrado!")
    
    def _login(self) -> None:
        self.browser.get(self.__url_principal)
        self._find_element(by=By.ID, target='login').send_keys(self.__user) 
        self._find_element(by=By.ID, target='password').send_keys(self.__password)
        self._find_element(by=By.ID, target='password').send_keys(Keys.RETURN) 
                    
        if self._find_element(by=By.XPATH, target='/html/body/div[1]/div/div/div/div[2]/form/div/ul/li', timeout=1, force=True).text == 'Login não encontrado.':
            raise PermissionError("Login não encontrado.")
 
        if 'Senha Inválida.' in (return_error:=self._find_element(by=By.XPATH, target='/html/body/div[1]/div/div/div/div[2]/form/div/ul/li', timeout=1, force=True).text):
            raise PermissionError(return_error)

        self._find_element(by=By.XPATH, target='/html/body/div[2]/div[3]/div/button[1]/span', timeout=2, force=True).click()
                    
        #import pdb; pdb.set_trace()
    
    def executar_contratos(self, *, url:str, dados:dict) -> str:
        self.browser.get(url)
        
        #aba pesquisa
        campo_empreendimento = self._find_element(By.ID, 'EmpreendimentoId_chzn')
        sleep(1)
        campo_empreendimento.click()
        
        ul_emp = self._find_element(By.TAG_NAME, 'ul', browser=campo_empreendimento)
        for li_emp in ul_emp.find_elements(By.TAG_NAME, 'li'):
            if li_emp.text == dados['Empreendimento']:
                li_emp.click()
                
        campo_bloco = self._find_element(By.ID, 'BlocoId_chzn')
        sleep(1)
        campo_bloco.click()
        
        ul_bloco = self._find_element(By.TAG_NAME, 'ul', browser=campo_bloco)
        for li_bloco in ul_bloco.find_elements(By.TAG_NAME, 'li'):
            if li_bloco.text == dados['Bloco']:
                li_bloco.click()
        
        campo_unidade = self._find_element(By.ID, 'UnidadeId_chzn')
        sleep(1)
        campo_unidade.click()
        
        if isinstance(dados['Unidade'], float):
            dados['Unidade'] = int(dados['Unidade'])
        if isinstance(dados['Unidade'], int):
            dados['Unidade'] = str(dados['Unidade'])
        ul_unidade = self._find_element(By.TAG_NAME, 'ul', browser=campo_unidade)
        for li_unidade in ul_unidade.find_elements(By.TAG_NAME, 'li'):
            if li_unidade.text == str(int(dados['Unidade'])):
                li_unidade.click()
        
        self._find_element(By.XPATH, '//*[@id="AgreementTabs"]/li[2]/a').click()
        
        #aba contrato (Novo)
        self._find_element(By.XPATH, '//*[@id="Tipo"]/option[3]').click() # tipo Contrato > Avulso
        
        self._find_element(By.ID, 'DataChave').clear()
        self._find_element(By.ID, 'DataChave').send_keys(dados['Data Chave'].strftime('%d%m%Y')) #data Chave
        
        self._find_element(By.ID, 'DataJuros').clear()
        self._find_element(By.ID, 'DataJuros').send_keys(dados['Data Juros'].strftime('%d%m%Y')) #data Juros
        
        while len(self._find_element(By.ID, 'TaxaJuros').get_attribute('value')) > 0: # type: ignore
            self._find_element(By.ID, 'TaxaJuros').send_keys(Keys.BACK_SPACE)
        self._find_element(By.ID, 'TaxaJuros').send_keys(dados['Juros (a.a.)']) # Juros
        
        while len(self._find_element(By.ID, 'TaxaMulta').get_attribute('value')) > 0: # type: ignore
            self._find_element(By.ID, 'TaxaMulta').send_keys(Keys.BACK_SPACE)
        self._find_element(By.ID, 'TaxaMulta').send_keys(dados['Multa']) # Multa
        
        while len(self._find_element(By.ID, 'TaxaMora').get_attribute('value')) > 0: # type: ignore
            self._find_element(By.ID, 'TaxaMora').send_keys(Keys.BACK_SPACE)
        self._find_element(By.ID, 'TaxaMora').send_keys(dados['Mora (a.m.)']) # Mora
        
        indice_pre_chave = self._find_element(By.ID, 'IndicePre') # Índice Pré-Chave
        for option in indice_pre_chave.find_elements(By.TAG_NAME, 'option'):
            if option.text == dados['Índice Pré']:
                option.click()
                break

        indice_pos_chave = self._find_element(By.ID, 'IndicePos') # Índice Pós-Chave
        for option in indice_pos_chave.find_elements(By.TAG_NAME, 'option'):
            if option.text == dados['Índice Pós']:
                option.click()
                break
        
        self._find_element(By.XPATH, '//*[@id="TipoParcelaId"]/option[3]').click() # Tipo Parcela > Avulso
        self._find_element(By.XPATH, '//*[@id="TipoAvulsoId"]/option[3]').click() # Tipo Avulso > Cob. Juros de Obra
        
        obs = f"VCTO CEF {dados['DT_VENCIMENTO'].strftime('%d/%m/%Y')}"
        self._find_element(By.ID, 'ObservacaoAvulso').send_keys(obs) # Observação
        
        self._find_element(By.XPATH, '//*[@id="PeriodicidadeId"]/option[2]').click() # Periodicidade
        
        self._find_element(By.ID, 'SerieDataBase').clear()
        self._find_element(By.ID, 'SerieDataBase').send_keys((datetime.now().replace(day=1)).strftime('%d%m%Y')) # Data Base
        
        
        while len(self._find_element(By.ID, 'ValorParcela').get_attribute('value')) > 0: # type: ignore
            self._find_element(By.ID, 'ValorParcela').send_keys(Keys.BACK_SPACE)
        self._find_element(By.ID, 'ValorParcela').send_keys(dados['VR_PAGO']) # Valor Parcela
        
        #adicionar data de vencimento
        data_mais_30_dias = datetime.now() + relativedelta(days=30)
        if data_mais_30_dias.day < 25:
            data_final = datetime(year=data_mais_30_dias.year, month=data_mais_30_dias.month, day=25)
        else:
            data_final = datetime(year=data_mais_30_dias.year, month=(data_mais_30_dias + relativedelta(months=1)).month, day=25)
        self._find_element(By.ID, 'DataPrimeiraParcela').clear()
        self._find_element(By.ID, 'DataPrimeiraParcela').send_keys(data_final.strftime('%d%m%Y'))# Data Vencimento
        
        #import pdb; pdb.set_trace()
        sleep(1)
        self._find_element(By.ID, 'btnSerieAdd').send_keys(Keys.ENTER)
        
        self._find_element(By.ID, 'serieEdit', timeout=60)
        
        self._find_element(By.XPATH, '//*[@id="Footer"]/div/button').click()
        
        #import pdb; pdb.set_trace()
        
        try:
            if (error:=self._find_element(By.XPATH, '//*[@id="Content"]/section/div[2]/div/div[1]/ul/li').text) != '':
                return error
        except:
            pass
            
        
        tbody = self._find_element(By.TAG_NAME, 'tbody')
        for tr in tbody.find_elements(By.TAG_NAME, 'tr'):
            if 'Em Aprovação' in tr.text:
                codigo:str = tr.text.split(' ')[0]
        
        return codigo
        

if __name__ == "__main__":
    credencial = Credential.load("imbme_credential.json")
    #bot_navegador = ImobmeBot(user=credencial['user'], password=credencial['password'])
    
    #bot_navegador.executar_contratos(url="http://qas.patrimarengenharia.imobme.com/Contrato/")
    input()