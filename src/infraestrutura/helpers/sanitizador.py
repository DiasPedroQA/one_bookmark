"""
Este módulo fornece funções para sanitização de texto.

O principal objetivo é remover caracteres problemáticos de Unicode,
mantendo acentos e outros caracteres válidos. Isso é útil para
limpar dados de entrada antes de processá-los ou armazená-los.

Funções:
    sanitizar_texto(texto: str) -> str: Remove caracteres Unicode problemáticos,
    mantendo acentos e retornando uma string limpa.
"""

import unicodedata
import re


def sanitizar_texto(texto: str) -> str:
    """Remove caracteres problemáticos de Unicode, mas mantém acentos.

    Args:
        texto: O texto que precisa ser sanitizado.

    Returns:
        O texto sanitizado, com acentos mantidos e caracteres Unicode inválidos removidos.
    """
    if not isinstance(texto, str):
        return texto  # Se não for uma string, retorne o valor original

    # Normalize o texto para decompor caracteres problemáticos
    texto_normalizado = unicodedata.normalize('NFKC', texto)
    # NFKC mantém a compatibilidade

    # Remover caracteres de controle (não imprimíveis ou invisíveis)
    texto_sanitizado = re.sub(r'[\u0000-\u001F\u007F-\u009F]', '', texto_normalizado)

    return texto_sanitizado
