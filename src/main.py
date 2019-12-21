###################
#                 #
#   Muti-agents   #
#                 #
###################

import os
from builtins import len

from lxml import etree


def varFileReader(pathFile):
    fVar = open(pathFile, "r")

    listVarDict = dict()
    listVar = []

    for ligne in fVar:
        ligne = ligne.split()

        listVarDict["var"] = ligne[0]
        listVarDict["dom"] = ligne[1]
        if len(ligne) > 2:
            listVarDict["K"] = ligne[2]
            listVarDict["C"] = ligne[3]

        listVar.append(listVarDict)
        listVarDict = dict()
    fVar.close()
    return listVar


def ctrFileReader(pathFile):
    fCtr = open(pathFile, "r")

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
    fCtr.close()
    return listCtr


def cstFileReader(pathFile):
    fCst = open(pathFile, "r")

    listCstDict = dict()
    listCst = []
    listCST = ['a1', 'a2', 'a3', 'a4', 'b1', 'b2', 'b3', 'b4']
    for ligne in fCst:
        ligne = ligne.split()
        if ligne != [] and ligne[0] in listCST:
            listCstDict[str(ligne[0])] = ligne[2]
            listCst.append(listCstDict)
            listCstDict = dict()
    fCst.close()

    return listCst


def domFileReader(pathFile):
    fDom = open(pathFile, "r")
    listDomDict = dict()
    listDom = []

    for ligne in fDom:
        ligne = ligne.split()
        listDomDict["dom"] = ligne[0]
        listDomDict["crd"] = ligne[1]
        listDomDict["ens"] = ligne[2:int(ligne[1]) + 2]
        Cardinality = int(ligne[1])
        listDom.append(listDomDict)
        listDomDict = dict()

    fDom.close()

    return listDom


def readRep(path):
    rep = os.listdir(path)

    pathFile = os.path.abspath(path)

    listFileMandatory = ["var.txt", "cst.txt", "ctr.txt", "dom.txt"]

    listVar = []
    listCst = []
    listCtr = []
    listDom = []
    for file in rep:

        if listFileMandatory[0] == file.lower():
            listVar = varFileReader(pathFile + "/" + str(listFileMandatory[0]))
        if listFileMandatory[1] == file.lower():
            listCst = cstFileReader(pathFile + "/" + str(listFileMandatory[1]))
        if listFileMandatory[2] == file.lower():
            listCtr = ctrFileReader(pathFile + "/" + str(listFileMandatory[2]))
        if listFileMandatory[3] == file.lower():
            listDom = domFileReader(pathFile + "/" + str(listFileMandatory[3]))
    print(listVar)
    print(listCst)
    print(listCtr)
    print(listDom)

    return listVar, listCst, listCtr, listDom


def xmlWriter(path):
    test = path.split("/")
    for i in range(0, len(test)):
        print(test[i])
        if "scen" in test[i]:
            scen = test[i]

    listVar, listCst, listCtr, listDom = readRep(path)

    print(os.getcwd())
    path = "xml/" + scen + ".xml"
    f = open(path, 'w')

    # instance
    instance = etree.Element("instance")
    presentation = etree.SubElement(instance, "presentation", name=str(scen), maxConstraintArity="3",
                                    maximize="false", format="XCSP 2.1_FRODO")

    # agents
    agents = etree.SubElement(instance, "agents", nbAgents=str(len(listVar)))
    for i in range(0, len(listVar)):
        agent = etree.SubElement(agents, "agent", name="agent" + str(i + 1))

    # domains
    domains = etree.SubElement(instance, "domains", nbDomains=str(len(listDom)))
    for i in range(0, len(listDom)):
        domain = etree.SubElement(domains, "domain", name="dom" + str(listDom[i]['dom']),
                                  nbValues=str(listDom[i]['crd']))
        domain.text = str(listDom[i]['ens']).replace("\'", "").replace("]", "").replace("[", "").replace(",", "")

    # varibles
    variables = etree.SubElement(instance, "variables", nbVariables=str(len(listVar)))
    for i in range(0, len(listVar)):
        variable = etree.SubElement(variables, "variable", name="var" + str((listVar[i]['var'])),
                                    domain="dom" + str(listVar[i]['dom']),
                                    agent="agent" + str(i + 1))

    # predicates
    listOpe = []
    for i in range(0, len(listCtr)):
        if listCtr[i]['ope'] not in listOpe:
            listOpe.append(listCtr[i]['ope'])

    predicates = etree.SubElement(instance, "predicates", nbPredicates=str(len(listOpe)))
    for i in range(0, len(listOpe)):
        if listOpe[i] is "=":
            predicate = etree.SubElement(predicates, "predicate", name="eq")
            parameters = etree.SubElement(predicate, "parameters")
            parameters.text = "int variable1 int variable2 int k12"
            expression = etree.SubElement(predicate, "expression")
            functional = etree.SubElement(expression, "functional")
            functional.text = "eq(abs(sub(variable1,variable2)),k12)"
        if listOpe[i] is ">":
            predicate = etree.SubElement(predicates, "predicate", name="gt")
            parameters = etree.SubElement(predicate, "parameters")
            parameters.text = "int variable1 int variable2 int k12"
            expression = etree.SubElement(predicate, "expression")
            functional = etree.SubElement(expression, "functional")
            functional.text = "gt(abs(sub(variable1,variable2)),k12)"
        # we add another operator if we needed

    # contraints
    contraints = etree.SubElement(instance, 'constraints', nbConstraints=str(len(listCtr)))
    for i in range(0, len(listCtr)):
        if listCtr[i]['ope'] is "=":
            constraint = etree.SubElement(contraints, 'constraint', name=str(listCtr[i]['var1']) + "_eq_" + str(
                listCtr[i]['var2']) + "_with_k12=" + str(listCtr[i]['dev']), arity="3",
                                          scope='var' + str(listCtr[i]['var1']) + " var" + str(listCtr[i]['var2']),
                                          reference="eq")
            parameters = etree.SubElement(constraint, "parameters")
            parameters.text = 'var' + str(listCtr[i]['var1']).replace("\'", "") + " var" + str(
                listCtr[i]['var2']).replace("\'", "") + \
                              " " + \
                              str(listCtr[i]['dev']).replace("\'", "")
        if listCtr[i]['ope'] is '>':
            constraint = etree.SubElement(contraints, 'constraint',
                                          name=str(listCtr[i]['var1']) + "_gt_" + str(
                                              listCtr[i]['var2']) + "_with_k12=" + str(listCtr[i]['dev'])
                                          , arity="3",
                                          scope='var' + str(listCtr[i]['var1']) + " var" + str(listCtr[i]['var2']),
                                          reference="gt")
            parameters = etree.SubElement(constraint, "parameters")
            parameters.text = 'var' + str(listCtr[i]['var1']).replace("\'", "") \
                              + " var" + \
                              str(listCtr[i]['var2']).replace("\'", "") + \
                              " " + \
                              str(listCtr[i]['dev']).replace("\'", "")

    # write into file
    f.write(etree.tounicode(instance, pretty_print=True, method="xml"))
    f.close()

    return path


def frodoRun(pathAbs):
    path = xmlWriter(pathAbs)
    pathS = path.split("/")
    ScenN = str(pathS[len(pathS) - 1]).replace(".xml", "")
    print(ScenN)
    os.system(
        "java -cp frodo2/frodo2.17.1.jar frodo2.algorithms.AgentFactory " + path + " frodo2/agents/MGM/MGMagentJaCoP.xml > graph/" + ScenN + ".txt")


listScen = ['scen01', 'scen02', 'scen03', 'scen04', 'scen05', 'scen06', 'scen07', 'scen08', 'scen09', 'scen10',
            'scen11']

for i in range(0, len(listScen)):
    path = "fichier/FullRLFAP/CELAR/" + listScen[i]
    frodoRun(path)
