from battle_field.items.devices_models import odometer_model
import unittest
import math


class TestOdometerModel(unittest.TestCase):

    count_of_slots = 10
    update_freq = 30
    callback_called_times = 0

    def callback(self, count_of_slots):
        self.callback_called_times += count_of_slots

    # test case 1.
    # residue = 0, positive rotation speed
    def test_positive_speed_empty_residue(self):
        # radians / sec
        self.callback_called_times = 0
        angle_speed_ps = 200 * math.pi * 30
        model = odometer_model.OdometerModel(
            self.count_of_slots,
            angle_speed_ps,
            self.update_freq,
            self.callback,
            None)
        model.update()
        self.assertEqual(
            self.callback_called_times,
            1000)
        self.assertTrue(
            model.residue < 0.001)

    # test case 2.
    # residue != 0, positive rotation speed
    def test_positive_speed_NOT_empty_residue(self):
        self.callback_called_times = 0
        angle_speed_ps = 200 * math.pi * 30
        model = odometer_model.OdometerModel(
            self.count_of_slots,
            angle_speed_ps,
            self.update_freq,
            self.callback,
            None)

        initial_residue = (2 * math.pi / self.count_of_slots) * 0.1
        model.residue = initial_residue
        model.update()
        self.assertEqual(
            self.callback_called_times,
            1000)
        self.assertTrue(
            math.fabs(
                model.residue -
                initial_residue) <
            0.00001)

    # test case 3.
    # residue != 0, changing rotation speed from positive to negative
    def test_change_speed_NOT_empty_residue(self):
        self.callback_called_times = 0
        angle_speed_ps = 200 * math.pi * 30
        model = odometer_model.OdometerModel(
            self.count_of_slots,
            angle_speed_ps,
            self.update_freq,
            self.callback,
            None)
        initial_residue = (2 * math.pi / self.count_of_slots) * 0.1
        model.residue = initial_residue
        model.update()
        model.change_speed(-2 * angle_speed_ps)
        model.update()
        self.assertEqual(
            self.callback_called_times,
            0)
        self.assertTrue(
            math.fabs(model.residue) -
            math.fabs(initial_residue) <
            0.0001)


if __name__ == '__main__':
    unittest.main()
