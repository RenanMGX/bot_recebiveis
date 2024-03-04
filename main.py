from Entities.imobmebot import ImobmeBot
from Entities.data_manipulation import XWtoDF
from Entities.credencital_load import Credential
from typing import Dict, List, Hashable, Any
import pandas as pd
import traceback
import xlwings as xw # type: ignore

if __name__ == "__main__":
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
            #import pdb; pdb.set_trace()
            #df_contratos_temp = data_with_sheet[sheet]
            #df_contratos_temp = df_contratos_temp[df_contratos_temp['Solicitação'] == ""]
            novos_contratos:List[dict] = data_with_sheet[sheet].to_dict(orient="records")
            
    
    
    
    #import pdb; pdb.set_trace()
    credencial = Credential.load("imbme_credential.json")
    #http://qas.patrimarengenharia.imobme.com/
    #https://patrimarengenharia.imobme.com/
    bot_navegador = ImobmeBot(user=credencial['user'], password=credencial['password'], url="http://qas.patrimarengenharia.imobme.com/")
    
    for dados in novos_contratos: # type: ignore
        if dados['Solicitação'] != "":
            print("passou")
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
    print(novos_contratos_novo['Solicitação'])
    
    XWtoDF.save_excel(path=path, df=novos_contratos_novo, sheet_name_to_save='contratos')
    
    #import pdb; pdb.set_trace()
    
    
    
    
