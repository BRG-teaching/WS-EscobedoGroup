from random import random, choice
from compas.geometry import Pointcloud, Frame, Plane
from compas.geometry import Box, Sphere, Torus
from compas.utilities import i_to_rgb
from compas_view2.app import App

cloud = Pointcloud.from_bounds(10, 10, 10, 50)

viewer = App()

for point in cloud:
    option = choice([1, 2, 3])
    color = i_to_rgb(random(), normalize=True)

    if option == 1:
        frame = Frame.worldXY()
        frame.point = point
        box = Box(frame, random(), random(), random())
        viewer.add(box, facecolor=color)

    elif option == 2:
        radius = random()
        sphere = Sphere(point, radius)
        viewer.add(sphere, facecolor=color)

    elif option == 3:
        plane = Plane(point, [0, 0, 1])
        radius = random()
        torus = Torus(plane, radius, 0.5 * radius)
        viewer.add(torus, facecolor=color)

viewer.run()
