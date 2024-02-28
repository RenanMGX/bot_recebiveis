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
                
                # for coluna in data.columns:
                #     if pd.api.types.is_datetime64_any_dtype(data[coluna]):
                #         data[coluna] = data[coluna].dt.to_pydatetime()
                
                df[sheet_name] = data
        
        for app_open in xw.apps:
            if xw.books[0].name == path.split("\\")[-1]:
                app_open.kill()
        
        return df

if __name__ == "__main__":
    pass