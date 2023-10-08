class MyDoodle:
    x = 0
    y = 0

    def __init__(self, x, y):
        # self.x = x
        # self.y = y
        pass


doodle1 = MyDoodle(1, 4)
doodle2 = MyDoodle(2, 3)

print(f"MyDoodle: {MyDoodle.x}, {MyDoodle.y}")
print(f"doodle1: {doodle1.x}, {doodle1.y}")
print(f"doodle2: {doodle2.x}, {doodle2.y}")
