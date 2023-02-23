

def concat_list(a_list):
    if len(a_list) == 0:
        return ""
    else:
        return a_list[0] + concat_list(a_list[1:])


def product(data):
    if len(data) == 0:
        return 1
    else:
        return data[0] * product(data[1:])


def backwards(s):
    if len(s) == 0:
        return ""
    
    return backwards(s[1:]) + s[0] 

def odds(data):
    if len(data) == 0:
        return []
    elif data[0] % 2 != 0:
        return [data[0]] + odds(data[1:])
    else:
        return odds(data[1:])


def squares(data, index = ""):
    if len(data) == 0:
        return index
    else:
        return [data[0] * data[0]] + squares(data[1:])
    
def find(data, value):
    if len(data) == 0:
        return None
    else:
        if value == data[0]:
            return 0
        else:
            recursive_stuff = find(data[1:], value)
            if recursive_stuff != None:
                return 1 + recursive_stuff
            else:
                return None

print(find(["hi", "", "you", "there"], "there"))
