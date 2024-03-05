from Entities.imobmebot import ImobmeBot
from Entities.data_manipulation import XWtoDF
from Entities.credencital_load import Credential
from typing import Dict, List, Hashable, Any
import pandas as pd
import traceback
import asyncio
import multiprocessing
import xlwings as xw # type: ignore


def gerar_contratos(df, credencial) -> None:
    print('Iniciando task1')
    bot_navegador = ImobmeBot(user=credencial['user'], password=credencial['password'], url="http://qas.patrimarengenharia.imobme.com/")
    for dados in df: # type: ignore
        if dados['Solicitação'] != "":
            continue
        print(f"{dados['Empreendimento']=}, {dados['Bloco']=}, {dados['Unidade']=} : Iniciado")
        try:
            codigo = bot_navegador.executar_contratos(url="http://qas.patrimarengenharia.imobme.com/Contrato/", dados=dados)
            dados['Solicitação'] = codigo
            print("        Concluido!")
        except Exception as error:
            print(f"{type(error)} | {error}")
            print("        Error!")
            continue
    
    novos_contratos_novo: pd.DataFrame = pd.DataFrame(novos_contratos) 
    XWtoDF.save_excel(path=path, df=novos_contratos_novo, sheet_name_to_save='contratos')

    

def gerar_pagamentos(df, credencial):
    print('Iniciando task2')
    print(df)
    
    # bot_navegador2 = ImobmeBot(user=credencial['user'], password=credencial['password'], url="http://qas.patrimarengenharia.imobme.com/")
    # for dados in df: # type: ignore
    #     if dados['Solicitação'] != "":
    #         continue
    #     print(f"{dados['Empreendimento']=}, {dados['Bloco']=}, {dados['Unidade']=} : Iniciado")
    #     try:
    #         codigo = bot_navegador2.executar_contratos(url="http://qas.patrimarengenharia.imobme.com/Contrato/", dados=dados)
    #         dados['Solicitação'] = codigo
    #         print("        Concluido!")
    #     except Exception as error:
    #         print(f"{type(error)} | {error}")
    #         print("        Error!")
    #         continue


if __name__ == "__main__":
    multiprocessing.freeze_support()
    #carregar aquivo
    path = "#materiais\\Base - Lançamento Juros de Obra3.xlsx"
    
    for app_open in xw.apps:
        if app_open.books[0].name == path.split("\\")[-1]:
            app_open.kill()
        elif app_open.books[0].name == 'Pasta1':
            app_open.kill()
    
    #ler planilha
    data_with_sheet:Dict[str, pd.DataFrame] = XWtoDF.read_excel(path)
    
    #separar dataframe por colunas
    for sheet in data_with_sheet.keys():
        if 'pagamento' in sheet.lower():
            novos_pagamentos: pd.DataFrame = data_with_sheet[sheet]
        if 'contratos' in sheet.lower():
            novos_contratos:List[dict] = data_with_sheet[sheet].to_dict(orient="records")
    
    #import pdb; pdb.set_trace()
    credencial = Credential.load("imbme_credential.json")
    #http://qas.patrimarengenharia.imobme.com/
    #https://patrimarengenharia.imobme.com/,

    #task1 = multiprocessing.Process(target=gerar_contratos, args=(novos_contratos, credencial,))
    #task1.start()
    
    task2 = multiprocessing.Process(target=gerar_pagamentos, args=(novos_pagamentos, credencial,))
    task2.start()
    
    #task1.join()
    task2.join()
    
    
    