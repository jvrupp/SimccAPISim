from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
# Create your views here.
from .serializers import BuscaSerializer,InsereSerializer
from .models import Pessoas
import jellyfish
from rest_framework.response import Response
import nltk
from nltk.metrics import jaccard_distance
import pandas as pd
from sklearn.cluster import KMeans


def split_match_aprox(nomes,inputs):
  nomes_match=[]
  #separa matchde aproximacoes
  for nom in nomes:
    nome_dividido=nom.split()
    tam_total=len(nome_dividido)
    interseccao = set(inputs.split()).intersection(nome_dividido)
    tam_intersec=len(interseccao)
    rel_match=tam_intersec/tam_total
    if rel_match > 0 :
      nomes_match.append(nom)
    else:
      #bucar a diferenca Universal - B Ex:[1,2,3,4,5] - [1,4] ==> [2,3,5]
      pass
  diferenca = set(nomes).difference(set(nomes_match))
  return (diferenca , nomes_match)

class InsereModelView(ModelViewSet):
    queryset = Pessoas.objects.all()
    serializer_class = InsereSerializer


class BuscaModelView(ModelViewSet):
    queryset = Pessoas.objects.all()
    serializer_class = BuscaSerializer
    http_method_names=['post']

    def create(self, request, *args, **kwargs):
        buscaSerial=BuscaSerializer(data=request.POST)
        if buscaSerial.is_valid():
            nomes = list(Pessoas.objects.all().values_list('nome',flat=True))
            entrada_nome = buscaSerial.data['nome']
            saidas=[]
            for i in list(split_match_aprox(nomes,entrada_nome)[0]):
                similaridade = 1 - jaccard_distance(set(entrada_nome), set(i))
                saidas.append([similaridade,1])
            km=KMeans(n_clusters=4,n_init=20)
            km.fit(saidas)
            saidas = pd.DataFrame(saidas)
            saidas['grupo']=km.labels_
            saidas['nomes']=list(split_match_aprox(nomes,entrada_nome)[0])
            idxmax=saidas.groupby('grupo')[0].mean().idxmax()
            resultado = saidas[saidas['grupo']==idxmax].sort_values(by=0,ascending=False)
            result_final = split_match_aprox(nomes,entrada_nome)[1]
            return Response({"MSG":result_final + list(resultado['nomes'])})
        else:
            return Response({"MSG":"NADA OK"})




#somente match 
#semlhanca

