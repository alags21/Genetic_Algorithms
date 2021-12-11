import math


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.position = (x, y)
        self.magnitude = math.sqrt(self.x**2 + self.y**2)

    def __add__(self, other):
        if type(other) != Vector:
            raise TypeError("Can only add vector and vector")
        else:
            return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if type(other) != Vector:
            raise TypeError("Can only subtract vector and vector")
        else:
            return Vector(self.x - other.x, self.x - other.x)

    def __mul__(self, other):
        if type(other) == Vector:
            return Vector(self.x * other.x, self.y * other.y)

        elif type(other) == int or type(other) == float:
            return Vector(self.x * other, self.y * other)

        else:
            raise TypeError("Can only multiply vector and vector")

    def __truediv__(self, other):
        if type(other) == Vector:
            raise Exception("Cannot divide vector by vector")
        else:
            return Vector(self.x / other, self.y / other)

    def __repr__(self):
        return f"⟨{self.x}, {self.y}⟩"


class Ball:
    def __init__(self, x, y, velocity, charge):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.charge = charge
        self.position = Vector(self.x, self.y)

    def __repr__(self):
        return f"⟨{self.x}, {self.y}⟩"


class ChargePoint:
    def __init__(self, x, y, charge):
        self.x = x
        self.y = y
        self.charge = charge
        self.position = Vector(self.x, self.y)

    def __repr__(self):
        return f"⟨{self.x}, {self.y}⟩, charge = {self.charge}"


def calculate_electricity_vector(ball):
    charge_influenced_vectors = []
    for chargepoint in CHARGEPOINTS:
        numerator = (chargepoint.position - ball.position) * (ball.charge * chargepoint.charge)
        denominator = (chargepoint.position - ball.position).magnitude ** 3
        charge_influenced_vectors.append(numerator /denominator)

    velocity_after_electricity_calculation = ball.velocity
    for c in charge_influenced_vectors:
        velocity_after_electricity_calculation += c

    return velocity_after_electricity_calculation

def calculate_new_position(ball):
    acceleration = GRAVITY + calculate_electricity_vector(ball)
    new_velocity = ball.velocity + acceleration
    new_position = ball.position + (new_velocity * DT)

    ball.velocity = new_velocity
    ball.x = new_position.x
    ball.y = new_position.y
    ball.position = Vector(ball.x, ball.y)

    return ball.position


def shoot_ball(ball, time, x_list, y_list):
    time += DT
    calculate_new_position(ball)
    if check_if_hit_wall(ball):
        x_list.append(ball.x)
        y_list.append(ball.y)
        return [time, ball, x_list, y_list]
    else:
        print(ball.position)
        print("____________")
        x_list.append(ball.x)
        y_list.append(ball.y)
        return shoot_ball(ball, time, x_list, y_list)


def check_if_hit_wall(ball):
    if ball.x >= 10:
        return True
    else:
        return False


GRAVITY = Vector(0, -1)
CHARGEPOINTS = [ChargePoint(1, 0, 2), ChargePoint(2, 0 ,-1), ChargePoint(-1, 0, -0.5)]
bal = Ball(-0, 0, Vector(1, 0), 21)
DT = 0.00001

print(shoot_ball(bal, 0, [bal.x], [bal.y]))
