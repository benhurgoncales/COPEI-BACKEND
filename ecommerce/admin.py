from django.contrib import admin

# Register your models here.
from .models import Figurinha
from .models import Selecao
from .models import Estadio
from .models import Vendedor
from .models import CadastroFig
from .models import Grupo

admin.site.register(Figurinha)
admin.site.register(Selecao)
admin.site.register(Estadio)
admin.site.register(Vendedor)
admin.site.register(CadastroFig)
admin.site.register(Grupo)
