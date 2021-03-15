from compas.geometry import Pointcloud
from compas.geometry import Box, Frame, Translation
from compas_view2.app import App

# ==============================================================================
# Parameters
# ==============================================================================

N = 500
W = 10
H = 5
D = 7

# ==============================================================================
# Objects
# ==============================================================================

world = Frame.worldXY()
cloud = Pointcloud.from_bounds(W, D, H, N)
bounds = Box(world, W, D, H)
box = Box(world, 2, 2, 2)

T = Translation.from_vector([0.5 * W, 0.5 * D, 0.5 * H])
bounds.transform(T)
box.transform(T)

# ==============================================================================
# Visualize
# ==============================================================================

viewer = App()

viewer.add(bounds, show_faces=False, show_edges=True)
viewer.add(box, show_faces=False, show_edges=True, linewidth=5)

for point in cloud:
    if box.contains(point):
        color = (1, 0, 0)
        size = 15
    else:
        color = (0, 0, 0)
        size = 5
    viewer.add(point, color=color, size=size)

viewer.run()