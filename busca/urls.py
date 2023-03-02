from rest_framework.routers import SimpleRouter
from .views import BuscaModelView,InsereModelView
routerBusca = SimpleRouter()

routerBusca.register('busca',BuscaModelView,basename="busca")
routerBusca.register('insere',InsereModelView,basename="insere")