import json
import re

data = json.loads(input())
type_errors_dict = {"bus_id": 0, "stop_id": 0, "stop_name": 0, "next_stop": 0, "stop_type": 0, "a_time": 0}
format_errors_dict = {"stop_name": 0, "stop_type": 0, "a_time": 0}
lines = []
lines_stops = {}
lines_stop_types = {}
lines_a_times = {}
bad_a_time_stop = {}
start_stops = set()
finish_stops = set()
transfer_stops = set()
stops_on_demand = set()
stops = set()
for bus in data:
    bus_id = bus["bus_id"]
    if not isinstance(bus_id, int) or len(str(bus_id)) == 0:
        type_errors_dict["bus_id"] += 1
    else:
        if bus_id not in lines:
            lines.append(bus_id)
            lines_stops[str(bus_id)] = set()
            lines_stop_types[str(bus_id)] = []
            lines_a_times[str(bus_id)] = []
            bad_a_time_stop[str(bus_id)] = []
        elif len(bad_a_time_stop[str(bus_id)]) > 0:
            continue
    stop_id = bus["stop_id"]
    if not isinstance(stop_id, int) or len(str(stop_id)) == 0:
        type_errors_dict["stop_id"] += 1
    stop_name = bus["stop_name"]
    if not isinstance(stop_name, str) or len(str(stop_name)) == 0:
        type_errors_dict["stop_name"] += 1
    else:
        if not re.match("[A-Z]\\w+\\s?\\w+?\\s(Road|Avenue|Boulevard|Street)$", stop_name):
            format_errors_dict["stop_name"] += 1
        else:
            lines_stops[str(bus_id)].add(stop_name)
            if stop_name in stops:
                transfer_stops.add(stop_name)
            else:
                stops.add(stop_name)
    next_stop = bus["next_stop"]
    if not isinstance(next_stop, int) or len(str(next_stop)) == 0:
        type_errors_dict["next_stop"] += 1
    stop_type = bus["stop_type"]
    if not isinstance(stop_type, str) or len(str(stop_type)) > 1:
        type_errors_dict["stop_type"] += 1
    if len(str(stop_type)) > 1 or (len(str(stop_type)) == 1 and not re.match("^(S|O|F)+?$", stop_type)):
        format_errors_dict["stop_type"] += 1
    else:
        lines_stop_types[str(bus_id)].append(stop_type)
        if stop_type == 'S':
            start_stops.add(stop_name)
        elif stop_type == 'F':
            finish_stops.add(stop_name)
        elif stop_type == 'O':
            stops_on_demand.add(stop_name)
    a_time = bus["a_time"]
    if not isinstance(a_time, str) or len(str(a_time)) == 0:
        type_errors_dict["a_time"] += 1
    else:
        if not re.match("^(0|1|2)[0-9]:[0-5][0-9]$", a_time):
            format_errors_dict["a_time"] += 1
        else:
            if len(lines_a_times[str(bus_id)]) > 0 and lines_a_times[str(bus_id)][-1] >= a_time:
                bad_a_time_stop[str(bus_id)].append(stop_name)
            else:
                lines_a_times[str(bus_id)].append(a_time)


def fieldValidation():
    print("Type and required field validation:", sum(type_errors_dict.values()), "errors")
    for d in type_errors_dict:
        print(d + ":", type_errors_dict[d])


def formatValidation():
    print("Format validation:", sum(format_errors_dict.values()), "errors")
    for d in format_errors_dict:
        print(d + ":", format_errors_dict[d])


def stopsValidation():
    bad_line = ''
    for line in lines_stops:
        if not ((lines_stop_types[line].count('S') == 1) and (lines_stop_types[line].count('F') == 1)):
            bad_line = line
            break

    if bad_line:
        print('There is no start or end stop for the line:', bad_line)
    else:
        print('Start stops:', len(start_stops), sorted(start_stops))
        print('Transfer stops:', len(transfer_stops), sorted(transfer_stops))
        print('Finish stops:', len(finish_stops), sorted(finish_stops))


def arrivalTimeCheck():
    print('Arrival time test:')
    all_right = True
    for line in bad_a_time_stop:
        if len(bad_a_time_stop[line]) > 0:
            print('bus_id line {}: wrong time on station {}'.format(line, *bad_a_time_stop[line]))
            all_right = False
    if all_right:
        print('OK')

def ondemandCheck():
    print('On demand stops test:')
    wrong = set()
    for on_demand in stops_on_demand:
        if on_demand in start_stops or on_demand in finish_stops or on_demand in transfer_stops:
            wrong.add(on_demand)
    if len(wrong) == 0:
        print('OK')
    else:
        print('Wrong stop type:', sorted(wrong))

ondemandCheck()
