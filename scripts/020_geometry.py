from random import random, choice
from compas.geometry import Point, Pointcloud, Polygon, Translation
from compas.geometry import is_point_in_polygon_xy
from compas.geometry import intersection_segment_segment_xy, mirror_points_line_xy
from compas_plotters import GeometryPlotter

# ==============================================================================
# Parameters
# ==============================================================================

N = 50
W = 100
H = 50

# ==============================================================================
# Objects
# ==============================================================================

cloud = Pointcloud.from_bounds(W, H, 0, N)
polygon = Polygon.from_sides_and_radius_xy(5, 20.0)
polygon.transform(Translation.from_vector([0.5 * W, 0.5 * H, 0]))
box = Polygon([[0, 0], [W, 0], [W, H], [0, H]])

# ==============================================================================
# Transformations
# ==============================================================================

# random translation vector per point in the cloud
transformations = [
    Translation.from_vector([
        choice([-1, +1]) * random(),
        choice([-1, +1]) * random(),
        0])
    for _ in cloud]
 
# ==============================================================================
# Visualisation
# ==============================================================================

# basic plotter instance
plotter = GeometryPlotter()

# add boundary box and polygon
plotter.add(box, edgecolor=(0, 0, 0), fill=False)
plotter.add(polygon, edgecolor=(0, 0, 1), facecolor=(0.7, 0.7, 1.0))

# add the points of the pointcloud
for point in cloud:
    plotter.add(point, facecolor=(1, 1, 1))

# start visualisation
plotter.zoom_extents()
plotter.pause(1)

# move points in the direction of the randomly assigned translation vectors
# bounce the points of the walls of the box
# color points red when they paas through the polygon
for _ in range(100):
    for i in range(N):
        T = transformations[i]
        a = cloud[i]
        b = a.transformed(T)
        artist = plotter.find(a)

        for side in box.lines:
            x = intersection_segment_segment_xy((a, b), side)
            if x:
                x1 = Point(*x)
                x2 = Point(* mirror_points_line_xy([x1 + (b - a)], side)[0])
                T = Translation.from_vector(x2 - x1)
                transformations[i] = T
                break

        a.transform(T)
        artist.facecolor = (1, 0, 0) if is_point_in_polygon_xy(a, polygon) else (1, 1, 1)

    # redraw the plotter view with a specific timeout
    plotter.redraw(pause=0.1)

# keep the window alive after completion of the script
plotter.show()
