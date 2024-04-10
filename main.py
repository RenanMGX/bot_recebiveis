from Entities.imobmebot import ImobmeBot
from Entities.data_manipulation import XWtoDF
from Entities.credencital_load import Credential
from datetime import datetime
from typing import Dict, List
import pandas as pd
import traceback
import xlwings as xw # type: ignore
import os


def gerar_contratos(*, df:pd.DataFrame, navegador:ImobmeBot, path:str) -> None:
    print('\n\nCriando novos contratos')
    log_error: LogOperation = LogOperation()
    novos_contratos:List[dict] = df.to_dict(orient="records")
    
    for dados in novos_contratos:
        if dados['Solicitação'] != "":
            continue
        print(f"{dados['Empreendimento']=}, {dados['Bloco']=}, {dados['Unidade']=} : Iniciado")
        try:
            codigo = navegador.executar_contratos(dados=dados)
            dados['Solicitação'] = codigo
            log_error.save(operation="Contratos", status="Concluido",type_error="", descript=f"{dados['Empreendimento']=}, {dados['Bloco']=}, {dados['Unidade']=}, {codigo=}")
            print("        Concluido!")
        except Exception as error:
            log_error.save(operation="Contratos", status="Error", type_error=f"{type(error)} -> {error}", descript=f"{dados['Empreendimento']=}, {dados['Bloco']=}, {dados['Unidade']=} : ")
            print(f"        Error! - {type(error)} -> {error}")
    
    novos_contratos_novo: pd.DataFrame = pd.DataFrame(novos_contratos) 
    try:
        XWtoDF.save_excel(path=path, df=novos_contratos_novo, sheet_name_to_save='#2_')
        log_error.save(operation="Salvar_Planilha", status="Concluido", type_error="", descript="arquivos salvos na planilha como sucesso")
    except Exception as error:
        print(traceback.format_exc())
        error_descript = traceback.format_exc().replace('\n', ' | ')
        log_error.save(operation="Salvar_Planilha", status="Error", type_error=str(error), descript=f"{type(error)} -> {error_descript}")

    

def gerar_pagamentos(*, df:pd.DataFrame, navegador:ImobmeBot, path:str):
    from selenium.common.exceptions import StaleElementReferenceException
    log_error: LogOperation = LogOperation()
    print('\n\nExecutando Pagamentos!')
    novos_pagamentos:List[dict] = df.to_dict(orient="records")
    
    for dados in novos_pagamentos:
        
        print(dados['NO_MUTUARIO'])
        try:
            navegador.executar_pagamentos(dados=dados)
            log_error.save(operation="Pagamentos", status="Concluido", type_error="", descript=dados['NO_MUTUARIO'])
            dados['Status_Script'] = "Concluido"
            print("        Concluido!")
        except ReferenceError as error:
            log_error.save(operation="Pagamentos", status="Error", type_error=str(error), descript=f"{dados['NO_MUTUARIO']}")
            dados['Status_Script'] = str(error)
            print(f"        Error! -> {error}")
        except TimeoutError as error:
            log_error.save(operation="Pagamentos", status="Error", type_error=str(error), descript=f"{dados['NO_MUTUARIO']}")
            dados['Status_Script'] = str(error)
            print(f"        Error! -> {error}")
        except StaleElementReferenceException as error:
            log_error.save(operation="Pagamentos", status="Error", type_error=str(error), descript=f"{dados['NO_MUTUARIO']}, Message: stale element reference: stale element not found")
            dados['Status_Script'] = str(error)
            print(f"        Error! -> Message: stale element reference: stale element not found")
        except Exception as error:
            error_descript = traceback.format_exc().replace('\n', ' | ')
            log_error.save(operation="Pagamentos", status="Error", type_error=str(error), descript=f"{dados['NO_MUTUARIO']}, {error_descript=}")
            dados['Status_Script'] = str(error).replace("\n", "|")
            print(traceback.format_exc())
            
    novos_pagamentos_novo: pd.DataFrame = pd.DataFrame(novos_pagamentos) 
    try:
        XWtoDF.save_excel_pagamento(path=path, df=novos_pagamentos_novo, sheet_name_to_save='#1_')
        log_error.save(operation="Salvar_Planilha", status="Concluido", type_error="", descript="arquivos salvos na planilha como sucesso")
    except Exception as error:
        print(traceback.format_exc())
        error_descript = traceback.format_exc().replace('\n', ' | ')
        log_error.save(operation="Salvar_Planilha", status="Error", type_error=str(error), descript=f"{type(error)} -> {error_descript}")

        
class LogOperation:
    def __init__(self, date=datetime.now(), filename='registros.csv') -> None:
        self.date:datetime = date
        self.file_name:str = (filename + '.csv') if not filename.endswith('.csv') else filename
        
        if not os.path.exists(self.file_name):
            with open(self.file_name, 'w', encoding='ISO-8859-1')as _file:
                _file.write("data;operação;estatus;tipo;descrição\n")
                
    
    def save(self, *, operation:str, status:str, type_error:str, descript:str) -> None:
        for app_open in xw.apps:
            if app_open.books[0].name == self.file_name:
                app_open.kill()
            elif app_open.books[0].name == 'Pasta1':
                app_open.kill()
        with open('registros.csv', 'a', encoding='ISO-8859-1')as _file:
            _file.write(f"{self.date.strftime('%d/%m/%Y')};{operation};{status};{type_error};{descript}\n")

if __name__ == "__main__":
    log_error: LogOperation = LogOperation()
    try:
        #carregar aquivo
        path:str = "#materiais\\Base - Lançamento Juros de Obra3.xlsx"
        
        for app_open in xw.apps:
            if app_open.books[0].name == path.split("\\")[-1]:
                app_open.kill()
            elif app_open.books[0].name == 'Pasta1':
                app_open.kill()
        
        #ler planilha
        dados:Dict[str, pd.DataFrame] = XWtoDF.read_excel(path)
        try:
            dados['novos_pagamentos']
        except KeyError:
            raise KeyError("a sheet Novos Pagamentos não foi encontrada!")
        try:
            dados['novos_contratos']
        except KeyError:
            raise KeyError("a sheet Novos Contratos não foi encontrada!")
        
        #import pdb; pdb.set_trace()
        credencial:dict = Credential("imobme_credential.json").load()
        #http://qas.patrimarengenharia.imobme.com/
        #https://patrimarengenharia.imobme.com/,
        bot_navegador:ImobmeBot = ImobmeBot(user=credencial['user'], password=credencial['password'], url="http://qas.patrimarengenharia.imobme.com/")

        gerar_contratos(df=dados['novos_contratos'], navegador=bot_navegador, path=path)
        
        gerar_pagamentos(df=dados['novos_pagamentos'], navegador=bot_navegador, path=path)
        
        print("fim")
    
    except Exception as error:
        path_log:str = "log_error\\"
        if not os.path.exists(path_log):
            os.makedirs(path_log)
        
        file_name:str = f"{path_log}{datetime.now().isoformat().replace(':', '.')}.txt"
        with open(file_name, 'w')as _file:
            _file.write(traceback.format_exc())
    
    