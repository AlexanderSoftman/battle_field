import os
import math
from PyQt5.QtGui import (QPixmap)
from PyQt5.QtWidgets import QGraphicsPixmapItem
import battle_field
from battle_field.items.vehicles.tank import tank
from battle_field.items import obstacle


class Bullet(QGraphicsPixmapItem):
    bullet_pict_path = os.path.join(
        os.path.split(battle_field.__file__)[0], 'images/bullet.png')
    explosion_pict_path = os.path.join(
        os.path.split(battle_field.__file__)[0], 'images/explosion_1.png')
    # bullet_power = 101
    basic_speed = 265

    # Create the bounding rectangle
    def __init__(self, scene, pos, angle, initial_speed):
        QGraphicsPixmapItem.__init__(self)
        self.setPos(pos)
        self.setRotation(angle)
        self.speed = self.basic_speed + initial_speed
        self.setPixmap(
            QPixmap(
                self.bullet_pict_path))
        self.setOffset(
            - self.boundingRect().width() / 2,
            - self.boundingRect().height() / 2)
        self.setScale(0.025)
        self.cycles_of_explosion = 5
        self.exploded = False
        self.setVisible(True)
        print(
            "bullet pos_x = " + str(pos.x()) + "pos_y = " +
            str(pos.y()) + " angle = " + str(angle))

    def update(self):
        x = self.pos().x() + self.speed * math.cos(
            self.rotation() * math.pi / 180.0) * self.scene().dt
        y = self.pos().y() + self.speed * math.sin(
            self.rotation() * math.pi / 180.0) * self.scene().dt
        self.setPos(x, y)
        for item in self.scene().collidingItems(self):
            print("colliding with item = %s" % (item,))
        print(
            "item.isVisible = %s" % (self.isVisible(),))
        if (self.exploded is False):
            if self.check_collision():
                # stop bullet
                self.speed = 0
                self.exploded = True
                self.setPixmap(
                    QPixmap(
                        self.explosion_pict_path))
                self.setScale(0.050)
        else:
            self.cycles_of_explosion -= 1

        if self.cycles_of_explosion < 0:
            self.scene().removeItem(self)

    def check_collision(self):
        collision_detected = False
        for item in self.scene().collidingItems(self):
            if isinstance(item, tank.Tank):
                item.destroy()
                # item.make_damage(self.bullet_power)
                collision_detected = True
                break
            if isinstance(item, obstacle.Obstacle):
                collision_detected = True
                break
        return collision_detected
