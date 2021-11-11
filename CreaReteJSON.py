import jsonpickle

def CreaJSONdaRete(path,rete):
    f = open(path, 'w')
    json_obj = jsonpickle.encode(rete)
    f.write(json_obj)