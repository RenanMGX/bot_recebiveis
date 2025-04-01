import pandas as pd
import xlwings as xw # type: ignore
from xlwings.main import Book, Sheet

class XWtoDF:
    @staticmethod
    def calcular_letra(num:int) -> str:
        ultima_coluna:int = num

        coluna_temp:int = 0
        while ultima_coluna >= 27:
            ultima_coluna = ultima_coluna - 26
            coluna_temp += 1

        coluna_extra:str = ""
        if coluna_temp > 0:
            coluna_extra = chr(coluna_temp + 65 - 1)

        return f"{coluna_extra}{chr(ultima_coluna + 65 - 1)}"
    
    @staticmethod
    def read_excel(path:str) -> dict:
        """utiliza o xlwings para ler os dados de uma planilha e retornar um DataFrame

        Args:
            path (str): caminho do arquivo

        Returns:
            dict: nome da sheet, Dataframe com os dados
        """
        app = xw.App(visible=False)
        with app.books.open(path)as wb:
            df:dict = {}
            
            for sheet_name in wb.sheet_names:
                sheet_name:str
                sheet:Sheet = wb.sheets[sheet_name]
                sheet.api.AutoFilter.ShowAllData()
                
                ultima_coluna = sheet.api.UsedRange.Columns.Count
                ultima_coluna_disponivel = XWtoDF.calcular_letra(ultima_coluna + 1) 
                
                sheet.range(f'{ultima_coluna_disponivel}1').value = 'Celula_Colorida'
                
                for row in range(len(sheet.range('A2').expand('down'))):
                   if sheet.range(f'A{row+2}').color:
                       sheet.range(f'{ultima_coluna_disponivel}{row+2}').value = 'colorido'
                
                data: pd.DataFrame = sheet.range(f'A1:{ultima_coluna_disponivel}1').expand('down').options(pd.DataFrame, index=False, header=True).value

                data = data.replace(float('nan'), "")
                data = data[data['Celula_Colorida'] != 'colorido']
                
                #Novo Pagamento
                if '#1_' in sheet_name.lower():
                    data = data[data['Contrato de juros de obra ?'] != '']
                
                if '#1_' in sheet_name.lower():#Novo Pagamento
                    df['novos_pagamentos'] = data
                    #import pdb; pdb.set_trace()
                elif '#2_' in sheet_name.lower(): #Novos Contratos'
                    df['novos_contratos'] = data
                    
                    
        for apps_xw in xw.apps:
            for open_apps in apps_xw.books:
                open_apps:Book
                if open_apps.name in path:
                    open_apps.close()
                    if len(xw.apps) <= 0:
                        apps_xw.kill()
        
        return df
    
    @staticmethod
    def save_excel(*, path:str, df:pd.DataFrame, sheet_name_to_save:str) -> None:
        app = xw.App(visible=False)
        dados_para_adicionar:list = df.values.tolist()
        dados_para_adicionar.insert(0, df.columns.tolist())
        
        solicitacao = [x for x in df['Solicitação']]
        solicitacao.insert(0, 'Solicitação')
        
        with app.books.open(path)as wb:
            for sheet_name in wb.sheet_names:
                if sheet_name_to_save in sheet_name:
                    sheet:Sheet = wb.sheets[wb.sheet_names.index(sheet_name)]
                    for x in range(len(solicitacao)): sheet.range(f'N{x+1}').value = solicitacao[x]
                    #import pdb; pdb.set_trace()
                    
                    #sheet.range('A1').expand().value = dados_para_adicionar
            wb.save()
        
        for apps_xw in xw.apps:
            for open_app in apps_xw.books:
                open_app:Book
                if open_app.name in path:
                    open_app.close()
                    if len(xw.apps):
                        apps_xw.kill()
                        
    @staticmethod
    def save_excel_pagamento(*, path:str, df:pd.DataFrame, sheet_name_to_save:str) -> None:
        app = xw.App(visible=False)
        dados_para_adicionar:list = df.values.tolist()
        dados_para_adicionar.insert(0, df.columns.tolist())
        
        status_script = [x for x in df['Status_Script']]
        status_script.insert(0, 'Status_Script')
        
        with app.books.open(path)as wb:
            for sheet_name in wb.sheet_names:
                if sheet_name_to_save in sheet_name:
                    sheet = wb.sheets[wb.sheet_names.index(sheet_name)]
                    for x in range(len(status_script)): sheet.range(f'R{x+1}').value = status_script[x]
                    #import pdb; pdb.set_trace()
                    
                    #sheet.range('A1').expand().value = dados_para_adicionar
            wb.save()
        
        for apps_xw in xw.apps:
            for open_app in apps_xw.books:
                open_app:Book
                if open_app.name in path:
                    open_app.close()
                    if len(xw.apps):
                        apps_xw.kill()
                        

if __name__ == "__main__":
    dados = XWtoDF.read_excel(r'R:\bot_recebiveis\Base - Lançamento Juros de Obra - SCRIPT (2) 2.xlsx')
    import pdb; pdb.set_trace()