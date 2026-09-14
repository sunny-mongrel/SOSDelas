from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    class TipoUsuario(models.TextChoices):
        USUARIA = "USUARIA", "Usuária comum"
        ADMINISTRADOR = "ADMINISTRADOR", "Administrador"

    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    tipo_usuario = models.CharField(
        max_length=15,
        choices=TipoUsuario.choices,
        default=TipoUsuario.USUARIA,
    )

    def __str__(self):
        return self.nome or self.username


class Conteudo(models.Model):
    titulo = models.CharField(max_length=200)
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Conteúdo"
        verbose_name_plural = "Conteúdos"
        ordering = ["-data_criacao"]

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="comentarios",
    )
    conteudo = models.ForeignKey(
        Conteudo,
        on_delete=models.CASCADE,
        related_name="comentarios",
    )
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Comentário"
        verbose_name_plural = "Comentários"
        ordering = ["-data_criacao"]

    def __str__(self):
        return f"Comentário de {self.usuario} em {self.conteudo}"


class SolicitacaoApoio(models.Model):
    class Status(models.TextChoices):
        PENDENTE = "PENDENTE", "Pendente"
        EM_ANALISE = "EM_ANALISE", "Em análise"
        RESPONDIDA = "RESPONDIDA", "Respondida"
        ENCERRADA = "ENCERRADA", "Encerrada"

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="solicitacoes_apoio",
    )
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDENTE,
    )

    class Meta:
        verbose_name = "Solicitação de apoio"
        verbose_name_plural = "Solicitações de apoio"
        ordering = ["-data_solicitacao"]

    def __str__(self):
        return f"Solicitação de {self.usuario} - {self.get_status_display()}"


class Notificacao(models.Model):
    solicitacao_apoio = models.ForeignKey(
        SolicitacaoApoio,
        on_delete=models.CASCADE,
        related_name="notificacoes",
    )
    titulo = models.CharField(max_length=200)
    data_criacao = models.DateTimeField(auto_now_add=True)
    lida = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"
        ordering = ["-data_criacao"]

    def __str__(self):
        return self.titulo