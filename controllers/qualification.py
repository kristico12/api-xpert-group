# dependencies
from os import listdir
from os.path import isfile, join
from flask import jsonify
from datetime import datetime

# utils
from utils.constants import ROUTE_SAVE


def qualification():
    all_count_enter = 0
    all_points_count_enter = 0

    all_count_urgente = 0
    all_points_count_urgente = 0

    all_count_exelente_servicio_finisht = 0
    all_points_count_exelente_servicio_finisht = 0
    all_count_exelente_servicio_include = 0
    all_points_count_exelente_servicio_include = 0

    all_count_time_seconds_max_60 = 0
    all_points_count_time_seconds_max_60 = 0
    all_count_time_seconds_min_60 = 0
    all_points_count_time_seconds_min_60 = 0

    all_count_abandonated_chat = 0
    all_points_count_abandonated_chat = 0
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
            # --------------------------------------- count for \n line --------------------------------------------|
            if i != len(dividier_conversation) - 1:
                count_enter = data.count('\n') - 2
            else:
                count_enter = data.count('\n')
            all_count_enter += count_enter
            # calculate point for conversation
            if count_enter <= 5:
                all_points_count_enter += 20
            else:
                all_points_count_enter += 10
            # ----------------------------------------- count for URGENTE -------------------------------------------|
            count_urgente = data.count('URGENTE')
            all_count_urgente += count_urgente
            # calculate points for urgente
            if count_urgente != 0:
                if count_urgente <= 2:
                    all_points_count_urgente -= 5
                else:
                    all_points_count_urgente -= 10
            # ----------------------------------------- count for EXCELENTE SERVICIO FINISHT -------------------------|
            count_exelente_servicio_finisht = data.count('EXCELENTE SERVICIO.\n\n')
            all_count_exelente_servicio_finisht += count_exelente_servicio_finisht
            # calculate points for excelente servicio
            if count_exelente_servicio_finisht > 0:
                all_points_count_exelente_servicio_finisht += 100
            # --------------------------------------- count for EXCELENTE SERVICIO ------------------------------------|
            count_exelente_servicio = data.count('EXCELENTE SERVICIO')
            all_count_exelente_servicio_include += count_exelente_servicio
            if count_exelente_servicio - count_exelente_servicio_finisht > 0:
                all_points_count_exelente_servicio_include += 10
            # ------------------------------------------ count times --------------------------------------------------|
            results_list_line_conversaiton = list(filter(lambda x: (len(x) > 0), data.split('\n')))[1:]
            time_init = results_list_line_conversaiton[0][:8]
            time_finisht = results_list_line_conversaiton[len(results_list_line_conversaiton) - 1][:8]
            # convert string time to datetime
            time_init = datetime.strptime(time_init, '%H:%M:%S')
            time_finisht = datetime.strptime(time_finisht, '%H:%M:%S')
            difference_time = time_finisht - time_init
            # check if > to one minute
            if difference_time.seconds >= 60:
                all_count_time_seconds_max_60 += 1
                all_points_count_time_seconds_max_60 += 25
            else:
                all_count_time_seconds_min_60 += 1
                all_points_count_time_seconds_min_60 += 50
            # ----------------------------------------- count chat abandoned -----------------------------------------|
            if len(results_list_line_conversaiton) == 1:
                all_count_abandonated_chat += 1
                all_points_count_abandonated_chat -= 100
    # calculate diff EXCELENTE SERVICIO
    all_count_exelente_servicio_include = all_count_exelente_servicio_include - all_count_exelente_servicio_finisht
    # calculate points
    total_points = (all_points_count_enter + all_points_count_urgente + all_points_count_exelente_servicio_include
        + all_points_count_exelente_servicio_finisht + all_points_count_time_seconds_min_60 + all_points_count_time_seconds_max_60
        + all_points_count_abandonated_chat)
    # calculate stars
    if total_points < 0:
        stars = 0
    elif 0 <= total_points < 25:
        stars = 1
    elif 25 <= total_points < 50:
        stars = 2
    elif 50 <= total_points < 75:
        stars = 3
    elif 75 <= total_points < 90:
        stars = 4
    else:
        stars = 5
    response = {
        'total_points': total_points,
        'stars': stars,
        'count_files': len(list_files),
        'results': [
            {'name': 'Total Enter', 'total_point': all_points_count_enter, 'total_count': all_count_enter},
            {'name': 'Total Urgente', 'total_point': all_points_count_urgente, 'total_count': all_count_urgente},
            {
                'name': 'Total Excelente Servicio',
                'total_point': all_points_count_exelente_servicio_finisht + all_points_count_exelente_servicio_include,
                'total_count': all_count_exelente_servicio_include + all_count_exelente_servicio_finisht
            },
            {
                'name': 'Total Numero Duracion ( > 1 M)',
                'total_point': all_points_count_time_seconds_max_60,
                'total_count': all_count_time_seconds_max_60,
            },
            {
                'name': 'Total Numero Duracion ( < 1 M)',
                'total_point': all_points_count_time_seconds_min_60,
                'total_count': all_count_time_seconds_min_60,
            },
            {
                'name': 'Total Chat Abandonado',
                'total_point': all_points_count_abandonated_chat,
                'total_count': all_count_abandonated_chat,
            }
        ]
    }
    return jsonify(response), 200