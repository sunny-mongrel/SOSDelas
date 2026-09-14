from django.contrib.auth.models import AbstractUser
from django.db import models


# Modelo que representa as usuárias cadastradas no sistema.
# O AbstractUser já fornece recursos de autenticação do Django,
# como username, senha, permissões e outros campos.
class Usuario(AbstractUser):
    # Nome da usuária que será exibido no sistema.
    nome = models.CharField(max_length=150)

    # E-mail da usuária. O unique=True impede que dois cadastros
    # utilizem o mesmo endereço de e-mail.
    email = models.EmailField(unique=True)

    # Define como a usuária será representada quando o objeto
    # for exibido no Django.
    def __str__(self):
        return self.nome or self.username


# Modelo que representa os conteúdos publicados no site.
class Conteudo(models.Model):
    # Título do conteúdo.
    titulo = models.CharField(max_length=200)

    # Texto principal do conteúdo.
    texto = models.TextField()

    # Data e hora em que o conteúdo foi criado.
    # auto_now_add=True preenche esse campo automaticamente.
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Nome do modelo no singular dentro do Django Admin.
        verbose_name = "Conteúdo"

        # Nome do modelo no plural dentro do Django Admin.
        verbose_name_plural = "Conteúdos"

        # Exibe os conteúdos do mais recente para o mais antigo.
        ordering = ["-data_criacao"]

    # Define como o conteúdo será representado quando for exibido.
    def __str__(self):
        return self.titulo


# Modelo que representa os comentários feitos pelas usuárias.
class Comentario(models.Model):

    # Relaciona o comentário à usuária que o escreveu.
    # Uma usuária pode ter vários comentários.
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="comentarios",
    )

    # Relaciona o comentário ao conteúdo comentado.
    # Um conteúdo pode receber vários comentários.
    conteudo = models.ForeignKey(
        Conteudo,
        on_delete=models.CASCADE,
        related_name="comentarios",
    )

    # Texto escrito pela usuária no comentário.
    texto = models.TextField()

    # Data e hora em que o comentário foi criado.
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Nome do modelo no singular dentro do Django Admin.
        verbose_name = "Comentário"

        # Nome do modelo no plural dentro do Django Admin.
        verbose_name_plural = "Comentários"

        # Mostra os comentários mais recentes primeiro.
        ordering = ["-data_criacao"]

    # Define como o comentário será representado quando exibido.
    def __str__(self):
        return f"Comentário de {self.usuario} em {self.conteudo}"


# Modelo que representa uma solicitação de apoio enviada pela usuária.
class SolicitacaoApoio(models.Model):

    # Define os possíveis estados de uma solicitação.
    class Status(models.TextChoices):
        PENDENTE = "PENDENTE", "Pendente"
        EM_ANALISE = "EM_ANALISE", "Em análise"
        RESPONDIDA = "RESPONDIDA", "Respondida"
        ENCERRADA = "ENCERRADA", "Encerrada"

    # Relaciona a solicitação à usuária que a enviou.
    # Uma usuária pode realizar várias solicitações.
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="solicitacoes_apoio",
    )

    # Mensagem escrita pela usuária na solicitação.
    texto = models.TextField()

    # Data e hora em que a solicitação foi criada.
    data_solicitacao = models.DateTimeField(auto_now_add=True)

    # Armazena o status atual da solicitação.
    # O status inicial é "Pendente".
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDENTE,
    )

    class Meta:
        # Nome do modelo no singular dentro do Django Admin.
        verbose_name = "Solicitação de apoio"

        # Nome do modelo no plural dentro do Django Admin.
        verbose_name_plural = "Solicitações de apoio"

        # Mostra as solicitações mais recentes primeiro.
        ordering = ["-data_solicitacao"]

    # Define como a solicitação será representada quando exibida.
    def __str__(self):
        return f"Solicitação de {self.usuario} - {self.get_status_display()}"


# Modelo responsável pelas notificações do administrador.
class Notificacao(models.Model):

    # Relaciona a notificação à solicitação de apoio que a gerou.
    solicitacao_apoio = models.ForeignKey(
        SolicitacaoApoio,
        on_delete=models.CASCADE,
        related_name="notificacoes",
    )

    # Título que será exibido na notificação.
    titulo = models.CharField(max_length=200)

    # Data e hora em que a notificação foi criada.
    data_criacao = models.DateTimeField(auto_now_add=True)

    # Indica se o administrador já visualizou a notificação.
    # Por padrão, uma nova notificação começa como não lida.
    lida = models.BooleanField(default=False)

    class Meta:
        # Nome do modelo no singular dentro do Django Admin.
        verbose_name = "Notificação"

        # Nome do modelo no plural dentro do Django Admin.
        verbose_name_plural = "Notificações"

        # Mostra as notificações mais recentes primeiro.
        ordering = ["-data_criacao"]

    # Define como a notificação será representada quando exibida.
    def __str__(self):
        return self.titulo