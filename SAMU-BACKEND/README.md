# Projeto SAMU de Excelência 

O projeto de Excelência se baseia em uma API que ira trabalhar em conjunto com o sistema já existente utilizado pelo SAMU.

## Qual é a funcionalidade da API?
 A funcionalidade principal da API consistirá na administração do estoque central do Serviço de Atendimento Móvel de Urgência (SAMU), visando aprimorar a gestão de despesas, a utilização de insumos e equipamentos, bem como o controle de materiais. Além disso, a API será responsável pelo monitoramento do prazo de validade dos insumos, a gestão das viaturas e outras funções correlatas.


## Tabela de conteúdos
   * [Funcionalidades](#funcionalidades)
   * [Tecnologias utilizadas](#tecnologias-utilizadas)
   * [Instalação](#instalacao)
   * [Como usar](#como-usar)
     
## Funcionalidades padrões do projeto
- [x]  Cadastrar (Usuário, equipamentos, medicamento, viatura, material)
- [x]  Deletar (Usuário, equipamentos, medicamento, viatura, material)
- [x]  Listar (Usuário, equipamentos, medicamento, viatura, material)
- [x]  Atualizar (Usuário, equipamentos, medicamento, viatura, material)
- [x]  Alocar (Equipamento, medicamento, material)
- [x]  Desalocar (Equipamento, medicamento, material)

*Vale ressaltar que essas são as funcionalidades padrões, mas existem algumas entidades que contém suas funções particulares.*

## 🛠 Tecnologias Utilizadas
- Python: 3.11.4
- PostgreSql: 13.9(Utilizando o elephantSQL, versão 9 à  ' diante)
- [Docker](https://www.docker.com): 24.0.6
- Docker-compose: v2.20.2
- Ubuntu : 20.04.6
## Requisitos para Uso

- IDE  - VScode, PyCharm, etc.
- Conta no Docker.hub
- Versão Atualizada do Windows referente ao WSL 2
- Núcleo Linux

## Tutorial de Instalação
O WSL é uma ferramenta que permite rodar programas Linux no Windows.  Você deve baixá-lo para fins de desenvolvimento, compatibilidade com aplicativos, uso de ferramentas, compartilhamento de arquivos, e entre outras funcionalidades.

*Vale ressaltar que se você obter Linux em seu sistema operacional, não é necessário instalá-lo.*
- [WSL](https://boom-particle-8c8.notion.site/como-instalar-o-wsl2-readme-md-02dcaa42ac7d490bb8f5bb6620669590)





## 💻 Instalação Padrão

- Observação: Execute os comandos a seguir no terminal da sua IDE ou no terminal do seu sitema operacional, as duas formas(abaixo) de instalação devem seguir os passos da `💻Instalação Local`

- 1 - Crie uma pasta:
```
    mkdir samu
```

- 2 - Entre na pasta do projeto:

```
    cd samu
```

- 3 - Clone o projeto

```
  git clone https://andresouza0365@dev.azure.com/andresouza0365/SAMU/_git/SAMU

```
- 4 - Execute o terminal
* Observação: Será assim caso tenha o VSCode, se não terá que abrir pela própria IDE
```
    code .
```

## 🐋 Execução Docker

- 1 - No caso da troca do "Host" e suas portas, mudanças devem ser feitas no arquivo `🗃️ docker-compose.yaml`.

- 2 - Execute o comando abaixo no seu terminal (IDE ou Shell):
```
    docker-compose up
```

## 🐋 Execução com dev container
É possível executar um container em desenvolvimento, onde as alterações são refletidas no código de forma automática, sem ser necessário realizar build novamente.

### Requisitos
Para essa execução é necessário:
- Estar utilizando a IDE VSCode
- Baixar a extensão Dev Containers da microsoft
- Baixar a extensão Remote Development da microsoft

Após cumprir os requisitos, os passos para execução são os seguintes:

- Já com o VSCode aberto, acessar a barra de pesquisa de comandos dele, utilizando o atalho:

```
    Ctrl + Shift + P
```

- Buscar e selecionar o comando:

```
    Dev Containers: Rebuild And Reopen In Container
```


## 🚩 Execução Local

- 1 -  Abra o terminal da sua IDE ou o terminal do seu sistema operacional

- 2 - Ative o ambiente virtual

```
    python -m venv .env
```
Caso já tenha um ambiente (pasta chamada .env), execute este comando (Windows)
```
    ./.env/Scripts/activate
```
Execute este comando (Linux)
```
    source .env/bin/activate
```
- 3 - Instale as dependências

```
    pip install -r requirements.txt
```
- 4 - Faça a migração
```
    python manage.py migrate
```
- 5 - Inicie a aplicação 

```
    python manage.py runserver
```
## Pronto agora sua aplicação está funcionando, basta clicar no link direcionado no terminal
```
    ctrl + click(mouse)
    Starting development server at http://127.0.0.1:8000/

```
* Assim sendo redirecionado para a sua API.
* Alerta!! Caso não apareça um link, verifique todos os passos fornecidos novamente.
* Observação: Caso tenha a ferramenta Postman, será disponibilizado um arquivo com todos os Endpoints para você fazer suas pesquisas e alterações. Apenas, siga os passos disponibilizados e pronto, você estará com a API funcionando! Além de colections para testes de funcionalidade.


## ✍ Autores

- [SENAI 402 ADS](https://github.com/seu-usuario)
Agradecemos a todos os contribuidores por ajudar a tornar o SAMU um sistema eficiente para unidades de saúde.
   
## Documentação

- Adicionar documentação baseado nas tecnologias e códigos utilizados para versionamento de Code.