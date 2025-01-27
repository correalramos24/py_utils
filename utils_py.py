import pathlib

# =============================CHECK TYPES======================================
def is_a_list(var) -> bool:
    """Check if var is a list"""
    return isinstance(var, list)

def is_a_str(var) -> bool:
    """Check if var is a string"""
    return isinstance(var, str)

def is_a_path(var) -> bool:
    """Check if var is a Path"""
    return isinstance(var, pathlib.Path)

# =============================PATH METHODS=====================================
def convert_path_to_str(p: pathlib.Path) -> str:
    """Convert a Path (only name) to a string"""
    return str(p.name).replace("/", "-")

def convert_full_path_to_str(p: pathlib.Path) -> str:
    """Convert a Path (full path) to a string"""
    return str(p).replace("/", "-")

# =============================STRING METHODS===================================
def stringfy(var) -> str:
    """Convert var to string, according to the type"""
    if is_a_path(var): 
        return convert_path_to_str(var)
    elif is_a_list(var):
        ret = str(var[0])
        for e in var[1:]:
            ret+= ',' +str(e)
        return ret
    else:
        return str(var)

def listify(var: object) -> list:
    """Convert var to list, if it is not already a list or none"""
    if is_a_list(var) or not var: 
        return var
    else:
        return [var]

# =============================DICT METHODS=====================================

def get_key(d: dict, key, builder, default: object = None) -> object:
    return builder(d[key]) if key in d else default
    
def safe_get_key(d: dict, key, builder, default: object = None) -> object:
    if key in d.keys():
        try:
            return builder(d[key])
        except Exception:
            return default
    else:
        return default







