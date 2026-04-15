
def main_path():
    
    main_path = "/store/vitorpmatias/TESE/TESE/"

    return main_path

def stringify_dict(d):
    parts = []
    
    for key, value in d.items():
        if isinstance(value, list):  
            value_str = "_".join(map(str, value))
        else:
            value_str = str(value).replace(".", "") 

        parts.append(f"{key}_{value_str}")

    return "_".join(parts)