from rest_framework import routers, serializers, viewsets, mixins
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout

from ecommerce.models import Grupo
from ecommerce.models import Estadio
from ecommerce.models import Vendedor
from ecommerce.models import CadastroFig
from ecommerce.models import Selecao
from ecommerce.models import Figurinha


#### Figurinha ########################################
class FigurinhaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Figurinha
        fields = [
            'id', 'numero', 'num', 'fotoFig', 'nomeFig', 'jogador', 'lendaria',
            'especial', 'escudo'
        ]


class FigurinhaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Figurinha.objects.all().order_by('numero')
    serializer_class = FigurinhaSerializer

class FigurinhaEstadioViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FigurinhaSerializer
      
    def get_queryset(self):
        queryset = Figurinha.objects.filter(estadio__isnull=False)
        return queryset
    
    
    ######################################################
    
    
    ###### Estadio ########################################
class EstadioSerializer(serializers.ModelSerializer):
    figurinhas = FigurinhaSerializer(many=True, read_only=True)

    class Meta:
        model = Estadio
        fields = ['id', 'nomeEstadio', 'figurinhas']


class EstadioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Estadio.objects.all().order_by('nomeEstadio')
    serializer_class = EstadioSerializer


######################################################


#### Selecao ########################################
class SelecaoSerializer(serializers.ModelSerializer):
    figurinhas = FigurinhaSerializer(many=True, read_only=True)

    class Meta:
        model = Selecao
        fields = ['id', 'pais', 'fotoBandeira', 'fotoTime', 'figurinhas']


class SelecaoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Selecao.objects.all().order_by('pais')
    serializer_class = SelecaoSerializer


######################################################


#### Grupos ########################################
class GrupoSerializer(serializers.ModelSerializer):
    selecoes = SelecaoSerializer(many=True, read_only=True)

    class Meta:
        model = Grupo
        fields = ['id', 'nomeGrupo', 'selecoes']


class GrupoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Grupo.objects.all().order_by('nomeGrupo')
    serializer_class = GrupoSerializer


######################################################


#### Vendedor ########################################
class VendedorSerializer(serializers.ModelSerializer):
    #cadastrofig = CadastroFigSerializer(many=True, read_only=True)

    class Meta:
        model = Vendedor
        fields = [
            'id', 'user', 'email', 'telefone', 'estado', 'cidade'
        ]


class VendedorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Vendedor.objects.all().order_by('user')
    serializer_class = VendedorSerializer


######################################################

  
#### CadastroFig ########################################
class CreateCadastroFigSerializer(serializers.ModelSerializer):
    #figurinha = FigurinhaSerializer()

    class Meta:
        model = CadastroFig
        fields = ['condicao', 'aceitaTroca', 'preco', 'figurinha']
      
class CadastroFigSerializer(serializers.ModelSerializer):
    figurinha = FigurinhaSerializer()
    vendedores = VendedorSerializer()

    class Meta:
        model = CadastroFig
        fields = ['condicao', 'aceitaTroca', 'preco', 'figurinha', 'vendedores']


class CreateCadastroFigViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = CadastroFig.objects.all().order_by('preco')
    serializer_class = CreateCadastroFigSerializer

    def perform_create(self, serializer):
      serializer.save(vendedores = Vendedor.objects.filter(usuario = self.request.user)[0])    

class CadastroFigViewSet(viewsets.ReadOnlyModelViewSet, mixins.DestroyModelMixin):
    serializer_class = CadastroFigSerializer
    permission_classes = [IsAuthenticated]
      
    def get_queryset(self):
      return CadastroFig.objects.filter(vendedores = Vendedor.objects.filter(usuario = self.request.user)[0])  


class CadastroFigFilterViewSet(viewsets.ReadOnlyModelViewSet):
  serializer_class = CadastroFigSerializer
  def get_queryset(self):
    """
    Filtra filme por titulo e ator
    """
    queryset = CadastroFig.objects.all()
    query = {}

    figurinha = self.request.query_params.get('figurinha', None)
    if figurinha is not None:
      query['figurinha'] = figurinha


    print(query)
    queryset = queryset.filter(**query)    
    return queryset  

      

######################################################


class CreateVendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = [
            'id', 'user', 'email', 'telefone', 'estado', 'cidade'
        ]


class CreateVendedorViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = CreateVendedorSerializer
    queryset = Vendedor.objects.all()

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'username',
            'password',
        ]

    @transaction.atomic
    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = self.Meta.model(**validated_data)
        instance.set_password(password)
        instance.save()
        return instance


class UserRegistrationViewSet(mixins.CreateModelMixin,
                              viewsets.GenericViewSet):
    serializer_class = UserRegistrationSerializer


class LoginViewSet(ViewSet):
    @staticmethod
    def create(request: Request) -> Response:
        user = authenticate(username=request.data.get('username'),
                            password=request.data.get('password'))

        if user is not None:
            login(request, user)
            return JsonResponse({"id": user.id, "username": user.username})
        else:
            return JsonResponse(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class VendedorDetailsViewSet(ViewSet):
    serializer_class = VendedorSerializer
    permission_classes = [IsAuthenticated]

    @staticmethod
    def list(request: Request) -> Response:
        usuarios = Vendedor.objects.filter(usuario=request.user)
        usuario = usuarios[0] if usuarios.exists() else None
        serializer = VendedorSerializer(usuario, many=False)
        return Response(serializer.data)


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username')


class UserDetailsViewSet(ViewSet):
    serializer_class = UserDetailsSerializer
    permission_classes = [IsAuthenticated]

    @staticmethod
    def list(request: Request) -> Response:
        serializer = UserDetailsSerializer(request.user, many=False)
        return Response(serializer.data)


class LogoutViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def list(request: Request) -> Response:
        logout(request)
        content = {'logout': 1}
        return Response(content)


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'grupos', GrupoViewSet)
router.register(r'selecoes', SelecaoViewSet)
router.register(r'vendedores', VendedorViewSet)
router.register(r'figurinhas', FigurinhaViewSet)
#router.register(r'cadastrofigs', CadastroFigViewSet)
router.register(r'estadios', EstadioViewSet)
router.register(r'figurinhas-estadio', FigurinhaEstadioViewSet, basename="FigurinhaEstadio")
router.register(r'cadastro-fig-create', CreateCadastroFigViewSet, basename = "cadastrofigcreate")
router.register(r'cadastro-fig', CadastroFigViewSet, basename = "cadastrofig")
router.register(r'cadastro-fig-filter', CadastroFigFilterViewSet, basename = "cadastrofigfilter")



#Rotas de autenticação
router.register(r'currentuser', VendedorDetailsViewSet, basename="Currentuser")
router.register(r'currentusuario',
                VendedorDetailsViewSet,
                basename="Currentusuario")
router.register(r'login', LoginViewSet, basename="Login")
router.register(r'logout', LogoutViewSet, basename="Logout")
router.register(r'user-registration', UserRegistrationViewSet, basename="User")
router.register(r'usuarios-create', CreateVendedorViewSet)
