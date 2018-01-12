from PyQt5 import QtCore
import logging
import random
from battle_field.slam import least_squares_method
from battle_field.common import geometry
# RANSAC = Random Sampling Consensus
# is a method which can be used to extract lines from a laser scan.
# These lines can in turn be used as landmarks.
# In indoor environments straight lines are often observed by laser scans as
# these are characteristic of straight walls which usually are common.
# RANSAC interfaces -> input: list of lidar measurements


LOG = logging.getLogger(__name__)


class RANSAC():
    # N
    # count of attempts to create line
    MAX_NUMBER_OF_ATTEMPTS = 0
    # S
    # count of dots from lidar measurement for find line
    # in FIRST iteration of line creating
    NUMBER_OF_SAMPLES = 0
    # D
    # neighborhood around dot in degrees for get NUMBER_OF_SAMPLES dots
    # around sample single dot
    SAMPLES_DEGREE_RANGE = 0

    # assume, that we have 1 measurement per one degree.
    # we need this parameter for getting sample of dots
    COUNT_OF_MEASUREMENTS_PER_DEGREE = 1

    # X
    # if dist between dot and line < MAX_BINDING_DIST_TO_LINE
    # so we assume that dot belong to line
    MAX_BINDING_DIST_TO_LINE = 0
    # C
    # minimum count of binded dots for creating line
    CONSENSUS = 0

    # you can use RANSAC only if initialization return true
    # should be initialize first
    def initialization(
        self,
        max_number_of_attempts=0,
        number_of_samples=0,
        samples_degree_range=0,
        max_binding_dist_to_line=0,
            consensus=0):
        if (max_number_of_attempts <= 0 or
                number_of_samples <= 2 or
                samples_degree_range <= 0 or
                max_binding_dist_to_line < 0 or
                consensus <= 2):
            return False
        else:
            self.MAX_NUMBER_OF_ATTEMPTS = max_number_of_attempts
            self.NUMBER_OF_SAMPLES = number_of_samples
            self.SAMPLES_DEGREE_RANGE = samples_degree_range
            self.MAX_BINDING_DIST_TO_LINE = max_binding_dist_to_line
            self.CONSENSUS = consensus
            return True

    # should be initialized second
    def initialization_lidar_info(
        self,
            count_of_measurements_per_degree):
        if (count_of_measurements_per_degree > 0):
            self.COUNT_OF_MEASUREMENTS_PER_DEGREE = (
                count_of_measurements_per_degree)
            return True
        else:
            return False

    # process lidar list of measurements in cartesian
    # input: [(x1,y1),(x2,y2), ... (xN, yN)]
    # return list of tuples line + line pars
    # [(line1->QLineF, line_pars1), (line2->QLineF, line_pars2), ... ]
    def process_cartesian(self, lidar_measurements):

        identified_lines = []
        trials = 0
        unassociated_lidar_measurements = {
            index: value for index, value in enumerate(
                lidar_measurements) if value is not None
        }
        while (
            (len(unassociated_lidar_measurements) > self.CONSENSUS) and (
                trials < self.MAX_NUMBER_OF_ATTEMPTS)):
            # increment trials count
            trials += 1
            # get random unassociated_lidar_measurement
            keys = list(unassociated_lidar_measurements.keys())
            random_index = random.choice(
                keys)
            # LOG.critical("random_index: %s" % (random_index,))
            random_sample_indexes = self.get_random_indexes_in_range(
                unassociated_lidar_measurements,
                random_index,
                self.NUMBER_OF_SAMPLES,
                self.SAMPLES_DEGREE_RANGE,
                self.COUNT_OF_MEASUREMENTS_PER_DEGREE)
            if random_sample_indexes is None:
                # LOG.critical("random_sample_indexes is None")
                pass
                # we don't have additional dots in our condition near
                # random dot, so lets try again but we already use trial...
            else:
                sample = []
                if random_index not in unassociated_lidar_measurements.keys():
                    LOG.critical("wrong random index: %s" % (random_index,))
                sample.append(
                    unassociated_lidar_measurements[
                        random_index])
                for random_sample_index in random_sample_indexes:
                    sample.append(
                        unassociated_lidar_measurements[
                            random_sample_index])
                line_parameters = least_squares_method.approximate_line(
                    sample)
                line = geometry.create_line_by_pars(line_parameters)
                associated_measurements = (
                    self.filter_measurement_by_distance_to_line(
                        unassociated_lidar_measurements,
                        line,
                        self.MAX_BINDING_DIST_TO_LINE))
                if len(associated_measurements) < self.CONSENSUS:
                    # LOG.critical(
                        # "len(associated_measurements) < self.CONSENSUS do nothing")
                    pass
                    # unsuccessfully attempt, lets have another one,
                    # but we used one trial
                else:
                    associated_measurements_list = [
                        value for key, value in
                        associated_measurements.items()]
                    specified_line_parameters = (
                        least_squares_method.approximate_line(
                            associated_measurements_list))
                    specified_line = geometry.create_line_by_pars(
                        specified_line_parameters)
                    specified_line_resized = (
                        self.resize_line_according_measurements(
                            specified_line,
                            associated_measurements_list))
                    identified_lines.append(
                        (specified_line_resized, specified_line_parameters))
                    # clean associated dots from unassociated measurements
                    unassociated_lidar_measurements = {
                        k: v for k, v in
                        unassociated_lidar_measurements.items()
                        if k not in associated_measurements}
        return identified_lines

    # function get random "number_of_samples" samples from
    # unassociated_lidar_measurements in "samples_degree_range" range
    # unassociated_lidar_measurements - dict
    # {index_1: (x1, y1), index_2: (x2, y2), ...}
    # return:
    # list of samples indexes in unassociated_lidar_measurements
    # or None if there are no valid samples in dict
    def get_random_indexes_in_range(
        self,
        unassociated_lidar_measurements,
        sample_dot_key,
        number_of_samples,
        samples_degree_range,
            count_of_measurements_per_degree):
        keys = unassociated_lidar_measurements.keys()
        keys = sorted(
            keys,
            key=lambda value: value)
        range_in_keys = samples_degree_range / count_of_measurements_per_degree
        keys_in_range = [i for i in keys if (
            i > sample_dot_key - (range_in_keys / 2)) and (
            i < sample_dot_key + (range_in_keys / 2))]
        if len(keys_in_range) < number_of_samples:
            return None
        random_keys = []
        for i in range(0, number_of_samples, 1):
            new_key = random.choice(keys_in_range)
            keys_in_range.remove(new_key)
            random_keys.append(new_key)
        return random_keys

    # function return list of tuples
    # {index_1: (x1, y1), index_2: (x2, y2), ... }
    # return dict: {index_1: (x1, y1), index_2: (x2, y2), ....}
    def filter_measurement_by_distance_to_line(
        self,
        unassociated_lidar_measurements,
        line,
            distance):
        filtered_measures = {}
        normal_line = line.normalVector()
        for index, dot in unassociated_lidar_measurements.items():
            intersect_dot = geometry.intersect_by_secant(
                QtCore.QPointF(
                    dot[0], dot[1]),
                normal_line,
                (line,),
                check_line_contain_point=False)
            if len(intersect_dot) != 1:
                LOG.critical(
                    "RANSAC: ERROR in filter_measurement_by_distance_to_line")
            if (QtCore.QLineF(
                    intersect_dot[0], QtCore.QPointF(
                        dot[0],
                        dot[1])).length() <= distance):
                filtered_measures[index] = dot
        return filtered_measures

    # functions resize line by finding maximum and minimum
    # measurements
    # input:
    # line -> QLineF
    # associated_measurements - dict of dots
    # [(x1, y1), (x2, y2), ... ]
    # return resized line
    def resize_line_according_measurements(
        self,
        line,
            associated_measurements):
        normal_line = line.normalVector()
        # sort dict by index

        p1 = geometry.intersect_by_secant(
            QtCore.QPointF(
                associated_measurements[0][0],
                associated_measurements[0][1]),
            normal_line,
            (line,),
            check_line_contain_point=False)
        p2 = geometry.intersect_by_secant(
            QtCore.QPointF(
                associated_measurements[-1][0],
                associated_measurements[-1][1]),
            normal_line,
            (line,),
            check_line_contain_point=False)
        if (len(p1) != 1 or len(p2) != 1):
            LOG.critical("RANSAC ERROR resize_line_according_measurements")
        return QtCore.QLineF(p1[0], p2[0])
