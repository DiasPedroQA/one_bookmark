# Resumo das Funcionalidades da API One Bookmark

1. **Inicialização do Servidor (src/main.py)**:
   - O módulo `main.py` é o ponto de entrada da aplicação, responsável por
   iniciar o servidor FastAPI. Ele importa e executa a função `iniciar_servidor`
   do módulo `infraestrutura.servidor`. Isso permite que o servidor seja iniciado
   ao executar o comando `python src/main.py`.

2. **Configuração do Servidor FastAPI (src/infraestrutura/servidor.py)**:
   - O módulo `servidor.py` configura a instância da aplicação FastAPI.
   Nele, são definidos o título, a descrição e a versão da API.
   O módulo também inclui as rotas definidas no `aplicacao.rotas`
   e inicia o servidor usando Uvicorn. O servidor escuta na porta 8000
   e tem recarregamento automático habilitado, permitindo que as alterações
   no código sejam refletidas sem reiniciar manualmente o servidor.

3. **Rotas para Validação de Caminhos (src/aplicacao/rotas.py)**:
   - O módulo `rotas.py` define as rotas da API para validar caminhos de arquivos.
   A rota `/validar-caminhos/` recebe uma lista de caminhos como parâmetro e
   verifica se são válidos ou inválidos, utilizando uma lista de caminhos válidos
   e inválidos pré-definida para diferentes sistemas operacionais (Linux, macOS
   e Windows). A validação é feita através da função `log_requisicao`, que registra
   os resultados da validação no log.

4. **Registro de Logs (src/infraestrutura/logger.py)**:
   - O módulo `logger.py` é responsável pela configuração do registro de logs da aplicação.
   Ele cria um arquivo `log_requisicoes.log`, onde as requisições de validação de caminhos
   são registradas com informações sobre se a validação foi bem-sucedida ou não.
   As mensagens são formatadas para incluir a data, hora, nível de log e a mensagem em si.

5. **Validação de Caminhos (src/dominio/validacao.py)**:
   - O módulo `validacao.py` fornece funções para validar a existência
   de caminhos no sistema de arquivos. A função `validar_caminho`
   verifica se um caminho específico existe e retorna um dicionário
   com o status da validação. A função `validar_caminhos` aceita uma
   lista de caminhos e classifica cada um deles como válido ou inválido,
   retornando um objeto JSON com as listas correspondentes.

6. **Modelos de Dados (src/dominio/modelos.py)**:
   - O módulo `modelos.py` define os Data Transfer Objects (DTOs) utilizados
   na API. `CaminhoEntradaDTO` é o modelo que representa a estrutura de entrada
   contendo uma lista de caminhos a serem validados, enquanto `CaminhoSaidaDTO`
   representa a estrutura de saída que contém as listas de caminhos válidos e inválidos.
   O Pydantic é utilizado para validação automática dos dados de entrada e saída.

### Conclusão
A API One Bookmark fornece uma solução robusta para validar caminhos
de arquivos em diferentes sistemas operacionais, com um sistema de
logging integrado para monitorar o desempenho e os resultados das requisições.
As funcionalidades estão organizadas em módulos distintos, promovendo
uma arquitetura limpa e fácil de manter.
