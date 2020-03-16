# dependencies
from os import listdir
from os.path import isfile, join
from flask import jsonify

# utils
from utils.constants import ROUTE_SAVE


def qualification():
    all_count_enter = 0
    all_count_urgente = 0
    all_count_exelente_servicio_finisht = 0
    all_count_exelente_servicio_include = 0
    # get list files history qualification
    list_files = [f for f in listdir(ROUTE_SAVE) if isfile(join(ROUTE_SAVE, f))]
    # loop list files
    for file in list_files:
        open_file = open(f'{ROUTE_SAVE}/{file}')
        # read file
        read_file = open_file.read()
        # dividier file
        dividier_conversation = read_file.split('CONVERSACION')
        # loop dividier conversation
        for i in range(1, len(dividier_conversation)):
            data = dividier_conversation[i]
            # count for \n line
            if i != len(dividier_conversation) - 1:
                count_enter = data.count('\n') - 2
            else:
                count_enter = data.count('\n')
            all_count_enter += count_enter
            # count for URGENTE
            count_urgente = data.count('URGENTE')
            all_count_urgente += count_urgente
            # count for EXCELENTE SERVICIO FINISHT
            count_exelente_servicio_finisht = data.count('EXCELENTE SERVICIO.\n\n')
            all_count_exelente_servicio_finisht += count_exelente_servicio_finisht
            # count for EXCELENTE SERVICIO
            count_exelente_servicio = data.count('EXCELENTE SERVICIO')
            all_count_exelente_servicio_include += count_exelente_servicio
            # count times
            time_init = ''
            time_finisht = ''
            results_list_line_conversaiton = list(filter(lambda x: (len(x) > 0), data.split('\n')))
            print(results_list_line_conversaiton)

            '''for line in range(1, len(data.split('\n'))):
                line_time = data.split('\n')[line]
                # validate if not \n
                if len(line_time) > 0:
                    print(line_time)
            print()

        count_enter = read_file.count('\n')
        count_urgente = read_file.count('URGENTE')
        print(count_urgente)'''
    # calculate diff EXCELENTE SERVICIO
    all_count_exelente_servicio_include = all_count_exelente_servicio_include - all_count_exelente_servicio_finisht
    return jsonify({'success': True}), 200