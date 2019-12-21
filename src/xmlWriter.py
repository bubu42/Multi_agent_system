from builtins import len

from lxml import etree


def xmlWriter(scen, listVar, listDom, listCtr):
    f = open("../xml/" + scen + ".xml", "w+")

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
                                  nbValues=str(listDom[i]['cdr']))
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

    #contraints
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

#xmlWriter(scen="scen02", listVar=listVar2, listDom=listDom2, listCtr=listCtr2)
