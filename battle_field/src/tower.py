from PyQt5.QtCore import qrand, QPointF, QLineF
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsPolygonItem
from PyQt5.QtGui import QPixmap, QPolygonF, QVector2D

import math

from bullet import Bullet


class Tower(QGraphicsPixmapItem):

    tower_picture_path = './src/images/head.png'

    def __init__(self, scene, parent):
        super(Tower, self).__init__(parent)
        self.rotation_speed = 5
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
        self.vision = QGraphicsPolygonItem(
            QPolygonF([
                QPointF(0, 0),
                QPointF(self.vision_distance, - self.vision_distance / 2),
                QPointF(self.vision_distance, self.vision_distance / 2)]),
            self)

    def update(self):
        self.enemy()
        self.change_angle()
        self.destroy()


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
                    QVector2D.dotProduct(vect_to_target, vect_of_body)) / math.pi

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
                sign * self.rotation_speed * self.scene().dt
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
