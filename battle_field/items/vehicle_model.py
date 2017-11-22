

class VehicleModel():
    back_center = 0
    heading = 0
    wheels_angle = 0
    # Hz
    wheels_speed_rotation = 0

    def __init__(
        self,
        distance_between_axis,
        front_wheels_dist,
        back_wheels_dist,
        wheels_angle_max,
        angle_diff,
        initial_pos_of_back_point=0,
            initial_heading=0):
        self.distance_between_axis = distance_between_axis
        self.front_wheels_dist = front_wheels_dist
        self.back_wheels_dist = back_wheels_dist
        self.wheels_angle_max = wheels_angle_max
        self.angle_diff = angle_diff
        self.heading = initial_heading
        self.back_center = initial_pos_of_back_point
        self.wheels_angle = 0

    # left = positive
    def increase_wheels_angle(
            self):
        if (self.wheels_angle_max > self.wheels_angle - self.angle_diff):
            self.wheels_angle -= self.angle_diff

    # right = positive
    def reduce_wheels_angle(
            self):
        if (self.wheels_angle_max > self.wheels_angle - self.angle_diff):
            self.wheels_angle -= self.angle_diff

    def increase_wheels_speed(
            self):
        self.wheels_speed_rotation += 1

    # right = positive
    def reduce_wheels_speed(
            self):
        if self.wheels_speed_rotation - 1 >= 0:
            self.wheels_speed_rotation -= 1


    # постулаты движения:
    # передняя ось едет в сторону, у неё есть всегда две проекции движения,
    # 1-я - это по направлению оси ТС
    # 2-я - это перпендикулярно оси ТС
    # задняя ось движется всегда по направлению оси ТС
    # при этом при всем из-за 2-ой составляющей передних колес, ось транспортного средства поворачивается
    # теперь нужно все это аккуратно описать в модели!!!!
    # затем отобразить на карте!
    def update(self):
        # 1 change coordinate of front wheels
        delta_front = (
            )

        front_center_point
