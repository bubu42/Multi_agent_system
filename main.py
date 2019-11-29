import os
import re
import pydcop as dcop


###################
#                 #
#   Muti-agents   #
#                 #
###################



chemin = "fichier/FullRLFAP/CELAR/scen01/"
var = "var.txt"
ctr = "ctr.txt"
cst = "cst.txt"
dom = "dom.txt"


fVar = open(chemin+var, "r")
fCtr = open(chemin+ctr, "r")
fCst = open(chemin+cst, "r")
fDom = open(chemin+dom, "r")



listVarDict = dict()
listVar =[]

for ligne in fVar:
    ligne = ligne.replace("  ","").replace("\n","").split()

    listVarDict["var"] = ligne[0]
    listVarDict["dom"] = ligne[1]

    listVar.append(listVarDict)


print (listVar)

