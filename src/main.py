###################
#                 #
#   Muti-agents   #
#                 #
###################


chemin = "fichier/FullRLFAP/CELAR/scen02/"
var = "var.txt"
ctr = "ctr.txt"
cst = "cst.txt"
dom = "dom.txt"

fVar = open(chemin + var, "r")
fCtr = open(chemin + ctr, "r")
fCst = open(chemin + cst, "r")
fDom = open(chemin + dom, "r")

listVarDict = dict()
listVar = []

for ligne in fVar:
    ligne = ligne.split()
    listVarDict["var"] = ligne[0]
    listVarDict["dom"] = ligne[1]
    listVar.append(listVarDict)
    listVarDict = dict()

listCtrDict = dict()
listCtr = []

for ligne in fCtr:
    ligne = ligne.split()
    listCtrDict["var1"] = ligne[0]
    listCtrDict["var2"] = ligne[1]
    listCtrDict["ctr"] = ligne[2]
    listCtrDict["ope"] = ligne[3]
    listCtrDict["dev"] = ligne[4]
    listCtr.append(listCtrDict)
    listCtrDict = dict()

listDomDict = dict()
listDom = []

for ligne in fDom:
    ligne = ligne.split()
    listDomDict["dom"] = ligne[0]
    listDomDict["cdr"] = ligne[1]
    listDomDict["ens"] = ligne[2:int(ligne[1]) + 2]
    Cardinality = int(ligne[1])
    listDom.append(listDomDict)
    listDomDict = dict()

listOpe = []
for i in range(0, len(listCtr)):
    if listCtr[i]['ope'] not in listOpe:
        listOpe.append(listCtr[i]['ope'])

print(listVar)
print(listCtr)
print(listDom)
print(listDom[0]["ens"])
print(listDom[1]["ens"])
print(listDom[2]["ens"])
print(len(listVar))
print(listOpe)
