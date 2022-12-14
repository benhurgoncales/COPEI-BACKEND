from django.db import models
from django.contrib.auth import get_user_model 

User = get_user_model()

class Figurinha(models.Model):
  numero = models.CharField("Codigo Figurinha", max_length=20,null= True)
  num = models.IntegerField("Numero ", null= True)
  nomeFig = models.CharField("Nome da figurinha",max_length=100)
  lendaria = models.BooleanField(null=True)
  especial = models.BooleanField(null=True)
  jogador = models.BooleanField(null=True)
  escudo = models.BooleanField(null=True)
  estadio = models.ForeignKey('Estadio', on_delete=models.PROTECT, verbose_name="Estadio", blank=True,null=True)
  selecao = models.ForeignKey('Selecao', on_delete=models.PROTECT, verbose_name="Seleção", blank=True, null=True)
  fotoFig = models.ImageField(upload_to='filmes', max_length=255)

  def __str__(self):
      return f"{self.numero} - {self.nomeFig}"
  class Meta:
      verbose_name = "Figurinha"
      verbose_name_plural = "Figurinhas"

class Selecao(models.Model):
  pais = models.CharField("Insira o pais",max_length=50)
  fotoBandeira = models.ImageField(upload_to='fotos', max_length=255, null=True)
  fotoTime = models.ImageField(upload_to='fotos', max_length=255, null=True)
  grupo = models.ForeignKey('Grupo', on_delete=models.PROTECT, verbose_name="Grupo")

  def __str__(self):
      return f"{self.pais}"
  class Meta:
      verbose_name = "Seleção"
      verbose_name_plural = "Seleçoes"

  @property
  def figurinhas(self):
    return Figurinha.objects.filter(selecao=self)       

class Grupo(models.Model):
  nomeGrupo = models.CharField("Nome do Grupo", max_length=1)

  def __str__(self):
      return f"{self.nomeGrupo}"
  class Meta:
      verbose_name = "Grupo"
      verbose_name_plural = "Grupos"

  @property
  def selecoes(self):
    return Selecao.objects.filter(grupo=self)   

class Estadio(models.Model):
  nomeEstadio = models.CharField("Nome do Estadio", max_length=30)


  def __str__(self):
      return f"{self.nomeEstadio}"
  class Meta:
      verbose_name = "Estadio"
      verbose_name_plural = "Estadios"

  @property
  def figurinhas(self):
    return Figurinha.objects.filter(estadio=self)  

class Vendedor(models.Model):
  fotoUsuario = models.ImageField(upload_to='filmes', max_length=255, null=True)
  user = models.CharField(max_length=50)
  email = models.EmailField(max_length=50)
  telefone = models.CharField(max_length=15)
  estado = models.CharField(max_length=30)
  cidade = models.CharField(max_length=30)
  figcadastrada = models.ManyToManyField("CadastroFig", verbose_name="Figurinhas Cadastradas")
  usuario = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Usuario Logado", null=True)
  

  def __str__(self):
      return f"{self.user} - {self.figcadastrada}"
  class Meta:
      verbose_name = "Vendedor"
      verbose_name_plural = "Vendedores"

class CadastroFig(models.Model):
  condicao = models.CharField(max_length=50)
  aceitaTroca = models.BooleanField(null=True)
  preco = models.DecimalField(max_digits= 6, decimal_places=2)
  figurinha = models.ForeignKey("Figurinha", on_delete=models.PROTECT, verbose_name="Figurinha",null=True)
  vendedores = models.ForeignKey("Vendedor", on_delete=models.PROTECT, verbose_name="Vendedor",null=True)

  def __str__(self):
      return f"{self.figurinha} - {self.preco}"
  class Meta:
      verbose_name = "Cadastro Figurinha"
      verbose_name_plural = "Cadastros das Figurinhas"
