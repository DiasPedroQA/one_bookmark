# `README.md`

````md
# One Bookmark - API para Manipulação de Arquivos HTML

Este repositório contém o código-fonte da **One Bookmark**, uma API em Python desenvolvida para manipular e processar arquivos HTML. O projeto utiliza TDD (Desenvolvimento Orientado a Testes) com `pytest` e `coverage` para garantir a qualidade e cobertura de testes.

## Objetivo do Projeto

A **One Bookmark** tem como finalidade:

- Ler arquivos HTML e diretórios.
- Extrair dados das tags `<a>` e `<h3>` usando **BeautifulSoup**.
- Retornar os resultados em formato JSON.

## Funcionalidades Principais

- **Leitura de arquivos e diretórios HTML**: A API permite navegar por diretórios e identificar arquivos HTML para extração de dados.
- **Extração de dados**: Os dados das tags HTML, como `<a>` e `<h3>`, são capturados e estruturados.
- **Saída em formato JSON**: Todos os resultados processados são convertidos em JSON para fácil manipulação.
- **Desenvolvimento orientado a testes**: A API é desenvolvida utilizando boas práticas de TDD com cobertura de testes.

## Como Configurar o Projeto?

### Requisitos

- **Sistema Operacional**: Ubuntu (ou qualquer sistema Unix-like).
- **Python**: Versão 3.12.3

### Passos de Configuração

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/DiasPedroQA/one_bookmark.git
   cd one_bookmark
   ```
````

2. **Crie e ative o ambiente virtual com `venv`**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instale as dependências**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configuração do Banco de Dados** (se aplicável):
   - Não há banco de dados necessário neste projeto no momento. Dependências relacionadas à infraestrutura e banco de dados podem ser adicionadas no futuro.

## Como Executar os Testes?

Para garantir a qualidade do código, execute os testes com `pytest`:

```bash
pytest --cov=app
```

Isso executará os testes unitários e gerará um relatório de cobertura de código.

## Como Contribuir?

Se você deseja contribuir com o desenvolvimento da **One Bookmark**, siga as diretrizes abaixo:

- **Escrevendo testes**:

  - Certifique-se de cobrir novos recursos com testes unitários.
  - Utilize `pytest` e busque manter uma cobertura de testes alta com `pytest-cov`.

- **Revisão de código**:

  - Todo código deve passar por revisão antes de ser aceito no repositório principal.

- **Padrões de código**:
  - Utilize `flake8` e `black` para garantir que o código segue os padrões de formatação e qualidade.

## Contato

Para dúvidas ou contribuições, entre em contato com o administrador do repositório:

- **Nome**: Pedro PM Dias
- **Email**: diaspedro.dev@gmail.com

Fique à vontade para abrir issues ou enviar pull requests com sugestões e melhorias!

## Recursos Adicionais

- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/): Guia para trabalhar com a extração de dados de HTML.
- [Pytest Documentation](https://docs.pytest.org/en/7.0.x/): Documentação oficial do framework de testes.
- [Aprenda Markdown](https://github.com/tutorials/markdowndemo): Guia útil para escrever e formatar documentos em Markdown.

```

```
