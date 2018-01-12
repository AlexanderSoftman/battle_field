import unittest
import logging
import random
import math
from PyQt5 import QtCore

from battle_field.slam import RANSAC


LOG = logging.getLogger(__name__)
LOG.critical("RANSACTest start")


# measure
class RANSACTest(unittest.TestCase):
    max_number_of_attempts = 20
    number_of_samples = 10
    samples_degree_range = 50
    max_binding_dist_to_line = 3
    consensus = 40
    count_of_measurements_per_degree = 1
    small_error = 0.5
    medium_error = 2
    big_error = 10

    def test_process_cartesian_one_line_no_noise(self):
        for i in range(0, 100):
            init_line_pars = (1, 0)
            sample = []
            # 20 empty dots
            for x in range(0, 20):
                sample.append(None)
            # 100 dots on line
            for x in range(20, 120):
                sample.append((x, x))
            for x in range(120, 180):
                sample.append(None)
            RANSAC_m = RANSAC.RANSAC()
            self.assertTrue(RANSAC_m.initialization(
                self.max_number_of_attempts,
                self.number_of_samples,
                self.samples_degree_range,
                self.max_binding_dist_to_line,
                self.consensus))
            RANSAC_m.initialization_lidar_info(
                self.count_of_measurements_per_degree)
            lines = RANSAC_m.process_cartesian(sample)
            # LOG.critical("lines: %s" % (lines,))
            self.assertEqual(len(lines), 1)
            self.assertEqual(lines[0][1][0], init_line_pars[0])
            self.assertEqual(lines[0][1][1], init_line_pars[1])

    def test_process_cartesian_one_line_small_noise(self):
        for i in range(0, 100):
            init_line_pars = (1, 0)
            sample = []
            # 20 empty dots
            for x in range(0, 20):
                sample.append(None)
            # 100 dots on line
            for x in range(20, 120):
                sample.append((x, x))
            for x in range(120, 180):
                sample.append(None)
            sample_noised = []
            for value in sample:
                if value is not None:
                    sample_noised.append((
                        value[0] + random.uniform(-1, 1),
                        value[1] + random.uniform(-1, 1)))
                else:
                    sample_noised.append(None)
            RANSAC_m = RANSAC.RANSAC()
            self.assertTrue(RANSAC_m.initialization(
                self.max_number_of_attempts,
                self.number_of_samples,
                self.samples_degree_range,
                self.max_binding_dist_to_line,
                self.consensus))
            RANSAC_m.initialization_lidar_info(
                self.count_of_measurements_per_degree)
            lines = RANSAC_m.process_cartesian(sample_noised)
            # LOG.critical("counter: %s" % (i,))
            # LOG.critical("one line small noise res lines: %s" % (lines,))
            # LOG.critical("k: %s, b: %s, init k: %s, init b: %s" % (
                # lines[0][1][0],
                # lines[0][1][1],
                # init_line_pars[0],
                # init_line_pars[1]))
            self.assertTrue(len(lines) > 0)
            for line in lines:
                self.assertTrue(
                    math.fabs(
                        line[1][0] - init_line_pars[0]) <= self.small_error)
                self.assertTrue(
                    math.fabs(
                        line[1][1] - init_line_pars[1]) <= self.medium_error)

    def test_process_cartesian_one_line_medium_noise(self):
        for i in range(0, 100):
            init_line_pars = (1, 0)
            sample = []
            # 20 empty dots
            for x in range(0, 20):
                sample.append(None)
            # 100 dots on line
            for x in range(20, 120):
                sample.append((x, x))
            for x in range(120, 180):
                sample.append(None)
            sample_noised = []
            for value in sample:
                if value is not None:
                    sample_noised.append((
                        value[0] + random.uniform(-3, 3),
                        value[1] + random.uniform(-3, 3)))
                else:
                    sample_noised.append(None)
            RANSAC_m = RANSAC.RANSAC()
            self.assertTrue(RANSAC_m.initialization(
                self.max_number_of_attempts,
                self.number_of_samples,
                self.samples_degree_range,
                self.max_binding_dist_to_line,
                self.consensus))
            RANSAC_m.initialization_lidar_info(
                self.count_of_measurements_per_degree)
            lines = RANSAC_m.process_cartesian(sample_noised)
            # LOG.critical("counter: %s" % (i,))
            # LOG.critical("one line medium noise res lines: %s" % (lines,))
            # LOG.critical("k: %s, b: %s, init k: %s, init b: %s" % (
                # lines[0][1][0],
                # lines[0][1][1],
                # init_line_pars[0],
                # init_line_pars[1]))
            self.assertTrue(len(lines) > 0)
            for line in lines:
                self.assertTrue(
                    math.fabs(
                        line[1][0] - init_line_pars[0]) <= self.medium_error)
                self.assertTrue(
                    math.fabs(
                        line[1][1] - init_line_pars[1]) <= self.big_error)

    def test_process_cartesian_two_lines_no_noise(self):
        for i in range(0, 100):
            init_lines_pars = [(1, 0), (-1, 240)]
            sample = []
            # 20 empty dots
            for x in range(0, 20):
                sample.append(None)
            # 100 dots on line
            for x in range(20, 120):
                sample.append((x, x))
            for x in range(120, 180):
                sample.append((x, -x + 240))
            RANSAC_m = RANSAC.RANSAC()
            self.assertTrue(RANSAC_m.initialization(
                self.max_number_of_attempts,
                self.number_of_samples,
                self.samples_degree_range,
                self.max_binding_dist_to_line,
                self.consensus))
            RANSAC_m.initialization_lidar_info(
                self.count_of_measurements_per_degree)
            lines = RANSAC_m.process_cartesian(sample)
            # LOG.critical("lines: %s" % (lines,))
            self.assertTrue(len(lines) >= 2)
            self.assertTrue(
                math.fabs(
                    lines[0][1][0] - init_lines_pars[0][0]) <=
                self.medium_error or math.fabs(
                    lines[0][1][0] - init_lines_pars[1][0]) <=
                self.medium_error)
            self.assertTrue(
                math.fabs(
                    lines[0][1][1] - init_lines_pars[0][1]) <=
                self.big_error or math.fabs(
                    lines[0][1][1] - init_lines_pars[1][1]) <=
                self.big_error)
            self.assertTrue(
                math.fabs(
                    lines[1][1][0] - init_lines_pars[1][0]) <=
                self.medium_error or math.fabs(
                    lines[1][1][0] - init_lines_pars[0][0]) <=
                self.medium_error)
            self.assertTrue(
                math.fabs(
                    lines[1][1][1] - init_lines_pars[1][1]) <=
                self.big_error or math.fabs(
                    lines[1][1][1] - init_lines_pars[0][1]) <=
                self.big_error)

    def test_process_cartesian_two_lines_noise(self):
        for i in range(0, 100):
            init_lines_pars = [(1, 0), (-1, 240)]
            sample = []
            # 20 empty dots
            for x in range(0, 20):
                sample.append(None)
            # 100 dots on line
            for x in range(20, 120):
                sample.append((x, x))
            for x in range(120, 180):
                sample.append((x, -x + 240))
            sample_noised = []
            for value in sample:
                if value is not None:
                    sample_noised.append((
                        value[0] + random.uniform(-3, 3),
                        value[1] + random.uniform(-3, 3)))
                else:
                    sample_noised.append(None)
            RANSAC_m = RANSAC.RANSAC()
            self.assertTrue(RANSAC_m.initialization(
                self.max_number_of_attempts,
                self.number_of_samples,
                self.samples_degree_range,
                self.max_binding_dist_to_line,
                self.consensus))
            RANSAC_m.initialization_lidar_info(
                self.count_of_measurements_per_degree)
            lines = RANSAC_m.process_cartesian(sample_noised)
            # LOG.critical("lines: %s" % (lines,))
            self.assertTrue(len(lines) >= 2)
            for line in lines:
                self.assertTrue(
                    math.fabs(
                        line[1][0] - init_lines_pars[0][0]) <=
                    self.medium_error or math.fabs(
                        line[1][0] - init_lines_pars[1][0]) <=
                    self.medium_error or math.fabs(
                        line[1][0] - init_lines_pars[1][0]) <=
                    self.medium_error or math.fabs(
                        line[1][0] - init_lines_pars[0][0]) <=
                    self.medium_error)
                self.assertTrue(
                    math.fabs(
                        line[1][1] - init_lines_pars[0][1]) <=
                    3 * self.big_error or math.fabs(
                        line[1][1] - init_lines_pars[1][1]) <=
                    3 * self.big_error or math.fabs(
                        line[1][1] - init_lines_pars[1][1]) <=
                    3 * self.big_error or math.fabs(
                        line[1][1] - init_lines_pars[0][1]) <=
                    3 * self.big_error)

    def test_process_cartesian_noise_only(self):
        for i in range(0, 100):
            sample = []
            # 20 empty dots
            for x in range(0, 20):
                sample.append((
                    random.uniform(-10, 10),
                    random.uniform(-10, 10)))
            RANSAC_m = RANSAC.RANSAC()
            self.assertTrue(RANSAC_m.initialization(
                self.max_number_of_attempts,
                self.number_of_samples,
                self.samples_degree_range,
                self.max_binding_dist_to_line,
                self.consensus))
            RANSAC_m.initialization_lidar_info(
                self.count_of_measurements_per_degree)
            lines = RANSAC_m.process_cartesian(sample)
            # LOG.critical("lines: %s" % lines)
            self.assertTrue(len(lines) == 0)

    # move line
    def test_process_cartesian(self):
        return
        init_lines = [
            (0, 0), (20,), (0, 20), (-1, 60), (1, -60), (0, 20), (100,)]
        # sample = self.create_random_dots(init_lines, 20)
        sample = []
        for x in range(0, 20):
            sample.append((x, x * init_lines[0][0] + init_lines[0][1]))
        for y in range(0, 20):
            sample.append((init_lines[1][0], y))
        for x in range(20, 40):
            sample.append((x, x * init_lines[2][0] + init_lines[2][1]))
        for x in range(40, 60):
            sample.append((x, x * init_lines[3][0] + init_lines[3][1]))
        for x in range(60, 80):
            sample.append((x, x * init_lines[4][0] + init_lines[4][1]))
        for x in range(80, 100):
            sample.append((x, x * init_lines[5][0] + init_lines[5][1]))
        for y in range(20, 0, -1):
            sample.append((init_lines[6][0], y))
        # add values to dots
        sample_noised = []
        for value in sample:
            sample_noised.append((
                value[0] + random.uniform(-1, 1),
                value[1] + random.uniform(-1, 1)))
        RANSAC_m = RANSAC.RANSAC()
        self.assertTrue(RANSAC_m.initialization(
            self.max_number_of_attempts,
            self.number_of_samples,
            self.samples_degree_range,
            self.max_binding_dist_to_line,
            self.consensus))
        RANSAC_m.initialization_lidar_info(
            self.count_of_measurements_per_degree)
        lines = RANSAC_m.process_cartesian(sample_noised)
        # for init_line in init_lines:
            # LOG.critical("init_line: %s" % (
                # init_line,))
        # for line in lines:
            # LOG.critical("line: %s" % (
                # line,))
        self.assertEqual(len(lines), len(init_lines))

    def test_resize_line_according_measurements(self):
        RANSAC_m = RANSAC.RANSAC()
        self.assertTrue(RANSAC_m.initialization(
            self.max_number_of_attempts,
            self.number_of_samples,
            self.samples_degree_range,
            self.max_binding_dist_to_line,
            self.consensus))
        RANSAC_m.initialization_lidar_info(
            self.count_of_measurements_per_degree)
        initial_line = QtCore.QLineF(
            QtCore.QPointF(0, 0),
            QtCore.QPointF(1, 0))
        associated_measurements = [
            (-5, 0.0001),
            (-4, -0.0001),
            (0, 3 * 0.0001),
            (6.1, 3 * 0.0001)]
        resized_line = RANSAC_m.resize_line_according_measurements(
            initial_line,
            associated_measurements)
        self.assertTrue(resized_line.p1().x() == -5)
        self.assertTrue(resized_line.p2().x() == 6.1)

    def test_get_random_indexes_in_range(self):
        RANSAC_m = RANSAC.RANSAC()
        self.assertTrue(RANSAC_m.initialization(
            self.max_number_of_attempts,
            self.number_of_samples,
            self.samples_degree_range,
            self.max_binding_dist_to_line,
            self.consensus))
        RANSAC_m.initialization_lidar_info(
            self.count_of_measurements_per_degree)
        test_dots = {
            1: (1, 1),
            2: (2, 2),
            3: (3 + self.max_binding_dist_to_line, 3),
            4: (4 + 2 * self.max_binding_dist_to_line, 4),
            5: (
                5 + self.max_binding_dist_to_line,
                5 + self.max_binding_dist_to_line),
            6: (
                6 + self.max_binding_dist_to_line / 3,
                6 + self.max_binding_dist_to_line / 3),
            7: (
                -7 + self.max_binding_dist_to_line / 3,
                -7 + self.max_binding_dist_to_line / 3),
            8: (
                0 + self.max_binding_dist_to_line / 5,
                0 + self.max_binding_dist_to_line / 5),
            9: (
                9 + 5 * self.max_binding_dist_to_line,
                0 + 5 * self.max_binding_dist_to_line),
            10: (
                10 - 3 * self.max_binding_dist_to_line,
                10),
            11: (1, 1),
            12: (2, 2),
            13: (3 + self.max_binding_dist_to_line, 3),
            14: (4 + 2 * self.max_binding_dist_to_line, 4),
            15: (
                5 + self.max_binding_dist_to_line,
                5 + self.max_binding_dist_to_line),
            16: (
                6 + self.max_binding_dist_to_line / 3,
                6 + self.max_binding_dist_to_line / 3),
            17: (
                -7 + self.max_binding_dist_to_line / 3,
                -7 + self.max_binding_dist_to_line / 3),
            18: (
                0 + self.max_binding_dist_to_line / 5,
                0 + self.max_binding_dist_to_line / 5),
            19: (
                9 + 5 * self.max_binding_dist_to_line,
                0 + 5 * self.max_binding_dist_to_line),
            20: (
                10 - 3 * self.max_binding_dist_to_line,
                10)
        }

        sample_1 = RANSAC_m.get_random_indexes_in_range(
            test_dots,
            20,
            5,
            10,
            1)
        self.assertTrue(20 in sample_1)
        self.assertTrue(16 in sample_1)
        self.assertTrue(17 in sample_1)
        self.assertTrue(18 in sample_1)
        self.assertTrue(19 in sample_1)

        # LOG.critical("sample_1: %s" % (sample_1,))

        for i in range(0, 100, 1):
            sample_2 = RANSAC_m.get_random_indexes_in_range(
                test_dots,
                10,
                5,
                10,
                1)
            self.assertFalse(0 in sample_2)
            self.assertFalse(1 in sample_2)
            self.assertFalse(2 in sample_2)
            self.assertFalse(3 in sample_2)
            self.assertFalse(4 in sample_2)
            self.assertFalse(16 in sample_2)
            self.assertFalse(17 in sample_2)
            self.assertFalse(18 in sample_2)
            self.assertFalse(19 in sample_2)
            self.assertFalse(20 in sample_2)
            self.assertTrue(len(sample_2) == 5)
            # LOG.critical("sample_2: %s" % (sample_2))

        self.assertTrue(
            RANSAC_m.get_random_indexes_in_range(
                {},
                10,
                5,
                10,
                1) is None)

    def test_filter_measurement_by_distance_to_line(self):
        RANSAC_m = RANSAC.RANSAC()
        self.assertTrue(RANSAC_m.initialization(
            self.max_number_of_attempts,
            self.number_of_samples,
            self.samples_degree_range,
            self.max_binding_dist_to_line,
            self.consensus))
        RANSAC_m.initialization_lidar_info(
            self.count_of_measurements_per_degree)
        test_dots = {
            1: (1, 1),
            2: (2, 2),
            3: (3 + self.max_binding_dist_to_line, 3),
            4: (4 + 2 * self.max_binding_dist_to_line, 4),
            5: (
                5 + self.max_binding_dist_to_line,
                5 + self.max_binding_dist_to_line),
            6: (
                6 + self.max_binding_dist_to_line / 3,
                6 + self.max_binding_dist_to_line / 3),
            7: (
                -7 + self.max_binding_dist_to_line / 3,
                -7 + self.max_binding_dist_to_line / 3),
            8: (
                0 + self.max_binding_dist_to_line / 5,
                0 + self.max_binding_dist_to_line / 5),
            9: (
                9 + 5 * self.max_binding_dist_to_line,
                0 + 5 * self.max_binding_dist_to_line),
            10: (
                10 - 3 * self.max_binding_dist_to_line,
                10)
        }
        filtered_dots = RANSAC_m.filter_measurement_by_distance_to_line(
            test_dots,
            QtCore.QLineF(
                QtCore.QPointF(
                    0, 0),
                QtCore.QPointF(
                    1, 1)),
            self.max_binding_dist_to_line)
        self.assertTrue(1 in filtered_dots)
        self.assertTrue(2 in filtered_dots)
        self.assertTrue(3 in filtered_dots)
        self.assertFalse(4 in filtered_dots)
        self.assertTrue(5 in filtered_dots)
        self.assertTrue(6 in filtered_dots)
        self.assertTrue(7 in filtered_dots)
        self.assertTrue(8 in filtered_dots)
        self.assertFalse(9 in filtered_dots)
        self.assertFalse(10 in filtered_dots)

    # input - (k, b) if y = kx + b valid or (x) if x = 3
    def create_random_dots(self, lines, one_line_count_of_dots):
        dot_list = []
        x_init = 0
        for line in lines:
            for x in range(
                x_init,
                x_init + one_line_count_of_dots,
                    1):
                    if len(line) == 1:
                        dot_list.append((line[0], x))
                    elif len(line) == 2:
                        dot_list.append(
                            (x, line[0] * x + line[1]))
                    else:
                        # strange situation
                        pass
            x_init += one_line_count_of_dots
        return dot_list


if __name__ == '__main__':
    unittest.main()
