from Entities.imobmebot import ImobmeBot
from Entities.data_manipulation import XWtoDF
from Entities.credencital_load import Credential
from typing import Dict, List, Hashable, Any
import pandas as pd
import traceback

if __name__ == "__main__":
    #carregar aquivo
    path = "#materiais\\planilha_teste.xlsx"
    
    #ler planilha
    data_with_sheet:Dict[str, pd.DataFrame] = XWtoDF.read_excel(path)
    
    #separar dataframe por colunas
    for sheet in data_with_sheet.keys():
        if 'pagamento' in sheet.lower():
            novos_pagamentos: pd.DataFrame = data_with_sheet[sheet]
        elif 'contratos' in sheet.lower():
            novos_contratos:List[dict] = data_with_sheet[sheet].to_dict(orient="records")
    
    credencial = Credential.load("imbme_credential.json")
    #http://qas.patrimarengenharia.imobme.com/
    #https://patrimarengenharia.imobme.com/
    bot_navegador = ImobmeBot(user=credencial['user'], password=credencial['password'], url="http://qas.patrimarengenharia.imobme.com/")
    
    for dados in novos_contratos: # type: ignore
        print(f"{dados['Empreendimento']=}, {dados['Bloco']=}, {dados['Unidade']=} : Iniciado")
        try:
            codigo = bot_navegador.executar_contratos(url="http://qas.patrimarengenharia.imobme.com/Contrato/", dados=dados)
            dados['Solicitação'] = codigo
            print("        Concluido!")
        except Exception as error:
            print(f"{type(error)} | {error}")
            print("        Error!")
            continue
    
    novos_contratos = pd.DataFrame(novos_contratos)    # type: ignore
    print(novos_contratos['Solicitação'])# type: ignore
    
    
    
    
