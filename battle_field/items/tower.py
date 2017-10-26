import os
import math
from PyQt5.QtCore import qrand, QPointF, QLineF, Qt
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsPolygonItem
from PyQt5.QtGui import QPixmap, QPolygonF, QVector2D
from battle_field.items.bullet import Bullet
import battle_field.items.functions
from battle_field.items.obstacle import Obstacle
import battle_field


class Tower(QGraphicsPixmapItem):
    tower_picture_path = os.path.join(
        os.path.split(battle_field.__file__)[0], 'images/head.png')

    def __init__(self, scene, parent, bot_flag=True):
        super(Tower, self).__init__(parent)
        self.parent = parent
        self.rotation_speed_maximum = 5
        self.rotation_speed = 0
        self.setPixmap(QPixmap(self.tower_picture_path))
        self.setOffset(
            - self.boundingRect().width() / 2,
            - self.boundingRect().height() / 2)
        self.setScale(0.9)
        self.last_shoot_time = scene.time.elapsed()
        self.last_angle_time = scene.time.elapsed()
        self.shoot_period = 7000
        self.angle_period = 7000
        self.destination_angle = self.rotation()
        self.safety_distance = 400
        self.vision_distance = 5000
        self.vision_ideal = QPolygonF([
            QPointF(0, 0),
            QPointF(self.vision_distance, - self.vision_distance / 2),
            QPointF(self.vision_distance, self.vision_distance / 2)])
        self.vision_shape = self.vision_ideal
        self.vision = QGraphicsPolygonItem(
            self.vision_shape,
            self)
        self.vision_lines = []
        self.vision_lines.append(
            QLineF(
                QPointF(0, 0),
                QPointF(self.vision_distance, - self.vision_distance / 2)))
        self.vision_lines.append(
            QLineF(
                QPointF(0, 0),
                QPointF(self.vision_distance, self.vision_distance / 2)))
        self.behind_line = QLineF(
            QPointF(self.vision_distance, - self.vision_distance / 2),
            QPointF(self.vision_distance, self.vision_distance / 2))
        self.vision_lines.append(self.behind_line)
        self.bot_flag = bot_flag

    def update(self):
        self.update_vision()
        if (self.bot_flag):
            self.enemy()
            self.change_angle()
            self.destroy()
        else:
            self.rotate_tower()

    def enemy(self):
        # 1. search targets
        targets_list = self.scene().collidingItems(self.vision)
        enemies_info = []
        for target in targets_list:
            if (isinstance(target, Tower)):
                if target is self:
                    continue
                vect_to_target = QVector2D(
                    target.mapToScene(0, 0) - self.mapToScene(0, 0))
                distance_to_target = vect_to_target.length()
                vect_to_target = vect_to_target.normalized()
                vect_of_body = QVector2D(
                    (self.parentItem().mapToScene(1, 0)) -
                    (self.parentItem().mapToScene(0, 0))).normalized()
                angle_to_target = 180.0 * math.acos(
                    QVector2D.dotProduct(
                        vect_to_target, vect_of_body)) / math.pi

                vect_of_body_orto = QVector2D(
                    -vect_of_body.y(), vect_of_body.x())

                # get sign of angle
                sign = QVector2D.dotProduct(vect_to_target, vect_of_body_orto)
                angle_to_target = \
                    angle_to_target if sign > 0 else - angle_to_target

                enemies_info.append([
                    distance_to_target,
                    angle_to_target])

        # print(enemies_info)
        # 2. we should find tank with minimum
        # distance as most dangerous.most
        # But if distance is not so small,
        # we should find tank with our tower angle
        if len(enemies_info) == 0:
            self.start_scanning()
        else:
            # sort enemies by angle
            en_info_sorted = sorted(
                enemies_info, key=lambda x: math.fabs(x[1]))
            # default destination_angle - minimum value
            self.destination_angle = en_info_sorted[0][1]
            # check that we don't have enemy in safety area
            # it should be killed first
            for enemy in en_info_sorted:
                if (enemy[0] < self.safety_distance):
                    self.destination_angle = enemy[1]
                    break

    def start_scanning(self):
        # find new destination angle
        if self.scene().time.elapsed() - self.last_angle_time > \
                self.rotation():
            self.last_angle_time = self.scene().time.elapsed()
            self.angle_period = -45 + (qrand() % 90)

    def change_angle(self):
        # print("angle dif: " + str(self.rotation() - self.destination_angle))
        if (self.rotation() != self.destination_angle):
            if (self.destination_angle - self.rotation() > 0):
                sign = 1
            else:
                sign = -1
            self.setRotation(
                self.rotation() +
                sign * self.rotation_speed_maximum * self.scene().dt
            )

    def destroy(self):
        if (math.fabs(self.rotation() - self.destination_angle) < 5):
            self.create_bullet()

    def create_bullet(self):
        if self.scene().time.elapsed() - self.last_shoot_time > \
                self.shoot_period:
            bullet_x = self.boundingRect().width()
            bullet_y = 0
            self.scene().addItem(Bullet(
                self.scene(),
                self.mapToScene(QPointF(bullet_x, bullet_y)),
                self.parentItem().rotation() + self.rotation()))
            self.last_shoot_time = self.scene().time.elapsed()

    def rotate_tower(self):
        self.setRotation(
            self.rotation() +
            self.rotation_speed * self.scene().dt
        )

    def increase_rotation_speed(self):
        self.rotation_speed += 0.1 * self.rotation_speed_maximum
        if self.rotation_speed > self.rotation_speed_maximum:
            self.rotation_speed = self.rotation_speed_maximum

    def reduce_rotation_speed(self):
        self.rotation_speed -= 0.1 * self.rotation_speed_maximum
        if math.fabs(self.rotation_speed) > self.rotation_speed_maximum:
            self.rotation_speed = -self.rotation_speed_maximum

    def find_enemies(self):
        # 1. find all colliding with vision items
        # 2. find all lines of item inside poligonf
        # 3. find lines only inside vision poligonf
        # 4. find shadows for every item in vision
            # 4.1. find shadow for every line of item
            # 4.2. union shadows
            # 4.3. substract from shadow item poligonf
            # (so we will see item after that)
        # 5. assign to vision_shape ideal vision
        # 6. substract all shadows from ideal vision
        # 7. assign current shape to PolygonItem
        # 8. return filtered colliding items

        # 1. find all colliding with vision items
        items_in_vision = self.scene().collidingItems(self.vision)
        print("%s count items_in_vision" % (
            items_in_vision,))
        if len(items_in_vision) == 0:
            return items_in_vision
        shadows = []
        for item in items_in_vision:
            # 2. find all lines of item
            all_lines_of_item = functions.find_all_lines(item)
            # 3. find lines only inside vision poligonf
            lines_in_vision = self.find_lines_in_ideal_vision(
                all_lines_of_item)
            # 4. find shadows for every item in vision
            item_shadow = QPolygonF()
            for line in lines_in_vision:
                # 4.1. find shadow for every line of item
                line_shadow = self.find_line_shadow(line)
                # 4.2. union shadows
                item_shadow.united(line_shadow)
            # 4.3. substract from shadow item poligonf
            item_shadow = item_shadow.substracted(
                functions.find_poligon(item))
            shadows.append(item_shadow)
        # 5. assign to vision_shape ideal vision
        self.vision_shape = self.vision_ideal
        # 6. substract all shadows from ideal vision
        for shadow in shadows:
            self.vision_shape = self.vision_shape.substracted(
                shadow)
        # 7. assign current shape to PolygonItem
        self.vision.setPolygon(self.vision_shape)
        # 8. return filtered colliding items
        print("%s count of colliding items" % (
            self.scene().collidingItems(self.vision),))
        return self.scene().collidingItems(self.vision)

    def update_vision(self):
        # 0. assign to vision_shape ideal vision
        # 1. find all colliding with vision items
        # 2. find all lines of item inside poligonf
        # 3. find lines only inside vision poligonf
        # 4. find shadows for every item in vision
            # 4.1. find shadow for every line of item
            # 4.2. union shadows
            # 4.3. substract from shadow item poligonf
            # (so we will see item after that)
        # 5. substract all shadows from ideal vision
        # 6. assign current shape to PolygonItem

        # 0. assign to vision_shape ideal vision
        self.vision_shape = self.vision_ideal
        # 1. find all colliding with vision items
        items_in_vision_before_filtering = self.scene().collidingItems(
            self.vision)
        items_in_vision = []
        # we should filter items, we see only personages (except our parent)
        # and obstacles
        for item in items_in_vision_before_filtering:
            if ((isinstance(item, type(self.parent)) and
                item is not self.parent) or
                    isinstance(item, Obstacle)):
                    items_in_vision.append(item)
        print("%s len items in vision" % (len(items_in_vision),))
        print("%s items in vision" % (items_in_vision,))
        if len(items_in_vision) == 0:
            return items_in_vision
        shadows = []
        for item in items_in_vision:
            all_lines_of_item = (
                battle_field.items.functions.find_all_lines_in_my_sc(
                    item, self))
            print("%s all lines in towers coordinates" % (all_lines_of_item,))
            # 2. find all lines of item - in scene coordinates!
           # all_lines_of_item_scene = battle_field.items.functions.find_all_lines(
                #item)
            #print("%s all lines" % (all_lines_of_item_scene,))
            # 3. recalculate them to towers coordinates
            #all_lines_of_item = []
            #for line in all_lines_of_item_scene:
                # convert scene coordinates to parent coordinates
                #line_in_personage = QLineF(
                    #self.parent.mapFromScene(line.p1()),
                    #self.parent.mapFromScene(line.p2()))
                #print("%s line in personage coordinates" % (
                    #line_in_personage,))
                # convert to tower coordinates from parent
                #line_in_tower = QLineF(
                    #self.mapFromItem(
                        #self.parent, line_in_personage.p1()),
                    #self.mapFromItem(
                        #self.parent, line_in_personage.p2()))
                #print("%s line in tower coordinates" % (
                    #line_in_personage,))
                # add to list
                #all_lines_of_item.append(line_in_tower)
            
            
            # 3. find lines only inside vision poligonf
            lines_in_vision = self.find_lines_in_ideal_vision(
                all_lines_of_item)
            print("%s lines_in_vision" % (lines_in_vision,))
            # 4. find shadows for every item in vision
            item_shadow = QPolygonF()
            for line in lines_in_vision:
                # 4.1. find shadow for every line of item
                line_shadow = self.find_line_shadow(line)
                # 4.2. union shadows
                item_shadow.united(line_shadow)
            # 4.3. substract from shadow item poligonf
            item_shadow = item_shadow.subtracted(
                battle_field.items.functions.find_poligon(item))
            shadows.append(item_shadow)
        # 5. substract all shadows from ideal vision
        for shadow in shadows:
            self.vision_shape = self.vision_shape.subtracted(
                shadow)
        # 6. assign current shape to PolygonItem
        self.vision.setPolygon(self.vision_shape)

    def find_line_shadow(self, line):
        print("analyze %s line" % (line, ))
        point_of_intersection = QPointF()
        behind_line_intersections = []
        print("check first point of line for intersection")
        intersection_type = QLineF(
            line.p1(),
            QPointF(0, 0)).intersect(
            self.behind_line, point_of_intersection)
        if ((QLineF.BoundedIntersection == intersection_type or
            QLineF.UnboundedIntersection == intersection_type) and
            battle_field.items.functions.check_point_belongs_to_line(
                self.behind_line, point_of_intersection)):
            behind_line_intersections.append(point_of_intersection)
        print("check second point of line for intersection")
        intersection_type = QLineF(
            line.p2(),
            QPointF(0, 0)).intersect(
            self.behind_line, point_of_intersection)
        if ((QLineF.BoundedIntersection == intersection_type or
            QLineF.UnboundedIntersection == intersection_type) and
            battle_field.items.functions.check_point_belongs_to_line(
                self.behind_line, point_of_intersection)):
            behind_line_intersections.append(point_of_intersection)
        print("%s len of behind_line_intersections list" % (
            len(behind_line_intersections),))
        return QPolygonF(
            [behind_line_intersections[0],
                line.p1(),
                line.p2(),
                behind_line_intersections[1]])

    def find_lines_in_ideal_vision(self, lines):

        lines_in_vision = []
        # lines fully inside vision
        for line in lines:
            if (self.vision_ideal.containsPoint(
                line.p1(), Qt.OddEvenFill) and
                    self.vision_ideal.containsPoint(
                        line.p2(), Qt.OddEvenFill)):
                    lines_in_vision.append(line)
        # lines, part of which inside vision_ideal
        for line in lines:
            point_of_intersection_list = []
            for vision_line in self.vision_lines:
                point_of_intersection = QPointF()
                intersection_type = vision_line.intersect(
                    line, point_of_intersection)
                if QLineF.BoundedIntersection == intersection_type:
                    point_of_intersection_list.append(point_of_intersection)
            # check if we have 2 points of intersection
            # so should create line without start and end of first line
            if len(point_of_intersection_list) == 2:
                lines_in_vision.append(
                    QLineF(
                        point_of_intersection_list[0],
                        point_of_intersection_list[1]))
            # check if we have 1 points of intersection
            # so should create line WITH start or end of first line
            if len(point_of_intersection_list) == 1:
                # find start or end inside vision_ideal
                if self.vision_ideal.containsPoint(line.p1(), Qt.OddEvenFill):
                    lines_in_vision.append(
                        QLineF(
                            point_of_intersection_list[0],
                            line.p1()))
                elif self.vision_ideal.containsPoint(
                        line.p2(), Qt.OddEvenFill):
                    lines_in_vision.append(
                        QLineF(
                            point_of_intersection_list[0],
                            line.p2()))
        return lines_in_vision