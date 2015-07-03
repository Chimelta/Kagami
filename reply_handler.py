import re

def add_at(name: str):
    return '@' + name + ' '

def reply_handle(text: str, my_name: str, author_name: str):
    pattern = re.compile('(@.*? )')
    matched = pattern.findall(text)
    if my_name == author_name:
        ret = ''
    else:
        ret = '@' + author_name + ' '
    for x in matched:
        if x != add_at(my_name) and x != add_at(author_name) and x != '@ ':
            ret += x
    return ret

