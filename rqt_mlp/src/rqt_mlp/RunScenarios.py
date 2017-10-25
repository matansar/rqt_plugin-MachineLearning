#!/usr/bin/env python
## Phase 1

import inspect, os
NO_COND = -9999
## for randomlay
scn_counter_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "/Scenarios/Extentions/tmp/scenarios_counter.tmp"



topics_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "/topics/"


class RunScenario:
    # ------------------------------------------------------------ constructor ------------------------------------------------------------

    # selected_scenario = {id = "", params = {x: value_x}}
    def __init__(self, bag_obj, export_bag, selected_scenario, selected_topics):
        must_topics = ['/host_statistics', '/node_statistics', '/statistics', "/move_base/feedback"]
        self.__restart_flag = False
        self.__bag_obj = bag_obj
        self.__export_bag = export_bag
        self.__selected_scenario = selected_scenario
        self.__selected_topics = list(set(selected_topics + must_topics))

    # ------------------------------------------------------------ getters ------------------------------------------------------------

    def get_export_bag(self):
        return self.__export_bag

    def get_selected_scenario(self):
        return self.__selected_scenario

    # ------------------------------------------------------------ setters ------------------------------------------------------------

    def add_temporal_filename(self, number):
        self.__export_bag = "%s_%s.bag" % (self.__export_bag[:-4], number)

    def turn_on_restart_flag(self):
        self.__restart_flag = True

    # ------------------------------------------------------------ functionality ------------------------------------------------------------

    # def apply_record_icon(self):
    #     self.__bag_obj.apply_record_icon()

    def run_record_scenario(self):
        scn_id = self.__selected_scenario['id']
        params = RunScenario.__get_scenarios_params(scn_id)
        operands = [self]
        for param in params:
            operands.append(self.__selected_scenario['params'][param])
        operator = (scenarios[scn_id])['function']
        operator(*operands)

    def generate_bag(self):
        self.__bag_obj.record_bag(self.__export_bag, False, self.__selected_topics)

    def close_bag(self):
        if not self.__restart_flag:
            if os.path.exists(scn_counter_path):
                os.remove(scn_counter_path)
        self.__bag_obj.restart_recording(self.__restart_flag)

    @staticmethod
    def __get_scenarios_params(scn_id):
        global scenarios
        print str(scenarios)
        return list(scenarios[scn_id]['params'])



# ------------------------------------------------------------ scenarios ------------------------------------------------------------

def source_destination_scenario(scn_obj, source_x, source_y, angle, distance):
    import Source_Dest_Scenario as sds
    sds.Run_Scenario(scn_obj, source_x, source_y, angle, distance)

def randomaly_source_destionation_scenario(scn_obj, number_simulations):
    import Randomaly_Source_Dest_Scenario as rsds
    create_restarting_file(scn_obj)
    # scn_obj.add_temporal_filename(number_simulations)
    rsds.Run_Scenario(scn_obj, number_simulations)

def obstacle_source_destination_scenario(scn_obj, source_x, source_y, angle, distance):
    import Obstacle_Source_Dest_Scenario as osds
    osds.Run_Scenario(scn_obj, source_x, source_y, angle, distance)

def randomaly_obstacle_source_destination_scenario(scn_obj, number_simulations):
    import Randomaly_Obstacle_Source_Dest_Scenario as rosds
    create_restarting_file(scn_obj)
    #
    rosds.Run_Scenario(scn_obj, number_simulations)


# ------------------------------------------------

def create_restarting_file(scn_obj):
    filename = scn_obj.get_export_bag()
    selected_scenario = scn_obj.get_selected_scenario()
    first_key = selected_scenario['params'].keys()[0]
    (selected_scenario['params'])[first_key] = int((selected_scenario['params'])[first_key])
    if (selected_scenario['params'])[first_key] < 1:
        # scn_obj.apply_record_icon()
        os.remove(scn_counter_path)
    else:
        import time
        if (selected_scenario['params'])[first_key] > 1:
            # print "hihihihihihi = %s " % (selected_scenario['params'])[first_key]

            # time.sleep(10)
            scn_obj.turn_on_restart_flag()
        (selected_scenario['params'])[first_key] = (selected_scenario['params'])[first_key] - 1
        # time.sleep(5)
        if os.path.exists(scn_counter_path):
            with open(scn_counter_path, 'r') as f:
                scn_number = int(f.read().splitlines()[1])
        else:
            scn_number = 0
        scn_obj.add_temporal_filename(scn_number)
        scn_number = scn_number + 1
        with open(scn_counter_path, 'w') as f:
            f.write(filename + '\n')
            f.write(str(scn_number) + '\n')
            f.write(str(selected_scenario))



# ------------------------------------------------------------ private functions ------------------------------------------------------------


# ----------------------------------------------------------------- global variables --------------------------------------------------------

scenarios = {}


# ----------------------------------------------------------------- global getters -----------------------------------------------------------



def get_scenarios_options():
    scenarios = create_scenarios()
    ret = {}
    for scn_id, scenario in scenarios.items():
        choise = dict(name=scenario["name"], params=list(scenario["params"]))
        ret[scn_id] = choise
    return ret


def get_topics_options():
    def get_topics_files(dir_path, suffix):
        files = [f for f in os.listdir(dir_path) if f[-len(suffix):] == suffix]
        return files

    files = get_topics_files(topics_directory, '.txt')
    ret = {}
    for f in files:
        topic_subject = f[:-4]  # get off '.txt' suffix
        content = ""
        with open(topics_directory + f) as read_f:
            content = [x.strip() for x in read_f.readlines()]  # remove whitespace
        ret[topic_subject] = content
    return ret


# ----------------------------------------------------------------- initializations ------------------------------------------------------

def create_scenarios():
    # scenarios 1 -----------------------------------
    tmp_scenarios = {}
    scenario_id = 1
    name = "walking without obstacles from specific source to specific destination"
    ## param, label, condition
    params = [('source x','', NO_COND), ('source y','', NO_COND), ('angle (rad)','', NO_COND), ('distance', 'greater than zero', 0)]
    function = source_destination_scenario
    tmp_scenarios[scenario_id] = dict(name=name, params=params, function=function)
    # scenarios 2 -----------------------------------
    scenario_id = 2
    name = "walking randomly without obstacles from source to destination"
    params = [('number of simulations', 'greater than zero', 0)]
    function = randomaly_source_destionation_scenario
    tmp_scenarios[scenario_id] = dict(name=name, params=params, function=function)
    # scenarios 1 -----------------------------------
    scenario_id = 3
    name = "walking with an obstacle from specific source to specific destination"
    params = [('source x', '', NO_COND), ('source y', '', NO_COND), ('angle (rad)', '', NO_COND), ('distance', 'greater than 3', 3)]
    function = obstacle_source_destination_scenario
    tmp_scenarios[scenario_id] = dict(name=name, params=params, function=function)
    # scenarios 2 -----------------------------------
    scenario_id = 4
    name = "walking randomly with an obstacle from source to destination"
    params = [('number of simulations', 'greater than zero', 0)]
    function = randomaly_obstacle_source_destination_scenario
    tmp_scenarios[scenario_id] = dict(name=name, params=params, function=function)
    return tmp_scenarios

def init_scenarios():
    global scenarios
    tmp_scenarios = create_scenarios()
    for scn_id, scenario in tmp_scenarios.items():
        params = (tmp_scenarios[scn_id])['params']
        new_params = []
        for param in params:
            new_params.append(param[0])
        (tmp_scenarios[scn_id])['params'] = new_params
    scenarios = tmp_scenarios

# to import dynamically a py_file from another directory
def import_dynamically(path):
    import sys
    sys.path.insert(0, path)


init_scenarios()
import_dynamically(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "/Scenarios/")


# if __name__ == '__main__':
# selected_scenario = {"id" : 1, "params" : {'source x': 1 , 'source y': 2, 'destination x': 3, 'destination y': 4}}
# rs = RunScenario(selected_scenario, [])
# rs.generate_bag_file("asdasd")