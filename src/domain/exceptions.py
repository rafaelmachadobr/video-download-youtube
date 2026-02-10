"""
Exceções customizadas do domínio.
Seguindo Clean Architecture, exceções de domínio não devem depender
de detalhes de implementação (frameworks, bibliotecas externas).
"""


class DomainException(Exception):
    """Exceção base para todas as exceções do domínio."""

    pass


class InvalidURLException(DomainException):
    """Levantada quando a URL fornecida é inválida."""

    def __init__(self, url: str, message: str = "URL inválida"):
        self.url = url
        super().__init__(f"{message}: {url}")


class DownloadFailedException(DomainException):
    """Levantada quando o download do vídeo falha."""

    def __init__(self, url: str, reason: str = "Erro desconhecido"):
        self.url = url
        self.reason = reason
        super().__init__(f"Falha ao baixar vídeo de {url}: {reason}")


class VideoNotSavedException(DomainException):
    """Levantada quando falha ao salvar o vídeo no repositório."""

    def __init__(self, reason: str = "Erro ao salvar no banco de dados"):
        super().__init__(reason)
