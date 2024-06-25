from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from Entities.credencital_load import Credential
from time import sleep
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pdb
from typing import Literal
from pandas.core.series import Series

class ImobmeBot:
    @property
    def url_principal(self):
        return self.__url_principal
    def __init__(self, *, user:str, password:str, url:Literal["http://qas.patrimarengenharia.imobme.com/", "https://patrimarengenharia.imobme.com/"]) -> None:
        self.browser: webdriver.Chrome = webdriver.Chrome()
        
        if not url.endswith('/'):
            self.__url_principal:str = url + '/'
        else:
            self.__url_principal = url
            
        self.browser.get(self.__url_principal)
        self.browser.get(self.__url_principal)
        self.browser.maximize_window()
        
        self.__user:str = user
        self.__password:str = password
        
        self._login()
    
    def _find_element(
        self, 
        by, 
        target:str, 
        browser=None, 
        timeout:int=10, 
        force:bool=False, 
        speak:bool=False, 
        scroll:bool=False
    ) -> WebElement:

        for _ in range(timeout*4):
            try:
                result:WebElement
                if browser == None:
                    result = self.browser.find_element(by, target)
                else:
                    browser_temp: WebElement = browser
                    result = browser_temp.find_element(by, target)
                print(f"{target=}") if speak else None
                if scroll:
                    result.location_once_scrolled_into_view
                return result
            except:
                sleep(0.25)
        
        if force:
            print(f"target='html'") if speak else None
            return self.browser.find_element(By.TAG_NAME, 'html')
        
        raise Exception(f"{by=}, {target=} | não foi encontrado!")
    
    def _login(self, tentar:bool=False) -> None:
        if tentar:
            try:
                sleep(1)
                self.browser.find_element(By.ID, 'login')
            except:
                return
        self.browser.get(self.__url_principal)
        self.browser.get(self.__url_principal)
        self._find_element(by=By.ID, target='login').send_keys(str(self.__user)) 
        self._find_element(by=By.ID, target='password').send_keys(str(self.__password))
        self._find_element(by=By.ID, target='password').send_keys(Keys.RETURN) 
                    
        if self._find_element(by=By.XPATH, target='/html/body/div[1]/div/div/div/div[2]/form/div/ul/li', timeout=1, force=True).text == 'Login não encontrado.':
            raise PermissionError("Login não encontrado.")
 
        if 'Senha Inválida.' in (return_error:=self._find_element(by=By.XPATH, target='/html/body/div[1]/div/div/div/div[2]/form/div/ul/li', timeout=1, force=True).text):
            raise PermissionError(return_error)

        self._find_element(by=By.XPATH, target='/html/body/div[2]/div[3]/div/button[1]/span', timeout=2, force=True).click()
                    
    def executar_contratos(self, *, dados:dict) -> str:
        self._login(tentar=True)
        self.browser.get(self.__url_principal + 'Contrato/')
        self.browser.get(self.__url_principal + 'Contrato/')
        self.browser.maximize_window()
        
        #aba pesquisa
        campo_empreendimento:WebElement = self._find_element(By.ID, 'EmpreendimentoId_chzn')
        self.wait_load()
        campo_empreendimento.click()
        
        ul_emp:WebElement = self._find_element(By.TAG_NAME, 'ul', browser=campo_empreendimento)
        for li_emp in ul_emp.find_elements(By.TAG_NAME, 'li'):
            if li_emp.text == dados['Empreendimento']:
                li_emp.click()
                
        campo_bloco:WebElement = self._find_element(By.ID, 'BlocoId_chzn')
        self.wait_load()
        campo_bloco.click()
        
        ul_bloco:WebElement = self._find_element(By.TAG_NAME, 'ul', browser=campo_bloco)
        for li_bloco in ul_bloco.find_elements(By.TAG_NAME, 'li'):
            if li_bloco.text == dados['Bloco']:
                li_bloco.click()
        
        campo_unidade:WebElement = self._find_element(By.ID, 'UnidadeId_chzn')
        self.wait_load()
        campo_unidade.click()
        
        if isinstance(dados['Unidade'], float):
            dados['Unidade'] = int(dados['Unidade'])
        if isinstance(dados['Unidade'], int):
            dados['Unidade'] = str(dados['Unidade'])
        ul_unidade:WebElement = self._find_element(By.TAG_NAME, 'ul', browser=campo_unidade)
        for li_unidade in ul_unidade.find_elements(By.TAG_NAME, 'li'):
            if li_unidade.text == str(int(dados['Unidade'])):
                li_unidade.click()
        
        #aba contrato (Novo)
        self._find_element(By.XPATH, '/html',scroll=True)
        self._find_element(By.XPATH, '//*[@id="AgreementTabs"]/li[2]/a').click()
        
        
        self._find_element(By.XPATH, '//*[@id="Tipo"]/option[3]').click() # tipo Contrato > Avulso
        
        self._find_element(By.ID, 'DataChave', scroll=True).clear()
        self._find_element(By.ID, 'DataChave').send_keys(dados['Data Chave'].strftime('%d%m%Y')) #data Chave
        
        self._find_element(By.ID, 'DataJuros').clear()
        self._find_element(By.ID, 'DataJuros').send_keys(dados['Data Juros'].strftime('%d%m%Y')) #data Juros
        
        while len(self._find_element(By.ID, 'TaxaJuros').get_attribute('value')) > 0: # type: ignore
            self._find_element(By.ID, 'TaxaJuros').send_keys(Keys.BACK_SPACE)
        self._find_element(By.ID, 'TaxaJuros').send_keys(str(dados['Juros (a.a.)'])) # Juros
        
        while len(self._find_element(By.ID, 'TaxaMulta').get_attribute('value')) > 0: # type: ignore
            self._find_element(By.ID, 'TaxaMulta').send_keys(Keys.BACK_SPACE)
        self._find_element(By.ID, 'TaxaMulta').send_keys(str(dados['Multa'])) # Multa
        
        while len(self._find_element(By.ID, 'TaxaMora').get_attribute('value')) > 0: # type: ignore
            self._find_element(By.ID, 'TaxaMora').send_keys(Keys.BACK_SPACE)
        self._find_element(By.ID, 'TaxaMora').send_keys(str(dados['Mora (a.m.)'])) # Mora
        
        indice_pre_chave:WebElement = self._find_element(By.ID, 'IndicePre') # Índice Pré-Chave
        for option in indice_pre_chave.find_elements(By.TAG_NAME, 'option'):
            if option.text == dados['Índice Pré']:
                option.click()
                break

        indice_pos_chave:WebElement = self._find_element(By.ID, 'IndicePos') # Índice Pós-Chave
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
        self._find_element(By.ID, 'ValorParcela').send_keys(str(dados['VR_PAGO'])) # Valor Parcela
        
        #adicionar data de vencimento
        data_mais_30_dias:datetime = datetime.now() + relativedelta(days=30)
        if data_mais_30_dias.day < 25:
            data_final:datetime = datetime(year=data_mais_30_dias.year, month=data_mais_30_dias.month, day=25)
        else:
            data_final = datetime(year=data_mais_30_dias.year, month=(data_mais_30_dias + relativedelta(months=1)).month, day=25)
        self._find_element(By.ID, 'DataPrimeiraParcela').clear()
        self._find_element(By.ID, 'DataPrimeiraParcela').send_keys(data_final.strftime('%d%m%Y'))# Data Vencimento
        
        #import pdb; pdb.set_trace()
        self.wait_load()
        self._find_element(By.ID, 'btnSerieAdd').send_keys(Keys.ENTER)
        
        self._find_element(By.ID, 'serieEdit', timeout=60)
        
        self._find_element(By.XPATH, '//*[@id="Footer"]/div/button').click()
        
        #import pdb; pdb.set_trace()
        
        try:
            if (error:=self._find_element(By.XPATH, '//*[@id="Content"]/section/div[2]/div/div[1]/ul/li').text) != '':
                return error
        except:
            pass
        
        tbody:WebElement = self._find_element(By.TAG_NAME, 'tbody')
        for tr in tbody.find_elements(By.TAG_NAME, 'tr'):
            if 'Em Aprovação' in tr.text:
                codigo:str = tr.text.split(' ')[0]
        
        return codigo
        
    def executar_pagamentos(self, *, dados:dict) -> None:
        self._login(tentar=True)
        self.browser.get(self.__url_principal + 'Contrato/')
        self.browser.get(self.__url_principal + 'Contrato/')
        self.browser.maximize_window()

        self._find_element(By.XPATH, '/html',scroll=True)
        self._find_element(By.ID, 'Keyword').clear()  
        self._find_element(By.ID, 'Keyword').send_keys(str(dados['NO_MUTUARIO'])) 
        self.wait_load(wait_first=1)
        # import pdb; pdb.set_trace()
        # self._find_element(By.ID, 'feedback-loader').get_attribute('style')
        # 'display: block;'
        if self._find_element(By.ID, 'EmpreendimentoId_chzn').text != 'Empreendimento':
            self._find_element(By.XPATH, '/html/body/div/div/section/div[2]/div/div/div[2]/form/div[1]/div/a/abbr', timeout=1, force=True).click()
            self.wait_load(wait_first=1)
        
        # self.wait_load()
        # if self.browser.find_element(By.TAG_NAME, 'tbody').text == 'Nenhum registro':
        #     raise TimeoutError("Nenhum contrato Encontrado")
        
        contrato_lista:str = ""
        
        self.wait_load(wait_first=0, wait_before=1)
        tbody:WebElement = self._find_element(By.ID, 'result-table')
        contratos_encontrador:list = tbody.find_element(By.TAG_NAME, 'tbody').text.split('\n')
        
        numero_endereco_contrato:list = []
        for num in range(len(contratos_encontrador)): 
            if (' Cob. Juros de Obra ' in contratos_encontrador[num]) and (' Ativo ' in contratos_encontrador[num]) and (dados['NO_MUTUARIO'] in contratos_encontrador[num]):
                numero_endereco_contrato.append(num+1)
                
        if 'Nenhum registro' in contratos_encontrador:
            raise TimeoutError("Nenhum contrato Encontrado")        
        
        if len(numero_endereco_contrato) > 1:
            raise ReferenceError("foi encontrado mais de 2 contratos ativos")
        elif len(numero_endereco_contrato) <= 0:
            raise ReferenceError("não foi encontrado nenhum contrato ativo")
        
        # self._find_element(By.XPATH, f'//*[@id="result-table"]/tbody/tr[{numero_endereco_contrato[0]}]', scroll=True)
        # self.wait_load(wait_first=1)
        
        # self.browser.maximize_window()
        # target = f'//*[@id="result-table"]/tbody/tr[{numero_endereco_contrato[0]}]'
        # try:
        #     self._find_element(By.XPATH, target, scroll=True).click()
        # except:
        #     self._find_element(By.ID, 'result-table', scroll=True)
        #     self._find_element(By.XPATH, target).click()        
        # self.wait_load(wait_first=1)
        
        contrato_lista = contratos_encontrador[numero_endereco_contrato[0]-1].split(" ")[0]
        if contrato_lista == "":
            raise RecursionError("Contrato não identificado")        
        self.browser.get(self.__url_principal + f'Contrato//PosicaoFinanceira/{contrato_lista}')
        self.wait_load()
        del contrato_lista
        
        self._find_element(By.XPATH, '/html',scroll=True)
        self._find_element(By.XPATH, '//*[@id="AgreementTabs"]/li[2]/a').click()
        
        if not dados['NO_MUTUARIO'] in self._find_element(By.ID, 'proprietario-container').text:
            raise ReferenceError("pagina do contrato errada!")
        
        self._find_element(By.XPATH, '//*[@id="TipoParcelaId"]/option[3]', scroll=True).click()
        self._find_element(By.XPATH, '//*[@id="TipoAvulsoId"]/option[3]', scroll=True).click()
        
        obs:str = f"VCTO CEF {dados['DT_VENCIMENTO'].strftime('%d/%m/%Y')}"
        self._find_element(By.ID, 'ObservacaoAvulso').send_keys(obs)
        
        self._find_element(By.XPATH, '//*[@id="PeriodicidadeId"]/option[2]').click()
        
        self._find_element(By.ID, 'SerieDataBase').send_keys((datetime.now().replace(day=1)).strftime('%d%m%Y'))
        
        while len(self._find_element(By.ID, 'ValorParcela').get_attribute('value')) > 0: # type: ignore
            self._find_element(By.ID, 'ValorParcela').send_keys(Keys.BACK_SPACE)
        self._find_element(By.ID, 'ValorParcela').send_keys(str(dados['VR_PAGO'])) # Valor Parcela
        
        tabela_contratos:WebElement = self._find_element(By.ID, 'tab-serie')
        contratos_listados:list = self._find_element(By.TAG_NAME, 'tbody', browser=tabela_contratos).text.split('\n')
        
        ultima_dataSTR:str = self._find_element(By.XPATH, f'/html/body/div[1]/form/div/section/div[2]/div/div[8]/div/div/table[4]/tbody/tr[{len(contratos_listados)}]/td[9]').text
        ultima_data:datetime = datetime.strptime(ultima_dataSTR, '%d/%m/%Y')
        
        data_final:datetime = ImobmeBot.calcular_datas_vencimento(ultima_data)
        
        self._find_element(By.ID, 'DataPrimeiraParcela').send_keys(data_final.strftime('%d%m%Y'))
        
        self._find_element(By.ID, 'btnSerieAdd').send_keys(Keys.ENTER)
        self.wait_load()
        
        #import pdb; pdb.set_trace()
        self._find_element(By.XPATH, '//*[@id="Footer"]/div/button').click()
        self.wait_load()
        
        #self._find_element(By.XPATH, '//*[@id="Footer"]/div/button')

    def aba_associativa(self, *, dados:dict|Series):
        self._login(tentar=True)
        self.browser.get(self.url_principal + 'Contrato/')
        self.browser.get(self.url_principal + 'Contrato/')
        self.browser.maximize_window()
        
        self._find_element(By.ID, 'Keyword').clear()  
        self._find_element(By.ID, 'Keyword').send_keys(str(dados['CPF']))
        
        if self._find_element(By.ID, 'EmpreendimentoId_chzn').text != 'Empreendimento':
            self._find_element(By.XPATH, '/html/body/div/div/section/div[2]/div/div/div[2]/form/div[1]/div/a/abbr', timeout=1, force=True).click()
            self.wait_load(wait_first=1)
        #pdb.set_trace()  
          
        contrato_lista:str = ""
        
        self.wait_load(wait_first=1, wait_before=1)
        tbody:WebElement = self._find_element(By.ID, 'result-table')
        contratos_encontrador:list = tbody.find_element(By.TAG_NAME, 'tbody').text.split('\n')
        
        numero_endereco_contrato:list = []
        
        #	
        for num in range(len(contratos_encontrador)): 
            if ((' PCV ' in contratos_encontrador[num]) or (' Cessão ' in contratos_encontrador[num])) and (' Ativo ' in contratos_encontrador[num]):
                numero_endereco_contrato.append(num+1)
        
        
        
        
        
        if 'Nenhum registro' in contratos_encontrador:
            raise TimeoutError("Nenhum contrato Encontrado")        
        
        if len(numero_endereco_contrato) > 1:
            #pdb.set_trace()
            raise ReferenceError("foi encontrado mais de 2 contratos ativos")
        elif len(numero_endereco_contrato) <= 0:
            #pdb.set_trace()
            raise ReferenceError("não foi encontrado nenhum contrato ativo")
        
        contrato_lista = contratos_encontrador[numero_endereco_contrato[0]-1].split(" ")[0]
        if contrato_lista == "":
            raise RecursionError("Contrato não identificado")  
        
        #
            
        self.browser.get(self.url_principal + f'/Contrato/Associativo/{contrato_lista}')
        self.wait_load()
        del contrato_lista
        
        #pdb.set_trace()
        
        existe_serie_associativa = False
        tags_h4 = self.browser.find_elements(By.TAG_NAME, 'h4')
        for tag_h4 in tags_h4:
            if 'Série Associativa' == tag_h4.text:
                existe_serie_associativa = True
        if not existe_serie_associativa:
            return "sem parcela associativo"
        
        try:
            self._find_element(By.ID, 'ContratoCd').clear()  
            self._find_element(By.ID, 'ContratoCd').send_keys(str(dados['Contrato']))
            
            self._find_element(By.ID, 'DataAssinatura').clear()
            data:datetime = dados['Data de assinatura']
            self._find_element(By.ID, 'DataAssinatura').send_keys(data.strftime('%d%m%Y'))
            
            self._find_element(By.ID, 'Agencia').clear()  
            self._find_element(By.ID, 'Agencia').send_keys(str(dados['Agência']))
            
            self._find_element(By.ID, 'Banco').clear()  
            self._find_element(By.ID, 'Banco').send_keys(str(dados['Banco']))
            
            self.limpar_campo(By.NAME, 'ValorTerreno')
            self._find_element(By.NAME, 'ValorTerreno').send_keys(str(dados['Valor do terreno']).replace('.', ','))
            
            self.limpar_campo(By.NAME, 'ValorFGTS')
            self._find_element(By.NAME, 'ValorFGTS').send_keys(str(dados['Valor do FGTS']).replace('.', ','))
            
            self.limpar_campo(By.NAME, 'ValorSubsidio')
            self._find_element(By.NAME, 'ValorSubsidio').send_keys(str(dados['Valor do subsídio']).replace('.', ','))
            
            self.limpar_campo(By.NAME, 'ValorFinanciamento')
            self._find_element(By.NAME, 'ValorFinanciamento').send_keys(str(dados['Valor do financiamento']).replace('.', ','))
        except:
            return "Já foi executado não é possivel alterar"
        
        
        self.wait_load(wait_before=1)
        
        #pdb.set_trace()
        self._find_element(By.ID, 'Salvar').click()
        
        lista_error:list
        try:
            lista_error = self.browser.find_element(By.CLASS_NAME, "validation-summary-errors").text.split("\n")
        except:
            lista_error = []
        
        retorno:str = ""
        if len(lista_error) > 0 :
            for erro in lista_error:
                if 'A soma dos Valores de FGTS, Subsídio e Financiamento deve ser igual ao valor da Série Associativa.' == erro:
                    valor_atualizado = self._find_element(By.XPATH, '//*[@id="Content"]/section/div[2]/div/div/div[3]/div/div/table/tbody/tr/td[8]').text
                    retorno += f"{erro} valor atualizado = {valor_atualizado} / "
                else:
                    retorno += f"{erro} / "
        else:
            retorno = "Concluido!"
        
        
        return retorno
        
    def limpar_campo(self, by:str, target:str):
        while len(str(self._find_element(by, target).get_attribute('value'))) > 0:
            self._find_element(by, target).send_keys(Keys.BACKSPACE)

    def wait_load(
        self, 
        wait_first:int|float=1, 
        wait_before:int|float=0.1
    ) -> None:
        
        sleep(wait_first)
        while self._find_element(By.ID, 'feedback-loader').get_attribute('style') == 'display: block;':
            sleep(0.005)
        sleep(wait_before)
    
    @staticmethod
    def calcular_datas_vencimento(data:datetime) -> datetime:
        data_mais_30_dias:datetime = data + relativedelta(days=30)
        
        data_final:datetime
        if (data_mais_30_dias-datetime.now()).days <= 30:
            data_atual_mais_30_dias:datetime = datetime.now() + relativedelta(days=30)
            if data_atual_mais_30_dias.day < 25:
                data_final = datetime(year=data_atual_mais_30_dias.year, month=data_atual_mais_30_dias.month, day=25)
            else:
                data_final = datetime(year=data_atual_mais_30_dias.year, month=(data_atual_mais_30_dias + relativedelta(months=1)).month, day=25)
        else:
            data_final = (data.replace(day=25)) + relativedelta(months=1)
        
        return data_final
    
if __name__ == "__main__":
    #credencial:dict = Credential.load("imbme_credential.json")
    #bot_navegador = ImobmeBot(user=credencial['user'], password=credencial['password'])
    
    #bot_navegador.executar_contratos(url="http://qas.patrimarengenharia.imobme.com/Contrato/")
    input()