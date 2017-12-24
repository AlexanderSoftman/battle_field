import math
import os
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from battle_field.items.vehicles.tank import tower
from battle_field.items import obstacle
from battle_field.common import functions
from battle_field.common.bump_checker import bump_checker_new
import battle_field


class Tank(QtWidgets.QGraphicsPixmapItem):
    tank_picture_path = os.path.join(
        os.path.split(battle_field.__file__)[0], 'images/tank.png')

    def __init__(self, scene, pos, angle, bot_flag=True):
        QtWidgets.QGraphicsPixmapItem.__init__(self)
        self.rect = QtWidgets.QGraphicsRectItem(
            QtCore.QRectF(0, 0, 10, 10), self)
        # delete counter after debug!!!
        self.built_li_shapes_list = []
        self.BumpChecker = bump_checker_new.BumpCheckerNew()
        # path brush
        self.setPos(pos)
        self.setRotation(angle)
        self.speed = 0
        self.Tank_rotation_speed = 20
        self.setPixmap(QtGui.QPixmap(self.tank_picture_path))
        self.setOffset(
            - self.boundingRect().width() / 2,
            - self.boundingRect().height() / 2)
        self.setScale(0.15)
        self.last_angle_time = scene.time.elapsed()
        self.Tank_angle_period = 6000 + QtCore.qrand() % 5000
        self.destination_angle = self.rotation()
        self.tower = tower.Tower(scene, self, bot_flag)
        self.bot_flag = bot_flag
        self.path_positions_list = []
        # self.health = health
        # create special colour poligonf around our tank
        return
        if self.bot_flag is False:
            print()
            self.colour_bound = QtGui.QPolygonF([
                QtCore.QPointF(
                    - self.boundingRect().width() / 2,
                    - self.boundingRect().height() / 2),
                QtCore.QPointF(
                    self.boundingRect().width() / 2,
                    - self.boundingRect().height() / 2),
                QtCore.QPointF(
                    self.boundingRect().width() / 2,
                    self.boundingRect().height() / 2),
                QtCore.QPointF(
                    - self.boundingRect().width() / 2,
                    self.boundingRect().height() / 2)])
            self.colour_bound_item = QtWidgets.QGraphicsPolygonItem(
                self.colour_bound, self)
            self.colour_bound_item_pen = QtGui.QPen(
                QtGui.QColor(0, 0, 255, 255))
            self.colour_bound_item_pen.setWidth(10)
            self.colour_bound_item.setPen(
                self.colour_bound_item_pen)
            self.colour_bound_item.setVisible(True)

    # interface
    def increase_speed(self):
        self.speed += 1

    # interface
    def reduce_speed(self):
        self.speed -= 1

    # interface
    def increase_angle(self):
        self.setRotation(
            self.rotation() + 2)

    # interface
    def reduce_angle(self):
        self.setRotation(
            self.rotation() - 2)

    # interface
    def make_damage(self, damage_power):
        self.health -= damage_power

    # internal for Tank, called by timer
    def update(self):
        # print("pos = %s" % (self.pos(),))
        self.change_pos()
        self.setPos(
            self.BumpChecker.bump_reaction(self))
        # move to tank level
        # if self.bot_flag:
            #if len(self.path_positions_list) == 0:
                #self.build_li_shapes()
            #else:
                #pass
                # self.correct_our_spped()

            # self.add_new_angle()
            # self.change_angle()

    # internal for Tank
    def change_pos(self):
        x = self.pos().x() + self.speed * math.cos(
            self.rotation() * math.pi / 180.0) * self.scene().dt
        y = self.pos().y() + self.speed * math.sin(
            self.rotation() * math.pi / 180.0) * self.scene().dt
        self.setPos(x, y)

    # internal for Tank
    def add_new_angle(self):
        if self.scene().time.elapsed() - self.last_angle_time > \
                self.Tank_angle_period:
            self.last_angle_time = self.scene().time.elapsed()
            self.destination_angle = -45 + (QtCore.qrand() % 90)

    # internal for Tank
    def change_angle(self):
        if (self.rotation() != self.destination_angle):
            if (self.destination_angle - self.rotation() > 0):
                sign = 1
            else:
                sign = -1
            self.setRotation(
                self.rotation() +
                sign * self.Tank_rotation_speed * self.scene().dt
            )

    # internal for Tank
    # def bump_check(self):
        # item_list = self.scene().collidingItems(self)
        # for item in item_list:
            # if (isinstance(item, Tank) and item is not self or
                    # isinstance(item, obstacle.Obstacle)):
                # self.move_us(item)

    # # internal for Tank
    # def move_us(self, item):
    #     if not self.collidesWithItem(item):
    #         return
    #     # 1. find all lines
    #     my_all_lines = functions.find_all_lines(self)
    #     item_all_lines = functions.find_all_lines(item)

    #     # 2. find colliding lines and dots
    #     my_lines, my_dots = self.find_colliding_lines_and_dots(
    #         my_all_lines, item_all_lines, item)
    #     item_lines, item_dots = self.find_colliding_lines_and_dots(
    #         item_all_lines, my_all_lines, self)

    #     # 3. find move direction
    #     move_dir = self.find_moving_vect(my_all_lines, item_all_lines, item)
    #     # 4. for every my and item dot inside other object
    #     # create projection
    #     full_projection_list = []

    #     for my_dot in my_dots:
    #         # create parallel line:
    #         par_line = QtCore.QLineF(my_dot, my_dot + move_dir.toPointF())
    #         # find all collisions with all lines of item:
    #         dots_intersected = []
    #         dot_intersected = QtCore.QPointF()
    #         for item_line in item_lines:
    #             intersect_type = par_line.intersect(item_line, dot_intersected)
    #             # check unbounded and bounded intersection type
    #             if ((QtCore.QLineF.BoundedIntersection == intersect_type) or
    #                 (QtCore.QLineF.UnboundedIntersection == intersect_type) and
    #                 (
    #                     min(
    #                         item_line.pointAt(0).x(),
    #                         item_line.pointAt(1).x()) <=
    #                     dot_intersected.x() <=
    #                     max(
    #                         item_line.pointAt(0).x(),
    #                         item_line.pointAt(1).x())) and (
    #                     min(
    #                         item_line.pointAt(0).y(),
    #                         item_line.pointAt(1).y()) <=
    #                     dot_intersected.y() <=
    #                     max(
    #                         item_line.pointAt(0).y(),
    #                         item_line.pointAt(1).y())) and
    #                     functions.check_point_belongs_to_line(
    #                         item_line, dot_intersected)):
    #                 dots_intersected.append(QtCore.QPointF(dot_intersected))
    #         # all item lines checked.
    #         # create list of projections vectors from
    #         # my point to direction
    #         dot_products_for_my_dot = []
    #         for dot in dots_intersected:
    #             # print("dot = " + str(dot))
    #             vector = QtGui.QVector2D(
    #                 QtCore.QPointF(
    #                     dot.x() - my_dot.x(),
    #                     dot.y() - my_dot.y()))
    #             dot_products_for_my_dot.append(
    #                 QtGui.QVector2D.dotProduct(vector, move_dir))
    #         # sort all dot product list
    #         dot_products_for_my_dot = sorted(
    #             dot_products_for_my_dot,
    #             key=lambda value: value)
    #         # check that list is not empty,
    #         # get maximum value (-1 element)
    #         if len(dot_products_for_my_dot) > 0:
    #             full_projection_list.append(
    #                 dot_products_for_my_dot[-1])
    #     # for every item dots create list of collision with my lines
    #     for item_dot in item_dots:
    #         # create parallel line:
    #         par_line = QtCore.QLineF(item_dot, item_dot + move_dir.toPointF())
    #         # find all collisions with all lines of item:
    #         dots_intersected = []
    #         dot_intersected = QtCore.QPointF()
    #         for my_line in my_lines:
    #             intersect_type = par_line.intersect(my_line, dot_intersected)
    #             # check unbounded and bounded intersection type
    #             # check that QtCore.QPointF belongs to QtCore.QLineF
    #             if ((QtCore.QLineF.BoundedIntersection == intersect_type) or
    #                 (QtCore.QLineF.UnboundedIntersection == intersect_type) and
    #                 (
    #                     min(
    #                         my_line.pointAt(0).x(),
    #                         my_line.pointAt(1).x()) <=
    #                     dot_intersected.x() <=
    #                     max(
    #                         my_line.pointAt(0).x(),
    #                         my_line.pointAt(1).x())) and (
    #                     min(
    #                         my_line.pointAt(0).y(),
    #                         my_line.pointAt(1).y()) <=
    #                     dot_intersected.y() <=
    #                     max(
    #                         my_line.pointAt(0).y(),
    #                         my_line.pointAt(1).y()))):
    #                 # print("add new intersect dot = " + str(dot_intersected))
    #                 dots_intersected.append(QtCore.QPointF(dot_intersected))
    #         # all my lines checked.
    #         # create list of projections vectors from
    #         # item point to direction
    #         dot_products_for_item_dot = []
    #         for dot in dots_intersected:
    #             vector = QtGui.QVector2D(
    #                 item_dot - dot)
    #             dot_products_for_item_dot.append(
    #                 QtGui.QVector2D.dotProduct(vector, move_dir))
    #         # sort all dot product list
    #         dot_products_for_item_dot = sorted(
    #             dot_products_for_item_dot,
    #             key=lambda value: value)
    #         # check that list is not empty,
    #         # get maximum value (-1 element)
    #         if len(dot_products_for_item_dot) > 0:
    #             full_projection_list.append(
    #                 dot_products_for_item_dot[-1])

    #     # 8. sort full_projection_list by projection values
    #     full_projection_list = sorted(
    #         full_projection_list,
    #         key=lambda value: value)

    #     # 9. move to maximum value from projection listfull_projection_list[-1]
    #     if len(full_projection_list) > 0:
    #         self.setPos(
    #             self.pos() + (move_dir * full_projection_list[-1]).toPointF())

    # # internal for Tank
    # def find_colliding_lines_and_dots(self, tested_list, second_list, item):
    #     lines_list = []
    #     dots_list = []
    #     point_of_intersection = QtCore.QPointF()
    #     # find bounded lines
    #     for test_line in tested_list:
    #         # add instersection dots
    #         for second_line in second_list:
    #             intersection_type = test_line.intersect(
    #                 second_line, point_of_intersection)
    #             if (QtCore.QLineF.BoundedIntersection == intersection_type and
    #                     test_line not in lines_list):
    #                 lines_list.append(QtCore.QLineF(test_line))

    #     # find lines fully inside item:
    #     rect = QtCore.QRectF(
    #         item.mapToScene(
    #             QtCore.QPointF(
    #                 - item.boundingRect().width() / 2,
    #                 - item.boundingRect().height() / 2)),
    #         item.mapToScene(
    #             QtCore.QPointF(
    #                 item.boundingRect().width() / 2,
    #                 item.boundingRect().height() / 2)))
    #     for test_line in tested_list:
    #         if (rect.contains(test_line.p1()) and
    #             rect.contains(test_line.p2()) and
    #                 test_line not in lines_list):
    #             lines_list.append(test_line)

    #     if len(lines_list) > 1:
    #         for first in lines_list:
    #             for second in lines_list:
    #                 if first != second:
    #                     if (first.p1() == second.p1() or
    #                         first.p1() == second.p2() and
    #                             first.p1() not in dots_list):
    #                             dots_list.append(first.p1())
    #                     if (first.p2() == second.p1() or
    #                         first.p2() == second.p2() and
    #                             first.p2() not in dots_list):
    #                             dots_list.append(first.p2())

    #     return lines_list, dots_list

    # # internal for Tank
    # def find_moving_vect(self, my_lines, obj_lines, item):
    #     all_dots_list = []
    #     point_of_intersection = QtCore.QPointF()
    #     # find bounded lines
    #     for my_line in my_lines:
    #         # add instersection dots
    #         for obj_line in obj_lines:
    #             intersection_type = my_line.intersect(
    #                 obj_line, point_of_intersection)
    #             if QtCore.QLineF.BoundedIntersection == intersection_type:
    #                 all_dots_list.append(QtCore.QPointF(point_of_intersection))
    #     # find lines fully inside me:
    #     rect = QtCore.QRectF(
    #         self.mapToScene(
    #             QtCore.QPointF(
    #                 - self.boundingRect().width() / 2,
    #                 - self.boundingRect().height() / 2)),
    #         self.mapToScene(
    #             QtCore.QPointF(
    #                 self.boundingRect().width() / 2,
    #                 self.boundingRect().height() / 2)))

    #     for obj_line in obj_lines:
    #         if (rect.contains(obj_line.p1()) and
    #                 rect.contains(obj_line.p2())):
    #             all_dots_list.append(obj_line.p1())
    #             all_dots_list.append(obj_line.p2())

    #     # sort list of dots
    #     all_dots_list = sorted(
    #         all_dots_list,
    #         key=lambda value: (QtCore.QLineF(
    #             QtCore.QPointF(0, 0),
    #             item.mapToItem(item, value)).angle()))

    #     normal_lines = []
    #     for idx_first, dot_first in enumerate(all_dots_list):
    #         for idx_second, dot_second in enumerate(all_dots_list):
    #             if (idx_first == idx_second + 1 or
    #                 (idx_first == len(all_dots_list) - 1 and
    #                     idx_second == 0)):
    #                 normal_lines.append(
    #                     QtCore.QLineF(
    #                         dot_first,
    #                         dot_second).normalVector())
    #     normal_lines = sorted(
    #         normal_lines,
    #         key=lambda value: value.length())
    #     return QtGui.QVector2D(
    #         normal_lines[-1].p2() - normal_lines[-1].p1()).normalized()
