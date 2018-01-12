import unittest
import logging

from battle_field.common import coordinates_conversion

LOG = logging.getLogger(__name__)
LOG.critical("CoordinatesConversionTest start")


# measure
class CoordinatesConversionTest(unittest.TestCase):

    # move line
    def test_coordinates_conversion(self):
        # double conversion tests 1000, 190 degrees
        coord_polar = (1000, 190)
        cartesian = coordinates_conversion.convert_polar_to_cartesian(
            coord_polar)
        coord_polar_new = (
            coordinates_conversion.convert_cartesian_to_polar(
                cartesian))
        self.assertAlmostEqual(coord_polar[0], coord_polar_new[0])
        self.assertAlmostEqual(coord_polar[1], coord_polar_new[1] + 360)
        # 400, 270 degrees
        coord_polar = (400, 270)
        cartesian = coordinates_conversion.convert_polar_to_cartesian(
            coord_polar)
        coord_polar_new = (
            coordinates_conversion.convert_cartesian_to_polar(
                cartesian))
        self.assertAlmostEqual(coord_polar[0], coord_polar_new[0])
        self.assertAlmostEqual(coord_polar[1], coord_polar_new[1] + 360)
        # check convertion cartesian to polar by x = 0 -> atan division by zero
        coordinates_conversion.convert_cartesian_to_polar((0, 100))
        coordinates_conversion.convert_cartesian_to_polar((0, 0))
        # test conversion with offset
        coord_cartesian = (
            coordinates_conversion.convert_polar_to_cartesian_with_offset(
                (100, 0), (100, 100)))
        self.assertAlmostEqual(coord_cartesian[0], 200)
        self.assertAlmostEqual(coord_cartesian[1], 100)


if __name__ == '__main__':
    unittest.main()
