from PyQt5 import QtCore
from PyQt5 import QtWidgets
import logging

from battle_field.common import functions
from battle_field.common import geometry
from battle_field.items.vehicles.tank import bullet

LOG = logging.getLogger(__name__)


# LidarModel:
# make list of points of map around lidar in
# scan_sector (input parameter)
# make all calculation and save them to self.memory parameters
# which is list of tuples [(QPointF coordinate, trust_value 0..1), ...]
class LidarModel():

    # input values:
    # 1) timer_update_freq, Hz - frequency of call update
    # 2) sensor_update_freq, Hz - frequency of creating
    # full map by sensor
    # 3) scan_sector, degrees, positive value
    # 4) points in sector - count of points in sector WITHOUT BOUND POINTS!
    # 5) lidar_maximum_distace - maximum distance of measure
    # 6) carrier_item - reference to item, that physically
    # carry LIDAR
    # 7) error_model - model of error
    def __init__(
        self,
        timer_update_freq,
        sensor_update_freq,
        scan_sector,
        points_in_sector,
        lidar_maximum_distance,
        carrier_item,
            error_model):
        self.timer_updates_per_scan_update = int(
            timer_update_freq /
            sensor_update_freq)
        self.counter = 1
        self.lidars_half_angle = scan_sector / 2
        self.points_in_sector = points_in_sector
        self.lidar_maximum_distance = lidar_maximum_distance
        self.angle_step = scan_sector / (points_in_sector - 1)
        self.carrier_item = carrier_item
        self.error_model = error_model
        # lidars memory
        self.memory = []
        # scanning shape - ellipse
        self.build_sector_of_scanning()

    # we can scan map or not
    def update(self):
        if (self.counter ==
                self.timer_updates_per_scan_update):
            self.counter = 1
            self.scan_map(
                self.carrier_item.scenePos(),
                self.find_carrier_angle(
                    self.carrier_item))
        else:
            self.counter += 1

    # make map scanning from current scene_pos and
    # according to axis_angle
    # return:
    # list of values [(distance, measure_of_trust 0..1), (), ()]
    # input values:
    # 1) scene_pos of LIDAR
    # 2) angle of LIDAR's axis on scene
    def scan_map(self, LIDAR_pos_global, LIDAR_angle_global):
        # clean memory
        self.memory = []
        # find all items in vision
        items_in_vision = self.carrier_item.scene().collidingItems(
            self.scanning_shape)
        items_in_vision_filtered = self.filter_items_in_vision(
            items_in_vision)
        list_of_lines = []
        for item in items_in_vision_filtered:
            item_lines = functions.find_all_lines_in_my_sc(
                item, self.carrier_item)
            # LOG.debug("lines = %s" % (item_lines,))
            list_of_lines.extend(item_lines)
        line_angle = -self.lidars_half_angle
        for i in range(self.points_in_sector):
            global_result = self.find_single_line_result(
                line_angle,
                list_of_lines)
            # LOG.debug("global_result = %s" % (global_result,))
            self.memory.append(global_result)
            line_angle += self.angle_step

    # find intersection of single_line and first object on
    # single_lines way
    # return:
    # (distance, trust_value 0..1)
    # input:
    # scene_pos - QPointF of physically place of LIDAR
    # angle_of_measure in degrees
    def find_single_line_result(
        self,
        angle_of_measure,
            list_of_lines):
        lidar_line = QtCore.QLineF(
            QtCore.QPointF(0, 0),
            QtCore.QPointF(1, 0))
        lidar_line.setAngle(angle_of_measure)
        points_with_distance = []
        # find all intersections of this line
        for line in list_of_lines:
            point_of_intersection = QtCore.QPointF()
            intersection_type = lidar_line.intersect(
                line, point_of_intersection)
            if ((QtCore.QLineF.BoundedIntersection ==
                    intersection_type) or
                    (QtCore.QLineF.UnboundedIntersection ==
                        intersection_type)):
                if (
                    geometry.check_line_contains_point(
                        line, point_of_intersection)):
                    # go to global system coordinate
                    point_of_intersection_global = (
                        self.carrier_item.mapToScene(
                            point_of_intersection))
                    # LOG.debug(
                        # "point_of_intersection_global: %s" % (
                            # point_of_intersection_global,))
                    points_with_distance.append(
                        (point_of_intersection_global,
                            QtCore.QLineF(
                                self.carrier_item.mapToScene(
                                    QtCore.QPointF(0, 0)),
                                point_of_intersection_global).length()))
                    # LOG.debug(
                        # "points with dists: %s" % (
                            # points_with_distance[-1],))
        # sort our results
        if len(points_with_distance) != 0:
            points_with_distance = sorted(
                points_with_distance,
                key=lambda x: x[1])
            # LOG.debug("hack = %s" % (points_with_distance[0][0],))
            return (points_with_distance[0][1], 1)
        else:
            return (None, 1)

    # untested
    # find all parents of QGraphicsItem obj and find
    # rotation of all parents
    # input values:
    # 1) carrier object - QGraphicsItem object, that
    # fisically carry LIDAR
    # return:
    # 1) angle on scene of X axis in degrees
    def find_carrier_angle(self, carrier):
        angle = carrier.rotation()
        carrier_of_carrier = carrier.parentItem()
        while carrier_of_carrier is not None:
            angle += carrier_of_carrier.rotation()
            angle = angle % 360
            carrier_of_carrier = carrier_of_carrier.parentItem()
        return angle

    # untested
    # build ellipse item of scanning
    # return: QGraphicsEllipseItem
    def build_sector_of_scanning(self):
        self.scanning_shape = QtWidgets.QGraphicsEllipseItem(
            - self.lidar_maximum_distance,
            - self.lidar_maximum_distance,
            2 * self.lidar_maximum_distance,
            2 * self.lidar_maximum_distance,
            self.carrier_item)
        self.scanning_shape.setStartAngle(
            - self.lidars_half_angle * 16)
        self.scanning_shape.setSpanAngle(
            2 * self.lidars_half_angle * 16)

    # function filter items in vision
    # will be removed - all our parents and all childs of our parents
    def filter_items_in_vision(self, items_in_vision):
        # 1. filter bullets and tanks
        rude_filtered = []
        for item in items_in_vision:
            if not isinstance(item, bullet.Bullet):
                rude_filtered.append(item)
        items_in_vision_filtered = list(rude_filtered)
        # 2. find top parent of carrier_item
        top_parent = self.carrier_item
        while top_parent.parentItem() is not None:
            top_parent = top_parent.parentItem()
        # top_parent now is a top parent
        not_checked_items = []
        not_checked_items.append(top_parent)
        while len(not_checked_items) != 0:
            try:
                childs = not_checked_items[0].childItems()
                if childs is not None:
                    not_checked_items.extend(childs)
            except AttributeError:
                pass
            try:
                items_in_vision_filtered.remove(
                    not_checked_items[0])
            except ValueError:
                pass
            except AttributeError:
                pass
            not_checked_items.remove(not_checked_items[0])
        return items_in_vision_filtered
