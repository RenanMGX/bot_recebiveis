from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from Entities.credencital_load import Credential
from time import sleep

class ImobmeBot:
    def __init__(self, *, user, password) -> None:
        self.browser: webdriver.Chrome = webdriver.Chrome()
        self.__user = user
        self.__password = password
    
    def _find_element(self,mod, target, timeout=10, force=False):
        for _ in range(timeout):
            try:
                result = self.browser.find_element(mod, target)
                return result
            except:
                sleep(1)
        
        if force:
            return self.browser.find_element(By.TAG_NAME, 'html')
        
        raise Exception(f"{mod=}, {target=} | não foi encontrado!")
    
    def login(f):# type: ignore
        def wrap(self, *args, **kwargs):
            result = f(self, *args, **kwargs)# type: ignore
            
            for x in self.browser.find_elements(By.TAG_NAME, 'strong'):
                if 'Imobme - Autenticação' in x.text:
                    print("fazendo login")
                    self._find_element(mod=By.ID, target='login').send_keys(self.__user) 
                    self._find_element(mod=By.ID, target='login').send_keys(self.__password) 
                    import pdb; pdb.set_trace()
            
            
            return result
        return wrap
    
    @login     # type: ignore
    def executar_contratos(self, *, url):
        #self._find_element()
        self.browser.get(url)

if __name__ == "__main__":
    credencial = Credential.load("imbme_credential.json")
    bot_navegador = ImobmeBot(initial_url="http://qas.patrimarengenharia.imobme.com/Contrato/", user=credencial['user'], password=credencial['password'])
    
    bot_navegador.executar_contratos()
    input()