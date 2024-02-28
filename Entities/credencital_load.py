import json
import os

class Credential:
    @staticmethod
    def load(path:str) -> dict:
        """crie / ler um arquivo json contendo as credenciais

        Args:
            path (str): caminho do arquivo que será salvo as crendicias

        Raises:
            FileNotFoundError: caso o arquivo não exista irá criar um e vai alertar que foi criado e pedira para iniciar o script novamente

        Returns:
            dict: dicionario com a credenciais salvas
        """
           
        if not os.path.exists(path):
            with open(path, 'w')as _file:
                json.dump({"user": "", "password": ""},_file)
            raise FileNotFoundError(f"{path=} não existe! então foi criar uma no repositorio, edite as credenciais e execute o codigo novamente!")

        with open(path, 'r')as _file:
            result:dict = json.load(_file)
        return result
        
if __name__ == "__main__":
    credential = Credential.load("test")
    print(credential)