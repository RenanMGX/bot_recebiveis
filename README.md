# Sistema de Gerenciamento e Interação Bot - ImmoFinBot

Este programa é uma solução automatizada destinada à gestão de interações e processamento de dados, enfocando operações financeiras e imobiliárias. Ele integra um sistema de bots para facilitar a comunicação e a execução de tarefas, visando otimizar a eficiência operacional. Configurado através de um conjunto de scripts Python, o sistema oferece ferramentas para manipulação de dados, carregamento de credenciais, e interações específicas do domínio. Ideal para empresas em busca de automação e melhorias na gestão de recebíveis e atendimento.

## Como começar

Para iniciar o programa, é necessário ter o Python instalado em seu ambiente. Com isso configurado, siga os passos abaixo para configurar e executar o programa.

### Pré-requisitos

- Python 3.8 ou superior
- Dependências listadas no arquivo `requirements.txt` (Use o comando `pip install -r requirements.txt` para instalar).

### Instalação

1. Clone o repositório para sua máquina local ou baixe os arquivos do projeto.
2. Instale as dependências necessárias utilizando o gerenciador de pacotes `pip`.

### Configuração

Antes de executar o programa, é necessário configurar as credenciais e variáveis de ambiente necessárias:

1. Abra o arquivo `credencital_load.py`.
2. Insira as credenciais necessárias, como chaves de API e senhas, conforme a documentação específica para cada serviço utilizado pelo programa.

### Execução

Para iniciar o sistema, navegue até a pasta do projeto no terminal e execute o comando:



## Estrutura do Programa

- `main.py`: Ponto de entrada do programa. Orquestra as operações e interações.
- `bot_recebiveis.py`: Contém a lógica para interação com usuários sobre recebíveis e operações financeiras.
- `imobmebot.py`: Implementa funções específicas para o setor imobiliário, facilitando a automação de tarefas relacionadas.
- `data_manipulation.py`: Fornece funcionalidades para manipulação e transformação de dados.
- `credencital_load.py`: Responsável pelo carregamento seguro de credenciais necessárias para a operação do programa.
- `__init__.py`: Arquivo de inicialização do pacote Python, usado para configurações gerais do pacote.

## Contribuindo

Contribuições são sempre bem-vindas! Por favor, leia o arquivo CONTRIBUTING.md para detalhes sobre o nosso código de conduta, e o processo para enviar pedidos de pull.

## Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

