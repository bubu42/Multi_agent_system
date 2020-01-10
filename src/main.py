###################
#                 #
#   Muti-agents   #
#                 #
###################

import os
import random
from builtins import len

import matplotlib.pyplot as plt
import nested_dict as nd
import numpy as np
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
        if len(ligne) == 6:
            listCtrDict["cost"] = ligne[5]
        else:
            listCtrDict["cost"] = 0

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

    if listCst == []:
        for i in range(0, len(listCST)):
            listCstDict[str(listCST[i])] = 1
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

    listCST = ['a1', 'a2', 'a3', 'a4', 'b1', 'b2', 'b3', 'b4']

    return listVar, listCst, listCtr, listDom


def xmlWriter(name, listVar, listCst, listCtr, listDom, path='/Users/citak/PycharmProjects/Multi_agent_system/xml/'):
    test = path.split("/")
    listCST = ['a1', 'a2', 'a3', 'a4', 'b1', 'b2', 'b3', 'b4']
    scenN = 0

    path += name + '.xml'

    f = open(path, 'w')

    # instance
    instance = etree.Element("instance")
    presentation = etree.SubElement(instance, "presentation", name=name, maxConstraintArity="2",
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
            parameters.text = "int variable1 int variable2 int K int C"
            expression = etree.SubElement(predicate, "expression")
            functional = etree.SubElement(expression, "functional")
            functional.text = "if(eq(abs(sub(variable1,variable2)),K),0,C)"
        if listOpe[i] is ">":
            predicate = etree.SubElement(predicates, "predicate", name="gt")
            parameters = etree.SubElement(predicate, "parameters")
            parameters.text = "int variable1 int variable2 int K int C"
            expression = etree.SubElement(predicate, "expression")
            functional = etree.SubElement(expression, "functional")
            functional.text = "if(gt(abs(sub(variable1,variable2)),K),0,C)"
        # we add another operator if we needed

    # contraints
    contraints = etree.SubElement(instance, 'constraints', nbConstraints=str(len(listCtr)))
    for i in range(0, len(listCtr)):
        if listCtr[i]['ope'] is "=":
            constraint = etree.SubElement(contraints, 'constraint', name=str(listCtr[i]['var1']) + "_eq_" + str(
                listCtr[i]['var2']) + "_with_K=" + str(listCtr[i]['dev']), arity="2",
                                          scope='var' + str(listCtr[i]['var1']) + " var" + str(listCtr[i]['var2']),
                                          reference="eq")

        if listCtr[i]['ope'] is '>':
            constraint = etree.SubElement(contraints, 'constraint',
                                          name=str(listCtr[i]['var1']) + "_gt_" + str(
                                              listCtr[i]['var2']) + "_with_K=" + str(listCtr[i]['dev'])
                                          , arity="2",
                                          scope='var' + str(listCtr[i]['var1']) + " var" + str(listCtr[i]['var2']),
                                          reference="gt")
        parameters = etree.SubElement(constraint, "parameters")

        parameters.text = 'var' + str(listCtr[i]['var1']).replace("\'", "") \
                          + " var" + \
                          str(listCtr[i]['var2']).replace("\'", "") + \
                          " " + \
                          str(listCtr[i]['dev']).replace("\'", "") + \
                          " " + str(listCst[int(listCtr[i]['cost'])][str(listCST[int(listCtr[i]['cost'])])])

    # write into file
    f.write(etree.tounicode(instance, pretty_print=True, method="xml"))
    f.close()

    return path


def frodoRun(pathResult, pathAbs, algo, pathXml, name):
    os.chdir('/Users/citak/PycharmProjects/Multi_agent_system')
    for i in algo:
        os.system("java -cp ./frodo2/frodo2.17.1.jar frodo2.algorithms.AgentFactory " + pathXml +
                  " ./frodo2/agents/" + i + '/' + i + "agentJaCoP.xml -timeout 36000000000 > " + pathResult + "" + i + "agentJaCoP" + name + ".txt")


##########
# RANDOM #
##########
def CreaterandomVarFile(path, nbVar, nbDom):
    fileRandomVar = open(path + '/var.txt', 'w+')

    for i in range(0, nbVar):
        dom = random.randint(1, nbDom)
        lines = str(i + 1) + ' ' + str(dom) + '\n'
        fileRandomVar.writelines(lines)

    fileRandomVar.close()


def CreaterandomDomFile(path, nbDom, nbElem):
    fileRandomDom = open(path + '/dom.txt', 'w+')

    for i in range(0, nbDom):
        elem = random.randint(1, nbElem)
        lines = str(i + 1) + ' ' + str(elem)
        for j in range(0, elem):
            nb = random.randint(1, 792)
            listR = []
            if nb not in listR:
                lines += ' ' + str(nb)
            listR = []
        lines += '\n'
        fileRandomDom.writelines(lines)

    fileRandomDom.close()


def CreaterandomCtrFile(path, nbVar):
    fileRandomCtr = open(path + '/ctr.txt', 'w+')

    for i in range(0, nbVar):
        nbVarR = random.randint(1, nbVar - 1)
        for j in range(0, nbVarR):
            nb = random.randint(1, 400)
            nbG = random.choice(['=', '>'])
            nbOp = random.choice(['D', 'F', 'G', 'L'])
            if nbG is '=':
                nb = 238

            if i != j:
                lines = str(i + 1) + ' ' + str(j + 1) + ' ' + str(nbOp) + ' ' + str(nbG) + ' ' + str(nb) + '\n'

                fileRandomCtr.writelines(lines)

    fileRandomCtr.close()


def CreaterandomCstFile(path, b=False):
    fileRandomCst = open(path + '/cst.txt', 'w+')
    lines = 'vide'
    if b is False:

        fileRandomCst.writelines(lines)

    else:
        listNbVar = random.choice(['100000', '10000', '1000', '100', '10'])
        if listNbVar is '100000':
            lines = 'a1 = 100000 \n a2 = 10000 \n  a3 = 1000 \n a4 = 100 \n  b1 = 10 \n b2 = 1 \n  b3 = 1 \n b4 = 1 \n '
        if listNbVar is '10000':
            lines = 'a1 = 10000 \n a2 = 1000 \n  a3 = 100 \n a4 = 10 \n  b1 = 1 \n b2 = 1 \n  b3 = 1 \n b4 = 1 \n '
        if listNbVar is '1000':
            lines = 'a1 = 1000 \n a2 = 100 \n  a3 = 10 \n a4 = 10\n  b1 = 1 \n b2 = 1 \n  b3 = 1 \n b4 = 1 \n '
        if listNbVar is '100':
            lines = 'a1 = 100 \n a2 = 10 \n  a3 = 1 \n a4 = 1 \n  b1 = 1 \n b2 = 1 \n  b3 = 1 \n b4 = 1 \n '
        if listNbVar is '10':
            lines = 'a1 = 1 \n a2 = 1 \n  a3 = 1 \n a4 = 1 \n  b1 = 1 \n b2 = 1 \n  b3 = 1 \n b4 = 1 \n '
    fileRandomCst.writelines(lines)

    fileRandomCst.close()


def OutputReadCostAndTime(outputPath):
    listScen = ['scen01', 'scen02', 'scen03', 'scen04', 'scen05', 'scen06',
                'scen07', 'scen08', 'scen09', 'scen10', 'scen11']
    #  Problem 1: 916 var., 5548 con., best known solution has cost 16 (optimal)

    listVar = [916, 200, 400, 680, 400, 200, 400, 916, 680, 680, 680]

    dir = os.listdir(outputPath)

    listOut = nd.nested_dict()
    list = dict()
    for file in dir:
        fileTest = file.replace('.txt', '')

        fileTest = fileTest.replace('agent', '')
        print(file)
        if 'JaCoP' in file:
            fileTest = fileTest.replace('_', '').split('JaCoP')
            nameF = fileTest[0] + '_' + fileTest[1]
            listOut[nameF]['algo'] = fileTest[0]
            # listOut[nameF]['file'] = fileTest[1]
            if 'random' in file:
                listOut[nameF]['variables'] = fileTest[1].split('random')[1]
            else:
                scen = fileTest[1].split('_')
                for i in range(len(listScen)):
                    if scen is listScen[i]:
                        listOut[nameF]['variables'] = listVar[i]

        f = open(outputPath + '/' + file, 'r')
        nbM = 0
        abIno = 0
        while 1:
            line = f.readline()

            if not line: break  # stop the loop if no line was read

            if 'Total cost of reported solution: ' in line:
                line = line.split('Total cost of reported solution: ')
                line[1] = line[1].replace(' ', '')
                listOut[nameF]['cost'] = line[1].replace('\n', '')

            if 'Algorithm finished' in line:
                line = line.split('Algorithm finished in')
                line = line[1].split('ms')
                listOut[nameF]['time'] = line[0].replace(' ', '')
                listOut[nameF]['time'] = line[0].replace('\u202f', '')  # probleme d'espace sous MacOs
            if 'Number of messages sent (by type):' in line and nbM != 1:
                while 1:
                    line = f.readline()

                    if '- Total:' in line:
                        print('nbMe: ', line)

                        line = line.split('- Total:')
                        listOut[nameF]['nbM'] = line[1].replace(' ', '').replace('\t', '').replace('\n', '').replace(
                            '\u202f', '')
                        nbM = 1

                    if 'Amount of information sent (by type, in bytes):' in line and abIno != 1:
                        while 1:
                            line = f.readline()
                            if '- Total:' in line:
                                print('amount: ', line)
                                line = line.split('- Total:')
                                listOut[nameF]['abInfo'] = line[1].replace(' ', '').replace('\t', '').replace('\n',
                                                                                                              '').replace(
                                    '\u202f', '')
                                abIno = 1
                                break
                        break
                break
        f.close()
    return listOut


def displayRes(listOut):
    for v in listOut:
        if not listOut[str(v)]['time']:
            print(v, '\ttime : out\tcost : / \tnbMessage : / \tAmount of information sent : /')
        else:
            print(v, '\ttime : ', listOut[str(v)]['time'],
                  '\tcost : ', listOut[str(v)]['cost'],
                  '\tnbMessage : ', listOut[str(v)]['nbM'],
                  '\tAmount of information sent : ', listOut[str(v)]['abInfo'])


def plotResTimeRandom(listOut):
    var = []
    algo = []
    var4 = []
    algo4 = []
    var10 = []
    algo10 = []
    var20 = []
    algo20 = []
    nbVar = []
    print(listOut)

    for v in listOut:

        if listOut[str(v)]['variables'] == '4':
            var4.append(int(listOut[str(v)]['time']))
            algo4.append(listOut[str(v)]['algo'])
        if listOut[str(v)]['variables'] == '10':
            if listOut[str(v)]['time']:
                var10.append(int(listOut[str(v)]['time']))
            else:
                var10.append(0)
            algo10.append(listOut[str(v)]['algo'])
        if listOut[str(v)]['variables'] == '20':
            if listOut[str(v)]['time']:
                var20.append(int(listOut[str(v)]['time']))
            else:
                var20.append(0)
            algo20.append(listOut[str(v)]['algo'])
        else:
            if listOut[str(v)]['time']:
                listOut[str(v)]['time'] = str(listOut[str(v)]['time']).replace(',', '')
                var.append(int(listOut[str(v)]['time']))
            else:
                var.append(0)
            algo.append(listOut[str(v)]['algo'])
            nbVar.append(v)

    if var4:
        ##########
        #  4 var #
        ##########
        plt.title("Temps d'éxéution (en ms) en fonction de l'algorithme utilisé \n 4 VAR")
        plt.bar(np.arange(len(var4)), var4, align='center')
        plt.xticks(np.arange(len(var4)), algo4)

        plt.ylabel('time in ms')
        plt.xlabel('algorithme')

        plt.savefig('./plot/time/algoAvec4varTime.png')
        plt.show()

    if var10:
        print(algo10)
        ##########
        # 10 var #
        ##########
        plt.title("Temps d'éxéution (en ms) en fonction de l'algorithme utilisé \n 10 VAR ")
        plt.bar(np.arange(len(var10)), var10, align='center')
        plt.xticks(np.arange(len(var10)), algo10)

        plt.ylabel('time in ms')
        plt.xlabel('algorithme')

        plt.savefig('./plot/time/algoAvec10varTime.png')
        plt.show()

    if var20:
        ##########
        # 20 var #
        ##########
        plt.title("Temps d'éxéution (en ms) en fonction de l'algorithme utilisé \n 20 VAR")
        plt.bar(np.arange(len(var20)), var20, align='center')
        plt.xticks(np.arange(len(var20)), algo20)

        plt.ylabel('time in ms')
        plt.xlabel('algorithme')

        plt.savefig('./plot/time/algoAvec20varTime.png')
        plt.show()
    else:

        ##########
        # ?? var #
        ##########
        plt.title(
            "Temps d'éxéution (en ms) en fonction de l'algorithme utilisé \n  " + str(nbVar[0]).split('_')[1] + "VAR ")
        plt.bar(np.arange(len(var10)), var10, align='center')
        plt.xticks(np.arange(len(var10)), algo10)

        plt.ylabel('time in ms')
        plt.xlabel('algorithme')

        plt.savefig('./plot/time/algoAvec10varTime.png')
        plt.show()


def plotResCostRandom(listOut):
    var = []
    algo = []
    var4 = []
    algo4 = []
    var10 = []
    algo10 = []
    var20 = []
    algo20 = []
    print(listOut)

    for v in listOut:

        if listOut[str(v)]['variables'] == '4':
            var4.append(int(listOut[str(v)]['cost']))
            algo4.append(listOut[str(v)]['algo'])
        if listOut[str(v)]['variables'] == '10':
            if listOut[str(v)]['cost']:
                var10.append(int(listOut[str(v)]['cost']))
            else:
                var10.append(0)
            algo10.append(listOut[str(v)]['algo'])
        if listOut[str(v)]['variables'] == '20':
            if listOut[str(v)]['cost']:
                var20.append(int(listOut[str(v)]['cost']))
            else:
                var20.append(0)
            algo20.append(listOut[str(v)]['algo'])
        else:
            if listOut[str(v)]['cost']:
                var.append(int(listOut[str(v)]['cost']))
            else:
                var.append(0)
            algo.append(listOut[str(v)]['algo'])

    if var4:
        ##########
        #  4 var #
        ##########
        plt.title("Coût en fonction de l'algorithme utilisé \n 4 VAR")
        plt.bar(np.arange(len(var4)), var4, align='center')
        plt.xticks(np.arange(len(var4)), algo4)

        plt.ylabel('cost')
        plt.xlabel('algorithme')

        plt.savefig('./plot/cost/algoAvec4varCost.png')
        plt.show()

    if var10:
        print(algo10)
        ##########
        # 10 var #
        ##########
        plt.title("Coût en fonction de l'algorithme utilisé \n 10 VAR ")
        plt.bar(np.arange(len(var10)), var10, align='center')
        plt.xticks(np.arange(len(var10)), algo10)

        plt.ylabel('cost')
        plt.xlabel('algorithme')

        plt.savefig('./plot/cost/algoAvec10varCost.png')
        plt.show()

    if var20:
        ##########
        # 20 var #
        ##########
        plt.title("Coût en fonction de l'algorithme utilisé \n 20 VAR")
        plt.bar(np.arange(len(var20)), var20, align='center')
        plt.xticks(np.arange(len(var20)), algo20)

        plt.ylabel('cost')
        plt.xlabel('algorithme')

        plt.savefig('./plot/cost/algoAvec20varCost.png')
        plt.show()


def plotResNbMesRandom(listOut):
    var = []
    algo = []
    abInfo = []
    var4 = []
    algo4 = []
    abInfo4 = []
    var10 = []
    algo10 = []
    abInfo10 = []
    var20 = []
    algo20 = []
    abInfo20 = []
    print(listOut)

    for v in listOut:

        if listOut[str(v)]['variables'] == '4':
            var4.append(int(listOut[str(v)]['nbM']))
            algo4.append(listOut[str(v)]['algo'])
            abInfo4.append(int(listOut[str(v)]['abInfo']))
        if listOut[str(v)]['variables'] == '10':
            if listOut[str(v)]['nbM']:
                var10.append(int(listOut[str(v)]['nbM']))
                abInfo10.append(int(listOut[str(v)]['abInfo']))
            else:
                var10.append(0)
                abInfo10.append(0)
            algo10.append(listOut[str(v)]['algo'])
        if listOut[str(v)]['variables'] == '20':
            if listOut[str(v)]['nbM']:
                var20.append(int(listOut[str(v)]['nbM']))
                abInfo20.append(int(listOut[str(v)]['abInfo']))
            else:
                var20.append(0)
                abInfo20.append(0)
            algo20.append(listOut[str(v)]['algo'])
        else:
            if listOut[str(v)]['nbM']:
                listOut[str(v)]['nbM'] = str(listOut[str(v)]['nbM']).replace(',', '')
                listOut[str(v)]['abInfo'] = str(listOut[str(v)]['abInfo']).replace(',', '')
                var.append(int(listOut[str(v)]['nbM']))
                abInfo.append(int(listOut[str(v)]['abInfo']))
            else:
                var.append(0)
                abInfo.append(0)
            algo.append(listOut[str(v)]['algo'])

    if var4:
        ##########
        #  4 var #
        ##########
        plt.title("nb messages en fonction de l'algorithme utilisé \n 4 VAR ")

        plt.bar(np.arange(len(var4)), var4, align='center')
        plt.xticks(np.arange(len(var4)), algo4)

        plt.ylabel('cost')
        plt.xlabel('algorithme')

        plt.savefig('./plot/nbMessage/algoAvec4varNbMessage.png')
        plt.show()

    if var10:
        print(algo10)
        ##########
        # 10 var #
        ##########
        plt.title("nb messages en fonction de l'algorithme utilisé \n 10 VAR ")
        plt.bar(np.arange(len(var10)), var10, align='center')
        plt.xticks(np.arange(len(var10)), algo10)

        plt.ylabel('cost')
        plt.xlabel('algorithme')

        plt.savefig('./plot/nbMessage/algoAvec10varNbMessage.png')
        plt.show()

    if var20:
        ##########
        # 20 var #
        ##########
        plt.title("nb messages en fonction de l'algorithme utilisé \n 20 VAR ")
        plt.bar(np.arange(len(var20)), var20, align='center')
        plt.xticks(np.arange(len(var20)), algo20)

        plt.ylabel('cost')
        plt.xlabel('algorithme')

        plt.savefig('./plot/nbMessage/algoAvec20varNbMessage.png')
        plt.show()


def plotResabInfoRandom(listOut):
    var = []
    algo = []
    var4 = []
    algo4 = []
    var10 = []
    algo10 = []
    var20 = []
    algo20 = []
    print(listOut)

    for v in listOut:

        if listOut[str(v)]['variables'] == '4':
            var4.append(int(listOut[str(v)]['abInfo']))
            algo4.append(listOut[str(v)]['algo'])
        if listOut[str(v)]['variables'] == '10':
            if listOut[str(v)]['abInfo']:
                var10.append(int(listOut[str(v)]['abInfo']))
            else:
                var10.append(0)
            algo10.append(listOut[str(v)]['algo'])
        if listOut[str(v)]['variables'] == '20':
            if listOut[str(v)]['abInfo']:
                var20.append(int(listOut[str(v)]['abInfo']))
            else:
                var20.append(0)
            algo20.append(listOut[str(v)]['algo'])
        else:
            if listOut[str(v)]['abInfo']:
                listOut[str(v)]['abInfo'] = str(listOut[str(v)]['abInfo']).replace(',', '')
                var.append(int(listOut[str(v)]['abInfo']))
            else:
                var.append(0)
            algo.append(listOut[str(v)]['algo'])

    if var4:
        ##########
        #  4 var #
        ##########
        plt.title("Amount of information sent en fonction de l'algorithme utilisé \n 4 VAR ")
        plt.bar(np.arange(len(var4)), var4, align='center')
        plt.xticks(np.arange(len(var4)), algo4)

        plt.ylabel('cost')
        plt.xlabel('algorithme')

        plt.savefig('./plot/amount/algoAvec4varNbMessage.png')
        plt.show()

    if var10:
        print(algo10)
        ##########
        # 10 var #
        ##########
        plt.title("Amount of information sent en fonction de l'algorithme utilisé \n 10 VAR ")
        plt.bar(np.arange(len(var10)), var10, align='center')
        plt.xticks(np.arange(len(var10)), algo10)

        plt.ylabel('cost')
        plt.xlabel('algorithme')

        plt.savefig('./plot/amount/algoAvec10varNbMessage.png')
        plt.show()

    if var20:
        ##########
        # 20 var #
        ##########
        plt.title("Amount of information sent  en fonction de l'algorithme utilisé \n 20 VAR ")
        plt.bar(np.arange(len(var20)), var20, align='center')
        plt.xticks(np.arange(len(var20)), algo20)

        plt.ylabel('cost')
        plt.xlabel('algorithme')

        plt.savefig('./plot/amount/algoAvec20varNbMessage.png')
        plt.show()
    else:
        plt.title("Amount of information sent  en fonction de l'algorithme utilisé \n " + var + "VAR ")
        plt.bar(np.arange(len(var)), var, align='center')
        plt.xticks(np.arange(len(var)), algo)

        plt.ylabel('cost')
        plt.xlabel('algorithme')

        plt.savefig('./plot/amount/algoAvec' + var + 'varNbMessage.png')
        plt.show()


##################
# RUN ALL RANDOM #
##################
def CreateRandomAndPlotOrDisplay(pathFile, nbVar, nbDom, nbCst=False, plot=True,
                                 algo=['MGM', 'DSA', 'AFB', 'DPOP', 'ADOPT', 'MaxSum'], pathResult='./output/',
                                 pathXml='./xml/', name='random'):
    CreaterandomVarFile(pathFile, nbVar, nbDom)
    CreaterandomDomFile(pathFile, nbDom, 22)
    CreaterandomCtrFile(pathFile, nbVar)
    CreaterandomCstFile(pathFile, nbCst)
    listVar, listCst, listCtr, listDom = readRep(pathFile)
    pathXMLcreated = xmlWriter(name, listVar, listCst, listCtr, listDom, path=pathXml)

    frodoRun(pathResult, pathFile, algo, pathXMLcreated, name + str(len(listVar)))

    listOut = OutputReadCostAndTime(pathResult)
    if plot is False:
        displayRes(listOut)
    else:
        plotResTimeRandom(listOut)


##################
# RUN ALL CELAR  #
##################

def CreateCelarAndPlotOrDisplay(pathFile, name, plot=True,
                                algo=['MGM', 'DSA', 'AFB', 'DPOP', 'ADOPT', 'MaxSum'], pathResult='./output/',
                                pathXml='./xml/'):
    listVar, listCst, listCtr, listDom = readRep(pathFile)

    pathXMLcreated = xmlWriter(name, listVar, listCst, listCtr, listDom, path=pathXml)

    frodoRun(pathResult, pathFile, algo, pathXMLcreated, name)

    listOut = OutputReadCostAndTime(pathResult)
    if plot is False:
        displayRes(listOut)
    else:
        plotResTimeRandom(listOut)
        plotResCostRandom(listOut)
        plotResNbMesRandom(listOut)
        plotResabInfoRandom(listOut)


print(os.getcwd())

listOut = OutputReadCostAndTime(outputPath='./output/')
displayRes(listOut)
plotResTimeRandom(listOut)
plotResCostRandom(listOut)
plotResNbMesRandom(listOut)
plotResabInfoRandom(listOut)

# CreateRandomAndPlotOrDisplay('./pre/', nbVar=20, nbDom=7)
# CreateCelarAndPlotOrDisplay('fichier/FullRLFAP/CELAR/scen01','scen01')
