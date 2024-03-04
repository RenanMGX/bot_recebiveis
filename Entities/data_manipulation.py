import pandas as pd
import xlwings as xw # type: ignore

class XWtoDF:
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
                sheet = wb.sheets[sheet_name]
                
                
                data: pd.DataFrame = sheet.range('A1').expand().options(pd.DataFrame, index=False, header=True).value
                #data: pd.DataFrame = sheet.range('A1:AD1').expand('down').options(pd.DataFrame, index=False, header=True).value
                
                # for coluna in data.columns:
                #     if pd.api.types.is_datetime64_any_dtype(data[coluna]):
                #         data[coluna] = data[coluna].dt.to_pydatetime()
                df[sheet_name] = data.replace(float('nan'), "")
                #import pdb; pdb.set_trace()
        
        for app_open in xw.apps:
            if app_open.books[0].name == path.split("\\")[-1]:
                app_open.kill()
            elif app_open.books[0].name == 'Pasta1':
                app_open.kill()
        
        return df
    
    def save_excel(*, path:str, df:pd.DataFrame, sheet_name_to_save:str) -> None:
        app = xw.App(visible=False)
        dados_para_adicionar:list = df.values.tolist()
        dados_para_adicionar.insert(0, df.columns.tolist())
        
        solicitacao = [x for x in df['Solicitação']]
        solicitacao.insert(0, 'Solicitação')
        
        with app.books.open(path)as wb:
            for sheet_name in wb.sheet_names:
                if sheet_name_to_save in sheet_name:
                    sheet = wb.sheets[wb.sheet_names.index(sheet_name)]
                    for x in range(len(solicitacao)): sheet.range(f'N{x+1}').value = solicitacao[x]
                    #import pdb; pdb.set_trace()
                    
                    #sheet.range('A1').expand().value = dados_para_adicionar
            wb.save()
        
        for x in xw.apps:
            if x.books[0].name == path.split("\\")[-1]:
                x.kill()
            elif x.books[0].name == 'Pasta1':
                x.kill()

if __name__ == "__main__":
    pass