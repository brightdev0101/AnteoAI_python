def percentage(number, total, integer = False):
    if total > 0:
        percent = number / total * 100
   
        if integer:
            return int(percent)
        return percent

    return 0

def average(lst):
    if len(lst) > 0:
        return sum(lst) / len(lst)
    else:
        return 0
        
        
def getFromList(listFrom, key, placeholder):
    """ Return a value from list by key.
    If the key don't exist return a placeholder
    
    Params:
        listFrom (list) - Original list
        key (string) - The key to retriev
        placeholder (string) - The placeholder
        
    Return
        result object from list or placeholder
    """
    
    if key in listFrom:
        return listFrom[key]
    else:
        return placeholder
  
