import logging
import re
from itertools import groupby


def createLogger(name, lvl=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(lvl)
    ch = logging.StreamHandler()
    ch.setLevel(lvl)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger






# s1 = ['level=1&ritual=true&range=30']
# s2 = ['level=1', '&', 'ritual=true', '&range=30']
# s3 = ['level', '=', '1', '&', 'ritual', '=', 'true', '&', 'range=', '30']
# s4 = ['level', '=', '1&ritual', '=', 'true&range', '=', '30']

# def norm_query(q):
#     p = re.compile(r"\w+(?:'\w+)*|[^\w\s]")
#     norm_list = []
#     for x in q:
#         norm_list += p.findall(x)
#     # ['level', '=', '1', '|', 'ritual', '=', 'true']
#     return norm_list

# def process_query(q):
#     normd_q = norm_query(q)
#     AND = groupby(normd_q, lambda x: x == '&')
#     result = [list(group) for m, group in AND if not m]
#     return result


# print(process_query(s1))
# print(process_query(s2))
# print(process_query(s3))
# a = process_query(s4)



# root ::= value
# value ::= string | filter | '&'
# filter ::= string '=' value

def parse_filter(inp):
    filter_regex = re.compile(r'(\w+)\s*=\s*([a-zA-Z0-9_ ]*)\s*(.*)')
    match = filter_regex.search(inp)
    if match is not None:
        field, value, remainds = match.groups()
        return field.strip(), value.strip(), remainds


def parse(s):
    inp = s
    result = []
    while inp:
        field, value, inp = list(parse_filter(inp))
        result.append([field, value])
    return result

print(parse('level=1 & ritual=True'))

print(parse('level=1 & ritual=True'))
print(parse('level= 1& ritual= True'))
print(parse('level = 1 & ritual= True'))
print(parse('level =1'))
print(parse('level   =1'))
print(parse('name = acid arrow & ritual=True'))



