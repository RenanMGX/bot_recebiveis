from Entities.imobmebot import ImobmeBot
from Entities.data_manipulation import XWtoDF
from Entities.credencital_load import Credential
from typing import Dict
import pandas as pd

if __name__ == "__main__":
    #carregar aquivo
    path = "#materiais\\Base - Lançamento Juros de Obra2.xlsx"
    
    #ler planilha
    data_with_sheet:Dict[str, pd.DataFrame] = XWtoDF.read_excel(path)
    
    #separar dataframe por colunas
    for sheet in data_with_sheet.keys():
        if 'pagamento' in sheet.lower():
            novos_pagamentos: pd.DataFrame = data_with_sheet[sheet]
        elif 'contratos' in sheet.lower():
            novos_contratos: pd.DataFrame = data_with_sheet[sheet]
    
    credencial = Credential.load("imbme_credential.json")
    bot_navegador = ImobmeBot(user=credencial['user'], password=credencial['password'])
    bot_navegador.executar_contratos(url="http://qas.patrimarengenharia.imobme.com/Contrato/")
    
    #import pdb; pdb.set_trace()
    
