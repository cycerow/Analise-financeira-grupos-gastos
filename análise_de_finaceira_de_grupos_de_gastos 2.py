# -*- coding: utf-8 -*-
"""Análise de finaceira de grupos de gastos.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nzRL7xLK84_gG7fTkvilTK3jdHDNrP1J

#**Análise de cluster método K-means**

##**Passo 1_Obter dados**

**Base de dados cartão de crédito - 1 atributo**

* **Fonte**:https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients
"""



import pandas as pd
import plotly.express as px
import plotly.graph_objects as go #concatenar gráficos
import numpy as np
from sklearn.preprocessing import StandardScaler #para padronização dos dados
#importar base de dados de idade
from sklearn.cluster import KMeans

base_cartao = pd.read_excel('/content/default of credit card clients.xls', header = 1)
base_cartao

#criar variavel(coluna) de soma Total
base_cartao['BILL_TOTAL'] = base_cartao['BILL_AMT1'] + base_cartao['BILL_AMT2'] + base_cartao['BILL_AMT3'] + base_cartao['BILL_AMT4'] + base_cartao['BILL_AMT5'] + base_cartao['BILL_AMT6']

base_cartao

#Criar base x_cartao
X_cartao = base_cartao.iloc[:,[1,25]].values
X_cartao

X_cartao.shape

X_cartao.info

"""##**Passo 2_Padronizar Base**"""

# Padronização dos dados pela função ".fit_tranform"
scaler_cartao = StandardScaler()
X_cartao = scaler_cartao.fit_transform(X_cartao)

X_cartao

"""##**Passo 3_Inicializar os centroides através do *Within-Clusters Sum-of-Squares***"""

# within-clusters sum-of-squares (Soma dos quadrados)
wcss = [] #criar uma variavel
for i in range(1, 11):
 #print(i)
 #gerar um agrupamento com os 11 clusters
 kmeans_cartao = KMeans(n_clusters=i, random_state=0) #radom_state para sempre ter os mesmos resutados
 kmeans_cartao.fit(X_cartao) #treinamento
 wcss.append(kmeans_cartao.inertia_) #colocar dentro de uma lista de resultados

wcss

"""##**Passo 4_ Definir número de cluster**"""

#Análise Método Elbow
grafico = px.line(x = range(1,11), y = wcss)
grafico.show()

"""Fazendo análise do gráfico através do método Elbow é possível observar o decaimento da função da soma dos quadrados a partir de 3 e 4 clusters, logo o número otimo de clusters é 4.

Obs: eixo y = wcss - soma dos quadrados da amostra.  x = nº de clusters [1, 11]

##**Passo 5_Agrupamento dos dados**
"""

kmeans_cartao = KMeans(n_clusters=4, random_state=0)
# A função "fit_predict" faz o treinamento e obtem os resultados
rotulos = kmeans_cartao.fit_predict(X_cartao)

#gráfico
grafico = px.scatter(x = X_cartao[:,0], y = X_cartao[:,1], color=rotulos)
grafico.show()

"""##**Passo 6_Análise**

x = Representa representa limite <br>
y = Gastos (BILL AMT)

* O grupo azul é o grupo zero: São as pessoas que possui limite do cartão de crédito e gastos baixos, são mais conservadores, gastam pouco.

* O grupo rosa é grupo 1: São pessoas que provavelmente possuem limite do cartão de credito alto enão utilizam.

* Grupo amarelo é o grupo 2: são as pessoas entre os grupos 0 e 1 onde possuem um gasto mais elevado, porém parte tem baixo limite e parte tem bom limite.

* Grupo Laranja 3: Pessoas com limite de cartão de credito elevado e bom gasto

* Existe um ponto fora da curva, onde uma pessoa possui alto limite e gastos elevados em comparação aos demais.
"""

# Para enviar para uma lista de cliente por grupo
# A função "np.column_stack" uni as duas listas base_cartao + rotulos
lista_cliente = np.column_stack((base_cartao, rotulos))
lista_cliente

# Ordenar os dados
lista_cliente = lista_cliente[lista_cliente[:,26].argsort()]
lista_cliente

"""##**Outros: Base de dados cartão de crédito - mais atributos**

"""

X_cartao_mais = base_cartao.iloc[:,[1,2,3,4,5,25]].values
X_cartao_mais

# Padronizar os dados
scaler_cartao_mais = StandardScaler()
X_cartao_mais = scaler_cartao.fit_transform(X_cartao_mais)

X_cartao_mais

# Método Elbow
wcss = [] #criar uma variavel
for i in range(1, 11):
 #print(i)
 #gerar um agrupamento com os 11 clusters
 kmeans_cartao_mais = KMeans(n_clusters=i, random_state=0) #radom_state para sempre ter os mesmos resutados
 kmeans_cartao_mais.fit(X_cartao_mais) #treinamento
 wcss.append(kmeans_cartao_mais.inertia_) #colocar dentro de uma lista de resultados

grafico = px.line(x = range(1, 11), y = wcss)
grafico.show()

kmeans_cartao_mais = KMeans(n_clusters=4, random_state=0)
rotulos = kmeans_cartao_mais.fit_predict(X_cartao_mais)

rotulos

"""**Aplicar PCA**

A aplicação do PCA sevirá para redução da quantidade de atributos, como foi selecionado 6, precisamos reduzir para 2 atributos x, y para análise de gráfico
"""

from sklearn.decomposition import PCA

pca = PCA(n_components=2)
X_cartao_mais_pca = pca.fit_transform(X_cartao_mais)

X_cartao_mais_pca.shape

X_cartao_mais_pca

grafico = px.scatter(x=X_cartao_mais_pca[:,0], y=X_cartao_mais_pca[:,1], color=rotulos)
grafico.show()