import sys
import textfsm
import re
import json
from tabulate import tabulate
from ntc_templates.parse import parse_output

file_name = 'show_router_bgp_summary'
template = './templates/nokia/' + file_name + '.textfsm'
output_file = './files/nokia/' + file_name + '.txt'
result_saved = './results/nokia/' + file_name + '.json'

with open(output_file) as output:
    # Get Address family
    firstLine = output.readlines()[0].rstrip()
    match = re.search('(?<=show bgp\s)\S*', firstLine) 
    if match is not None:
        addressFam = match.group(0)
    else:
        addressFam = "Unknown"

with open(template) as f, open(output_file) as output:
    re_table = textfsm.TextFSM(f)
    # print(re_table) # 
    header = re_table.header
    p = output.read()
    # print(p)
    result = re_table.ParseText(p)

    # ---------------
    # Para que se vea el Address Family en la tabla, comentar en este caso la linea de # Add column of address family to dictionary:
    if addressFam != 'Unknown':
        for i in result:
            i.append(addressFam)
        header.append('AddressFam')
    # --------------

    # Create dictionary:
    dictionary = {}
    count = 0
    for i in header:
        itm = []
        for item in result:
            itm.append(item[count])
        dictionary[i] = itm
        count+=1
    print('\n')
    print(dictionary)
    print('\n')

    # Add column of address family to dictionary:
    # dictionary['AddressFam'] = [addressFam]*len(result)

    print(tabulate(result, headers=header))
# Guardar Json:
with open(result_saved, 'w', encoding='utf-8') as f:
    json.dump(dictionary, f, ensure_ascii=False, indent=4)