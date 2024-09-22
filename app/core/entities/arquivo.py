class Arquivo:
    def __init__(self, localizacao: str):
        self.localizacao = localizacao
        self.nome = localizacao.split('/')[-1]  # Ajuste conforme necessário
        self.extensao = self.nome.split('.')[-1]

    def ler_conteudo(self) -> str:
        # Implementação para ler o conteúdo do arquivo
        pass

    def obter_tamanho(self) -> int:
        # Implementação para retornar o tamanho do arquivo
        pass

    def is_html(self) -> bool:
        return self.extensao.lower() == 'html'

    def raspar_dados(self) -> dict:
        # Implementação para raspar dados se o arquivo for HTML
        pass
