def ask(var, value, evidence, bn):
    prob = {}
    for each in [True, False]:
        evidence[var] = each
        prob[each] = ask_all(bn.variable_names[::-1],evidence,bn)
        del evidence[var]
    return prob[value] / sum(prob.values())

def ask_all(var, evidence, bn):
    if var == []: return 1.0
    total = 0.0
    eachEvidence = var.pop()    
    if eachEvidence not in evidence:
        for each in [True, False]:
            evidence[eachEvidence] = each
            total += bn.get_var(eachEvidence).probability(each, evidence) * ask_all(var, evidence, bn)
            del evidence[eachEvidence]       
    else: 
        total += bn.get_var(eachEvidence).probability(evidence[eachEvidence], evidence)*ask_all(var, evidence, bn)
    var.append(eachEvidence)
    return total