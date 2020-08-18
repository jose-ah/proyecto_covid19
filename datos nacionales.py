# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 14:48:02 2020

@author: josea
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import textwrap as tw


#importar  informacion
datos_totales=pd.read_csv("https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto5/TotalesNacionales_T.csv")
datos_casos_genero_edad=pd.read_csv("https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto16/CasosGeneroEtario_T.csv")
datos_fallecidos_edad= pd.read_csv("https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto10/FallecidosEtario_T.csv")
archivo_acciones = pd.read_excel('D:/Universidad/Electivos Comunes/Big Data/Proyecto covid/acciones - copia.xlsx')
PCR=pd.read_csv("https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto7/PCR_T.csv")
archivo_acciones=archivo_acciones.dropna()
PCR=PCR.fillna(0)

#lista de Fechas en la que ocurrio algun ACONTECIMIENTO
Fechas=archivo_acciones["Fecha"]
Fechas_hitos=[]
pd.to_datetime(Fechas)
for x in Fechas:
    Fechas_hitos.append(datetime.strftime(pd.to_datetime(x),'%d-%m'))


#lista de TODAS las fechas
fechas=datos_totales["Fecha"]
FECHAS=[]
pd.to_datetime(fechas)
for x in fechas:
    FECHAS.append(datetime.strftime(pd.to_datetime(x),'%d-%m'))


fallecidos_39=datos_fallecidos_edad["<=39"]
fallecidos_49=datos_fallecidos_edad["40-49"]
fallecidos_59=datos_fallecidos_edad["50-59"]
fallecidos_69=datos_fallecidos_edad["60-69"]
fallecidos_79=datos_fallecidos_edad["70-79"]
fallecidos_89=datos_fallecidos_edad["80-89"]
fallecidos_90=datos_fallecidos_edad[">=90"]


sintomaticos=datos_totales["Casos nuevos con sintomas"]
asintomaticos=datos_totales["Casos nuevos sin sintomas"]
asintomaticos=asintomaticos.fillna(0)
contagios_totales=asintomaticos+sintomaticos
max_value=contagios_totales.values.max()+1000

width = 0.5    # the width of the bars: can also be len(x) sequence
fig, ax = plt.subplots(figsize=(30, 25))

ax.bar(FECHAS, asintomaticos, width, label='Asymptomatic')
ax.bar(FECHAS, sintomaticos, width, bottom=asintomaticos, label='Symptomatic')

plt.xticks(range(0,len(FECHAS),3),rotation=90, fontsize='x-large')
plt.yticks(range(0,int(max_value), 500),fontsize='x-large')

ax.minorticks_on()
ax.set_ylabel('Infected', fontsize='xx-large')
ax.set_xlabel("Date", fontsize='xx-large')
plt.title('Daily cases of infection', fontsize='xx-large')
   
cont=0
bbox = dict(boxstyle="round", fc="0.8")            
while cont<len(Fechas_hitos):
    aux4=Fechas_hitos[cont]
    aux=FECHAS.index(aux4)
    aux2=sintomaticos[aux]+asintomaticos[aux] #posicion eje y
    texstr=archivo_acciones["Hito"][aux] #texto de anotacion
    box_annot=tw.fill(tw.dedent(texstr.rstrip()), width=45) #texto en casilla
    if cont<6:
        sep=-180+380*(cont+1)
        ax.annotate(box_annot, xy=(aux4, aux2),bbox=bbox, xytext=(aux4,(aux2+sep)), xycoords='data', size=15)
        ax.arrow(aux4,aux2+sep,0, -sep, width=0.15, head_width=0.4, head_length=1.2)
    
    
    elif cont<8:
        sep=-500+450*(cont+1)
        ax.annotate(box_annot, xy=(aux4, aux2),bbox=bbox, xytext=(aux4,(aux2+sep)), xycoords='data', size=15)
        ax.arrow(aux4,aux2+sep,0, -sep, width=0.15, head_width=0.4, head_length=1.2)
    elif cont<17:
        sep=-1200+450*(cont+1)
        ax.annotate(box_annot, xy=(aux4, aux2),bbox=bbox, xytext=(aux4,(aux2+sep)), xycoords='data', size=15)
        ax.arrow(aux4,aux2+sep,0, -sep, width=0.15, head_width=0.4, head_length=1.2)  
    
    elif cont<21:
        sep=400
        ax.annotate(box_annot, xy=(aux4, aux2),bbox=bbox, xytext=(aux4,(aux2+sep)), xycoords='data', size=15)
        ax.arrow(aux4,aux2+sep,0, -sep, width=0.15, head_width=0.4, head_length=1.2) 
   
    else:
        sep=-1600+90*(cont)
        ax.annotate(box_annot, xy=(aux4, aux2),bbox=bbox, xytext=(aux4,(aux2+sep)), xycoords='data', size=15)
        ax.arrow(aux4,aux2+sep,0, -sep, width=0.15, head_width=0.4, head_length=1.2)
    cont=cont+1
    
plt.grid(True, which="major")
ax.legend(loc=2, fontsize="xx-large")
plt.show()

###############EXAMENES PCR DiARIos###################

#Fechas examenes PCR
Fechas=PCR["Region"][2:]
Fechas_PCR=[]
pd.to_datetime(Fechas)
for x in Fechas:
    Fechas_PCR.append(datetime.strftime(pd.to_datetime(x),'%d-%m'))
    
series=PCR.keys()[1:] 
PCR_total=pd.DataFrame()   
PCR_total["PCR"]=PCR.sum(axis=1)
max_value=(PCR_total[2:]).values.max()+1000

fig, ax = plt.subplots(figsize=(20,15))
ax.plot(Fechas_PCR, PCR_total["PCR"][2:], linestyle="-", label="Total PCR's")
ax.set_ylabel('Test', fontsize='x-large')
ax.set_xlabel("Date", fontsize='x-large')
plt.title('Quantity of PCR tests done daily', fontsize='xx-large')

ax.grid(True)
plt.xticks(range(0,len(Fechas_PCR),3),rotation=90, fontsize='large')   
plt.yticks(range(0, int(max_value),1000),fontsize='large')
ax.legend(fontsize='large')
plt.grid(True, which="minor")
plt.show()


#Recuperados totales

Recuperados=[]
confirmados_recup= datos_totales["Casos confirmados recuperados"]
recup_FD=datos_totales["Casos recuperados por FD"]
recup_FIS=datos_totales["Casos recuperados por FIS"]
Recuperados[0:92]=recup_FD[0:92]
Recuperados[92:111]=recup_FIS[92:111]
Recuperados[111:len(confirmados_recup)]=confirmados_recup[111:]

fig, ax = plt.subplots(figsize=(15,10))
plt.bar(FECHAS, Recuperados, width, label='Recovered')
plt.xticks(range(0,len(FECHAS),7),rotation=90)
plt.ylabel('Recovered', fontsize="x-large")
ax.set_xlabel("Date", fontsize='x-large')
plt.title('Recovered cases', fontsize="xx-large")
plt.grid(True)
plt.legend(loc=2)
plt.show()


#Fallecidos por edad
fechas_fallecidos=FECHAS[(FECHAS.index("09-04")):len(FECHAS)]
fig, ax = plt.subplots(figsize=(20,15))
ax.bar(fechas_fallecidos, fallecidos_39, width, label='<=39 years')
ax.bar(fechas_fallecidos, fallecidos_49, width, bottom=fallecidos_39, label='40-49 years')
ax.bar(fechas_fallecidos, fallecidos_59, width, bottom=fallecidos_49, label='50-59 years')
ax.bar(fechas_fallecidos, fallecidos_69, width, bottom=fallecidos_59, label='60-69 years')
ax.bar(fechas_fallecidos, fallecidos_79, width, bottom=fallecidos_69, label='70-79 years')
ax.bar(fechas_fallecidos, fallecidos_89, width, bottom=fallecidos_79, label='80-89 years')
ax.bar(fechas_fallecidos, fallecidos_90, width, bottom=fallecidos_89, label='>=90 years')
plt.xticks(range(0,len(FECHAS),5),rotation=90, size="x-large")
ax.set_ylabel('Deaths', fontsize="x-large")
ax.set_xlabel('Date', fontsize="x-large")
ax.set_title('Cases of deaths by age range', fontsize="xx-large")
ax.legend(loc=2, fontsize="x-large") 
plt.grid(True)
plt.yticks(range(0, 6000,500))
plt.show()



###################################Contagiados por sexo y edad#######################################

def graph_year_range(data, dates, keys, gender):
    lines=['--', '-.', '-', ':']
    max_value=data.values.max()+1000
    fig, ax = plt.subplots(figsize=(20,15))
    aux=0
    while aux<len(keys):
        ax.plot(dates, data[keys[aux]], linestyle=lines[aux%4], label=keys[aux])
        aux=aux+1
    
    if gender=="F":
        ax.set_ylabel('Female cases', fontsize='x-large')
        ax.set_xlabel("Date", fontsize='x-large')
        plt.title('Evolution of female infected by age range', fontsize='xx-large')
    elif gender=="M":
        ax.set_ylabel('Male cases', fontsize='x-large')
        ax.set_xlabel("Date", fontsize='x-large')
        plt.title('Evolution of male infected by age range', fontsize='xx-large')
    elif gender=="FM":
         ax.set_ylabel('Total cases', fontsize='x-large')
         ax.set_xlabel("Date", fontsize='x-large')
         plt.title('Evolution of infected by age range', fontsize='xx-large')
    
    ax.grid(True)
    plt.xticks(range(0,len(dates),2),rotation=90, fontsize='large')   
    if gender=="FM":
        plt.yticks(range(0, max_value,1000),fontsize='large')
    else:
        plt.yticks(range(0, max_value,500),fontsize='large')

    ax.legend(fontsize='x-large')
    plt.grid(True, which="minor")
    plt.show()
    return fig

rangos_eng=['00 - 04 years', '05 - 09 years', '10 - 14 years',
            '15 - 19 years', '20 - 24 years', '25 - 29 years', '30 - 34 years',
            '35 - 39 years', '40 - 44 years', '45 - 49 years', '50 - 54 years',
            '55 - 59 years', '60 - 64 years', '65 - 69 years', '70 - 74 years',
            '75 - 79 years', '80 and more years']
rangos_masc=['00 - 04 años', '05 - 09 años', '10 - 14 años',
             '15 - 19 años', '20 - 24 años', '25 - 29 años', '30 - 34 años',
             '35 - 39 años', '40 - 44 años', '45 - 49 años', '50 - 54 años',
             '55 - 59 años', '60 - 64 años', '65 - 69 años', '70 - 74 años',
             '75 - 79 años', '80 y más años'] 
rangos_fem=['00 - 04 años.1', '05 - 09 años.1','10 - 14 años.1', '15 - 19 años.1',
            '20 - 24 años.1', '25 - 29 años.1','30 - 34 años.1', '35 - 39 años.1',
            '40 - 44 años.1', '45 - 49 años.1','50 - 54 años.1', '55 - 59 años.1',
            '60 - 64 años.1', '65 - 69 años.1','70 - 74 años.1', '75 - 79 años.1',
            '80 y más años.1']      



#Infections of BOTH genders by age range
both_gender_infections=pd.DataFrame()
aux=0
while aux<len(rangos_eng):
    both_gender_infections[rangos_eng[aux]]=pd.to_numeric(datos_casos_genero_edad[rangos_fem[aux]][1:])+pd.to_numeric(datos_casos_genero_edad[rangos_masc[aux]][1:])
    aux=aux+1

#male infections by age range
male_infections=pd.DataFrame()
aux=0
while aux<len(rangos_eng):
    male_infections[rangos_eng[aux]]=pd.to_numeric(datos_casos_genero_edad[rangos_masc[aux]][1:])
    aux=aux+1  

#female infections by age range 
female_infections=pd.DataFrame()
aux=0
while aux<len(rangos_eng):
    female_infections[rangos_eng[aux]]=pd.to_numeric(datos_casos_genero_edad[rangos_fem[aux]][1:])
    aux=aux+1  



fechas_genero_edad=datos_casos_genero_edad["Grupo de edad"][1:len(datos_casos_genero_edad["Grupo de edad"])]
FECHAS_genero_edad=[]
pd.to_datetime(fechas_genero_edad)
for x in fechas_genero_edad:
    FECHAS_genero_edad.append(datetime.strftime(pd.to_datetime(x),'%d-%m'))


graph_year_range(male_infections,FECHAS_genero_edad,rangos_eng,"M")
graph_year_range(female_infections,FECHAS_genero_edad,rangos_eng,"F")
graph_year_range(both_gender_infections,FECHAS_genero_edad,rangos_eng,"FM")


###########Graficos de barra por edad######    
    
def create_bar_per_age(FECHAS_genero_edad, datos_casos_genero_edad, pos_edad):
    rangos_masc=['00 - 04 años', '05 - 09 años', '10 - 14 años',
      '15 - 19 años', '20 - 24 años', '25 - 29 años', '30 - 34 años',
       '35 - 39 años', '40 - 44 años', '45 - 49 años', '50 - 54 años',
       '55 - 59 años', '60 - 64 años', '65 - 69 años', '70 - 74 años',
       '75 - 79 años', '80 y más años'] 
    rangos_fem=['00 - 04 años.1', '05 - 09 años.1','10 - 14 años.1', '15 - 19 años.1',
    '20 - 24 años.1', '25 - 29 años.1','30 - 34 años.1', '35 - 39 años.1',
    '40 - 44 años.1', '45 - 49 años.1','50 - 54 años.1', '55 - 59 años.1',
    '60 - 64 años.1', '65 - 69 años.1','70 - 74 años.1', '75 - 79 años.1',
    '80 y más años.1']
    x = np.arange(0,len(FECHAS_genero_edad),2)  # posicion de las fechas
    x2 = np.arange(len(FECHAS_genero_edad))  # posicion de los datos
    width = 0.35  # the width of the bars
    fig, ax = plt.subplots(figsize=(20,10))
    series_m=rangos_masc[pos_edad]
    series_f=rangos_fem[pos_edad]
    ax.bar(x2 - width/2, pd.to_numeric(datos_casos_genero_edad[series_m][1:len(datos_casos_genero_edad)]), width, label='Men')
    ax.bar(x2 + width/2, pd.to_numeric(datos_casos_genero_edad[series_f][1:len(datos_casos_genero_edad)]), width, label='Women')
    ax.set_ylabel('Casos nuevos')
    ax.set_xlabel("Fecha")
    ax.set_title(rangos_masc[pos_edad])
    ax.grid(True)
    ax.set_xticks(x)
    ax.set_xticklabels(FECHAS_genero_edad, rotation=90)
    ax.legend(fontsize=16)
    return fig 




#######################################GRAFICOS POR EDAD Y GENERO##########################
# fig, axs=plt.subplots(17);
# aux=0
# axs[aux]=create_bar_per_age(FECHAS_genero_edad, datos_casos_genero_edad,aux)
# aux=aux+1
# axs[aux]=create_bar_per_age(FECHAS_genero_edad, datos_casos_genero_edad,aux)
# aux=aux+1
# axs[aux]=create_bar_per_age(FECHAS_genero_edad, datos_casos_genero_edad,aux)
# aux=aux+1
# axs[aux]=create_bar_per_age(FECHAS_genero_edad, datos_casos_genero_edad,aux)
# aux=aux+1
# axs[aux]=create_bar_per_age(FECHAS_genero_edad, datos_casos_genero_edad,aux)
# aux=aux+1
# axs[aux]=create_bar_per_age(FECHAS_genero_edad, datos_casos_genero_edad,aux)
# aux=aux+1
# axs[aux]=create_bar_per_age(FECHAS_genero_edad, datos_casos_genero_edad,aux)
# aux=aux+1
# axs[aux]=create_bar_per_age(FECHAS_genero_edad, datos_casos_genero_edad,aux)
# aux=aux+1
# axs[aux]=create_bar_per_age(FECHAS_genero_edad, datos_casos_genero_edad,aux)
# aux=aux+1
# axs[aux]=create_bar_per_age(FECHAS_genero_edad, datos_casos_genero_edad,aux)
# aux=aux+1
# axs[aux]=create_bar_per_age(FECHAS_genero_edad, datos_casos_genero_edad,aux)
# aux=aux+1
# axs[aux]=create_bar_per_age(FECHAS_genero_edad, datos_casos_genero_edad,aux)
# aux=aux+1
# axs[aux]=create_bar_per_age(FECHAS_genero_edad, datos_casos_genero_edad,aux)
# aux=aux+1
# axs[aux]=create_bar_per_age(FECHAS_genero_edad, datos_casos_genero_edad,aux)
# aux=aux+1
# axs[aux]=create_bar_per_age(FECHAS_genero_edad, datos_casos_genero_edad,aux)
# aux=aux+1
# axs[aux]=create_bar_per_age(FECHAS_genero_edad, datos_casos_genero_edad,aux)
# aux=aux+1
# axs[aux]=create_bar_per_age(FECHAS_genero_edad, datos_casos_genero_edad,aux)
# aux=aux+1
# plt.show()

#############################################################################################




