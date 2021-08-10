#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from os import replace
import pandas as pd
import numpy as np
import re




sys = 'IEEE14/'

dfDBAR=pd.read_csv(sys+'DBAR.csv',header=None)
dfDBAR.columns=["de"]
dfDLIN=pd.read_csv(sys+'DLIN.csv',header=None)
dfDLIN.columns=["de","para"]
dfDLIN['Nlin']=list(range(len(dfDLIN["de"])))

dfbase=pd.read_csv(sys+'base.csv')
dfcaso=pd.read_csv(sys+'caso1.csv')
Teste=dfbase['Medidas'].tolist()
lstPf=[]
lstQf=[]
lstPinj=[]
lstQinj=[]
lstV=[]
i=0
for s in Teste:
    if(s.find("P")!=-1):
        if(s.find("-")!=-1):
            lstPf.append(i)
        else:
            lstPinj.append(i)
    elif(s.find("Q")!=-1):
        if(s.find("-")!=-1):
            lstQf.append(i)
        else:
            lstQinj.append(i)
    elif(s.find("V")!=-1):
        lstV.append(i)  
    i=i+1

P_barra=list(map(int,[s.replace("P","") for s in dfbase['Medidas'][lstPinj].tolist()]))
Q_barra=list(map(int,[s.replace("Q","") for s in dfbase['Medidas'][lstQinj].tolist()]))
Pf_barras=[s.replace("P","") for s in dfbase['Medidas'][lstPf].tolist()]
Qf_barras=[s.replace("Q","") for s in dfbase['Medidas'][lstQf].tolist()]
V_barra=list(map(int,[s.replace("V","") for s in dfbase['Medidas'][lstV].tolist()]))

Pf_de_para=[s.split("-") for s in Pf_barras]
Qf_de_para=[s.split("-") for s in Qf_barras]


dfbase["ramo"]=-1*np.ones(len(dfbase)).astype(np.int32)
dfbase["sentido"]=-1*np.ones(len(dfbase)).astype(np.int32)
dfbase["Barra"]=-1*np.ones(len(dfbase)).astype(np.int32)
dfbase["Barra"][lstPinj]=(P_barra-np.ones(len(P_barra))).astype(np.int32)
dfbase["Barra"][lstQinj]=(Q_barra-np.ones(len(Q_barra))).astype(np.int32)
dfbase["Barra"][lstV]=(V_barra-np.ones(len(V_barra))).astype(np.int32)

PFramos=[]
QFramos=[]
Pinjname=[]
Qinjname=[]
Vname=[]
[Pinjname.append("P    ") for x in lstPinj]
[Qinjname.append("Q    ") for x in lstQinj]
[Vname.append("V    ") for x in lstV]
PFname=[]
QFname=[]
for x in range(len(Pf_de_para)):
    if not dfDLIN[(dfDLIN["de"]==int(Pf_de_para[x][0]))&(dfDLIN["para"]==int(Pf_de_para[x][1]))].empty:
        PFramos.append(int(dfDLIN[(dfDLIN["de"]==int(Pf_de_para[x][0]))&(dfDLIN["para"]==int(Pf_de_para[x][1]))]["Nlin"].values))
        PFname.append("Pkm ")
    elif not dfDLIN[(dfDLIN["para"]==int(Pf_de_para[x][0]))&(dfDLIN["de"]==int(Pf_de_para[x][1]))].empty:  
        PFramos.append(int(dfDLIN[(dfDLIN["para"]==int(Pf_de_para[x][0]))&(dfDLIN["de"]==int(Pf_de_para[x][1]))]["Nlin"].values)) 
        PFname.append("Pmk ")


for x in range(len(Qf_de_para)):
    if not dfDLIN[(dfDLIN["de"]==int(Qf_de_para[x][0]))&(dfDLIN["para"]==int(Qf_de_para[x][1]))].empty:
        QFramos.append(int(dfDLIN[(dfDLIN["de"]==int(Qf_de_para[x][0]))&(dfDLIN["para"]==int(Qf_de_para[x][1]))]["Nlin"].values))
        QFname.append("Qkm ")
    elif not dfDLIN[(dfDLIN["para"]==int(Pf_de_para[x][0]))&(dfDLIN["de"]==int(Pf_de_para[x][1]))].empty:  
        QFramos.append(int(dfDLIN[(dfDLIN["para"]==int(Qf_de_para[x][0]))&(dfDLIN["de"]==int(Qf_de_para[x][1]))]["Nlin"].values)) 
        QFname.append("Qmk ")

dfbase["tipo"]=np.ones(len(dfbase)).astype(np.int32)
dfbase["tipo"][lstPinj]=Pinjname
dfbase["tipo"][lstQinj]=Qinjname
dfbase["tipo"][lstV]=Vname
dfbase["tipo"][lstPf]=PFname
dfbase["tipo"][lstQf]=QFname
dfbase["ramo"][lstPf]=np.array(PFramos).astype(np.int32)
dfbase["ramo"][lstQf]=np.array(QFramos).astype(np.int32)
dfbase["Zverd"]=dfbase["Valores"]
dfbase["Zmed"]=dfcaso["Valores"]
dfbase["ligado"]=np.ones(len(dfbase)).astype(np.int32)
dfbase["zeros"]=np.zeros(len(dfbase)).astype(np.int32)

header="{:d};{:d};{:d};{:d};{:d};{:d};{:d};0;0;0;\n".format(len(dfDBAR),len(dfDLIN),len(Pinjname),len(Qinjname),len(PFname),len(QFname),len(Vname))
with open("out.csv","w") as f:
    f.write(header)


dfprint=dfbase[["ligado","tipo","Barra","ramo","Zverd","Zmed","sigma","zeros"]]
dfprint.to_csv("out.csv",mode="a",sep=";",header=None,index=None,float_format="%0.7f")

with open("out.csv","a") as f:
    f.write("9999\n")