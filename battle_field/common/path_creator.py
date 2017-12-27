from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
import time


class PathCreator():

    # input values:
    # scene
    # prohibited_obj_types - lsit of objects,
    # that will forbid shapes creating
    def __init__(self, scene, prohibited_obj_types):
        self.scene = scene
        self.prohibited_obj_types = prohibited_obj_types
        # dict {(x,y) : li_shape, ...}
        self.li_shapes = {}
        self.path_brush = QtGui.QBrush(
            QtGui.QColor(210, 210, 210, 200),
            QtCore.Qt.SolidPattern)
        self.visibility = True

    def create_li_shapes_tree(
            self,
            li_shape_border,
            obj_point,
            dest_point):
        start_time = time.time()
        path_positions_list = []
        # clean current dict of li shapes
        for key, item in self.li_shapes.items():
            item.clean_from_scene()
        self.li_shapes.clear()
        weight = 0
        coordinates = [0, 0]
        self.obj_li_shape = LiShape(
            self.scene,
            obj_point,
            li_shape_border,
            weight,
            None,
            self.visibility)
        # check, may be we contain destination point
        dest_point_covered = self.obj_li_shape.contains(
            dest_point)
        dest_point_cant_be_reached = False
        undrawed_li_shapes = {}
        undrawed_li_shapes[tuple(coordinates)] = self.obj_li_shape
        self.li_shapes[tuple(coordinates)] = self.obj_li_shape
        # before we not covered by our cells destination point,
        # add new shapes, not colliding with nearest shapes
        while not dest_point_covered:
            generated_li_shapes = {}
            weight += 1
            # sort undrawes li_shapes accrding to distance to finish point
            # after items operation we will have list of tuples
            # [((X, Y), Li_shape_object)]
            undrawed_li_shapes_sorted = undrawed_li_shapes.items()
            undrawed_li_shapes_sorted = sorted(
                undrawed_li_shapes_sorted,
                key=lambda value: QtCore.QLineF(
                    value[1].center, dest_point).length())
            for value in undrawed_li_shapes_sorted:
                coordinates = value[0]
                li_shape = value[1]
                # create 4 rects centers around our object
                # generated_positions format =
                # [[(x,y), QPointf(position)], ]
                generated_positions = (
                    self.create_new_li_shapes_positions(
                        li_shape.center,
                        li_shape_border,
                        coordinates))
                # sort list of new shapes by distance
                # to destination point
                generated_positions = sorted(
                    generated_positions,
                    key=lambda value: QtCore.QLineF(
                        value[1], dest_point).length())
                # filtered positions, create shapes
                for value in generated_positions:
                    pos_coordinates = value[0]
                    pos = value[1]
                    if not self.li_shapes_collision_detector(
                            pos, pos_coordinates):
                        (new_li_shape,
                            dest_point_cant_be_reached,
                            dest_point_covered) = (
                            self.build_shape_with_prohibited_objects_checking(
                                pos,
                                li_shape_border,
                                weight,
                                li_shape,
                                dest_point))
                        if new_li_shape is not None:
                            self.li_shapes[pos_coordinates] = new_li_shape
                            generated_li_shapes[pos_coordinates] = new_li_shape
                        if dest_point_covered is True:
                            elapsed_time = time.time() - start_time
                            print("time for creating shapes: %s" % (
                                elapsed_time,))
                            if dest_point_cant_be_reached is False:
                                path_positions_list = (
                                    self.find_path_to_destination(
                                        new_li_shape))
                            else:
                                path_positions_list = None
                            return path_positions_list
            undrawed_li_shapes.clear()
            undrawed_li_shapes.update(generated_li_shapes)
            generated_li_shapes.clear()

    # create new shapes positions in format and return
    # input values: center - QPointF
    # border - double
    # coordinates - (x,y) - tuple
    # [(x,y): QPointf(position), ]
    def create_new_li_shapes_positions(
        self,
        center,
        border,
            coordinates):
        return [
            [(coordinates[0] + 1, coordinates[1]),
                center + QtCore.QPointF(2 * border, 0)],
            [(coordinates[0] + 1, coordinates[1] + 1),
                center + QtCore.QPointF(2 * border, 2 * border)],
            [(coordinates[0], coordinates[1] + 1),
                center + QtCore.QPointF(0, 2 * border)],
            [(coordinates[0] - 1, coordinates[1] + 1),
                center + QtCore.QPointF(- 2 * border, 2 * border)],
            [(coordinates[0] - 1, coordinates[1]),
                center + QtCore.QPointF(- 2 * border, 0)],
            [(coordinates[0] - 1, coordinates[1] - 1),
                center + QtCore.QPointF(- 2 * border, - 2 * border)],
            [(coordinates[0], coordinates[1] - 1),
                center + QtCore.QPointF(0, - 2 * border)],
            [(coordinates[0] + 1, coordinates[1] - 1),
                center + QtCore.QPointF(2 * border, - 2 * border)]]

    # input values:
    # position - QPointF
    # coordinates - (x,y) tuple
    # return True if collision detected
    # return False if no collisions
    def li_shapes_collision_detector(
            self, position, coordinates):
        # get coordinates tuple:
        for delta_x in range(1, -2, -1):
            for delta_y in range(1, -2, -1):
                get_object = self.li_shapes.get(
                    (coordinates[0] + delta_x,
                        coordinates[1] + delta_y),
                    None)
                if (get_object is not None):
                    if (get_object.polygon().containsPoint(
                            position,
                            QtCore.Qt.OddEvenFill)):
                        return True
        return False

    # input:
    # position - QPointF
    # border - double
    # weight - double
    # parent_shape - reference to parent_shape
    # return tuple of
    # 1)new_shape
    # 2)position_cannot_be_reached_flag
    # 3)destination_point covered
    # position cannot be reached if destination point inside prohibited object
    def build_shape_with_prohibited_objects_checking(
            self,
            position,
            border,
            weight,
            parent_shape,
            dest_point):
        new_shape = LiShape(
            self.scene,
            position,
            border,
            weight,
            parent_shape,
            self.visibility)
        pos_cant_be_reached = False
        colliding_items_list = self.scene.collidingItems(
            new_shape)
        dest_point_covered = (
            new_shape.polygon().containsPoint(
                dest_point, QtCore.Qt.OddEvenFill))
        for item in colliding_items_list:
            for item_type in self.prohibited_obj_types:
                if isinstance(item, item_type):
                    new_shape.clean_from_scene()
                    if dest_point_covered is True:
                        pos_cant_be_reached = True
                        # print("pos_cant_be_reached = True")
                    return None, pos_cant_be_reached, dest_point_covered
        return new_shape, pos_cant_be_reached, dest_point_covered

    def find_path_to_destination(
            self,
            dest_li_shape):
        # firts fill all shapes until destination shape
        # print("weight = %s" % (dest_li_shape.weight,))
        weight = dest_li_shape.weight
        shape = dest_li_shape
        path_positions_list = []
        while weight != 0:
            path_positions_list.append((shape.center, shape.weight))
            shape.setBrush(self.path_brush)
            shape = shape.parent_shape
            weight = shape.weight
        # sort path by distance:
        path_positions_list = sorted(
            path_positions_list,
            key=lambda value: value[1])
        return path_positions_list


class LiShape(QtWidgets.QGraphicsPolygonItem):

    # input parameters:
    # scene - scene
    # center - QPointF
    # border - border side
    # weight - Shape weight
    # parent_shape - parent shape
    # visibility - visibility of shape
    # colour - colour for marking
    def __init__(
        self,
        scene,
        center,
        border,
        weight,
        parent_shape,
        visibility,
            colour=QtGui.QColor(0, 255, 0, 255)):

        QtWidgets.QGraphicsPolygonItem.__init__(self)
        self.setPolygon(self.create_polygon(center, border))
        self.center = center
        self.weight = weight
        self.parent_shape = parent_shape
        self.pen = QtGui.QPen(
            colour)
        self.pen.setWidth(2)
        self.setPen(
            self.pen)
        self.setVisible(visibility)
        self.scene = scene
        self.scene.addItem(self)

    # build polygon as rect with known center in scene coordinates
    # input values:
    # center - QPointF value
    # border - double valuse
    # return: QPolygonF with 4 pointf
    def create_polygon(self, center, border):
        return (QtGui.QPolygonF([
            center + QtCore.QPointF(
                - border,
                - border),
            center + QtCore.QPointF(
                border,
                - border),
            center + QtCore.QPointF(
                border,
                border),
            center + QtCore.QPointF(
                - border,
                border)]))

    # clean item from scene
    def clean_from_scene(self):
        self.scene.removeItem(self)
