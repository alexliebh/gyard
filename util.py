NATIONALITIES = ["pays de l'est", "autres pays", "allemand", "hollandais", "alsacien-lorrain", "france", "belges", "anglais"]

def find_person_nationality(entry):
    for natio in NATIONALITIES:
        if(entry[natio].all() == True): 
            return natio
    return "inconnu"

def find_group_nationalities(data):
    natios = {}
    for natio in NATIONALITIES:
        natios[natio] = 0
    natios["inconnu"] = 0
    for id in data.index:
        natios[find_person_nationality(data.loc[[id]])] += 1
    return natios