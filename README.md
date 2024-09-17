# Coleção de Jogos - API e Banco de Dados

## Descrição

Este projeto é uma API desenvolvida para gerenciar uma coleção de jogos, com suporte para criação, leitura e exclusão de informações sobre jogos. Inclui um banco de dados para armazenamento dos dados e uma interface de API para interação com a aplicação.

## Instruções de Instalação

Para configurar o ambiente local e iniciar o projeto, siga as etapas abaixo:

### 1. Clonar o Repositório

Clone o repositório do projeto para o seu ambiente local usando o comando:

```bash
git clone <URL_DO_REPOSITORIO>
```

Substitua `<URL_DO_REPOSITORIO>` pela URL do repositório.

### 2. Configurar o Ambiente Virtual

É altamente recomendável utilizar um ambiente virtual como o [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) para isolar as dependências do projeto. Navegue até o diretório raiz do projeto e crie um ambiente virtual:

```bash
cd <DIRETORIO_DO_PROJETO>
python -m venv venv
```

Ative o ambiente virtual:

- No Windows:

  ```bash
  venv\Scripts\activate
  ```

- No macOS e Linux:

  ```bash
  source venv/bin/activate
  ```

### 3. Instalar Dependências

Com o ambiente virtual ativado, instale as bibliotecas necessárias utilizando o arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Comandos de Inicialização

Para iniciar a API, execute o seguinte comando:

```bash
flask run --host 0.0.0.0 --port 5000
```

#### Modo de Desenvolvimento

Se você estiver desenvolvendo e desejar que o servidor reinicie automaticamente após mudanças no código, utilize o parâmetro `--reload`:

```bash
flask run --host 0.0.0.0 --port 5000 --reload
```

### 5. Verificar o Status da API

Após iniciar o servidor, abra o navegador e acesse o seguinte link para verificar o status da API:

[http://localhost:5000/#/](http://localhost:5000/#/)

## Observações

- Certifique-se de que o Flask esteja instalado e configurado corretamente.
- Mantenha o ambiente virtual ativo enquanto trabalha no projeto para garantir que todas as dependências estejam disponíveis.

Para qualquer dúvida ou problema, consulte a [documentação do Flask](https://flask.palletsprojects.com/en/2.3.x/) ou entre em contato com o desenvolvedor responsável.