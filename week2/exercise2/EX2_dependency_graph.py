import os
from datetime import datetime
def log_as_dictionary(log):
    # return a dictionary with the following structure:
    # Task_G;case_1;user_6;2019-09-18 19:14:14
    # Task_G;case_2;user_6;2019-09-19 15:39:15
    # Task_H;case_1;user_2;2019-09-19 16:48:16
    # Task_E;case_2;user_7;2019-09-20 14:39:45
    # Task_F;case_2;user_8;2019-09-22 09:16:16
    dict_log = {}
    for line in log.split('\n'):
        if line:
            task, case, user, date = line.split(';')
            # store the case as a key in the dictionary
            if case not in dict_log:
                dict_log[case] = []
            # store the task, user, and date as a list in the list
            dict_log[case].append([task, user, date])
    return dict_log

def dependency_graph_inline(log) :
    dg = {}
    # loop through the cases in the log
    for key in log.keys():
        # loop through the tasks in the case
        for i in range(len(log[key])-1):
            # get the task name of the current case
            ai = log[key][i][0]
            # print(ai)
            # get the next task name of the current case
            aj = log[key][i+1][0]
            # print(aj)
            if ai not in dg:
                dg[ai] = {}
            if aj not in dg[ai]:
                # set the dependency count to 0
                dg[ai][aj] = 0
            # increment the count of the dependency
            dg[ai][aj] += 1
    # test the output of the dictionary
    # print("output of the dg",dg)
    return dg
    
def read_from_file(path):
    log = {}
    # construct the file path
    path = os.path.join(os.path.dirname(__file__), path)
    # print("path",path)
    with open(path, 'r') as file:
        # print("filename",file)
        # read the xml file
        xml = file.read()
        # print("xml",xml)
        # get the cases from the xml file
        cases = xml.split('<trace>')
        # print("cases",cases)
        # loop through the cases
        for case in cases[1:]:
            # get the case id
            case_id = case.split('<string key="concept:name" value="')[1].split('"/>')[0]
            # get the events of the case
            events = case.split('<event>')
            # store the events in the log
            log[case_id] = []
            for event in events[1:]:
                # get the event details
                if '<string key="concept:name" value="' in event:
                    task = event.split('<string key="concept:name" value="')[1].split('"/>')[0]
                    user = event.split('<string key="org:resource" value="')[1].split('"/>')[0]
                    date = event.split('<date key="time:timestamp" value="')[1].split('"/>')[0]
                    # transfer the date to a datetime object
                    # datetime.datetime(1970, 1, 1, 1, 0)
                    # time format : 1970-01-01T01:00:00+01:00
                    # extract the date and time
                    date = date.split('T')
                    # extract the year, month, and day
                    year, month, day = date[0].split('-')
                    # extract the hour, minute, and second
                    hour, minute,second = date[1].split(':')[:3]
                    # create a datetime object
                    date = datetime(int(year), int(month), int(day), int(hour), int(minute))
                    cost = int(event.split('<int key="cost" value="')[1].split('"/>')[0])
                    # store the event in the log
                    log[case_id].append({"concept:name": task, "org:resource": user, "time:timestamp": date, "cost": cost})
    return log

def dependency_graph_file(log):
    df = {}
    # loop through the cases in the log
    for key in log.keys():
        # loop through the tasks in the case
        for i in range(len(log[key])-1):
            # get the task name of the current case
            ai = log[key][i]["concept:name"]
            # print(ai)
            # get the next task name of the current case
            aj = log[key][i+1]["concept:name"]
            # print(aj)
            if ai not in df:
                df[ai] = {}
            if aj not in df[ai]:
                # set the dependency count to 0
                df[ai][aj] = 0
            # increment the count of the dependency
            df[ai][aj] += 1
    # test the output of the dictionary
    # print("output of the dg",dg)
    return df

f = """
Task_A;case_1;user_1;2019-09-09 17:36:47
Task_B;case_1;user_3;2019-09-11 09:11:13
Task_D;case_1;user_6;2019-09-12 10:00:12
Task_E;case_1;user_7;2019-09-12 18:21:32
Task_F;case_1;user_8;2019-09-13 13:27:41

Task_A;case_2;user_2;2019-09-14 08:56:09
Task_B;case_2;user_3;2019-09-14 09:36:02
Task_D;case_2;user_5;2019-09-15 10:16:40

Task_G;case_1;user_6;2019-09-18 19:14:14
Task_G;case_2;user_6;2019-09-19 15:39:15
Task_H;case_1;user_2;2019-09-19 16:48:16
Task_E;case_2;user_7;2019-09-20 14:39:45
Task_F;case_2;user_8;2019-09-22 09:16:16

Task_A;case_3;user_2;2019-09-25 08:39:24
Task_H;case_2;user_1;2019-09-26 12:19:46
Task_B;case_3;user_4;2019-09-29 10:56:14
Task_C;case_3;user_1;2019-09-30 15:41:22"""

log = log_as_dictionary(f)
# print(log)
dg = dependency_graph_inline(log)

for ai in sorted(dg.keys()):
   for aj in sorted(dg[ai].keys()):
       print (ai, '->', aj, ':', dg[ai][aj])
       
# output of the dg dictionary:
# Task_A -> Task_B : 3
# Task_B -> Task_C : 1
# Task_B -> Task_D : 2
# Task_D -> Task_E : 1
# Task_D -> Task_G : 1
# Task_E -> Task_F : 2
# Task_F -> Task_G : 1
# Task_F -> Task_H : 1
# Task_G -> Task_E : 1
# Task_G -> Task_H : 1

log = read_from_file("extension-log.xes")

# general statistics: for each case id the number of events contained
for case_id in sorted(log):
    print((case_id, len(log[case_id])))

# details for a specific event of one case
case_id = "case_123"
event_no = 0
print((log[case_id][event_no]["concept:name"], log[case_id][event_no]["org:resource"], log[case_id][event_no]["time:timestamp"],  log[case_id][event_no]["cost"]))
# the return log format : ('record issue', 'admin-1', datetime.datetime(1970, 1, 1, 1, 0), 11)