import os
from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
FILE = os.path.join(DATA, 'mesh.json')

mesh = Mesh.from_json(FILE)

artist = MeshArtist(mesh, layer="HiLo::Mesh")
artist.clear_layer()

boundary = mesh.vertices_on_boundary()
special5 = list(mesh.vertices_where({'vertex_degree': 5}))
special6 = list(mesh.vertices_where({'vertex_degree': 6}))

color = {vertex: (255, 0, 0) for vertex in boundary}
color.update({vertex: (0, 255, 0) for vertex in special5})
color.update({vertex: (0, 0, 255) for vertex in special6})

artist.draw_vertices(
    vertices=boundary + special5 + special6,
    color=color
)

color = {face: (0, 255, 0) for vertex in special5 for face in mesh.vertex_faces(vertex)}

for vertex in special6:
    for nbr in mesh.vertex_neighbors(vertex):
        edges = mesh.edge_loop((vertex, nbr))
        for edge in edges:
            left, right = mesh.edge_faces(*edge)
            color[left] = (0, 255, 255)
            color[right] = (255, 255, 0)

color.update({face: (255, 0, 0) for face in mesh.faces_on_boundary()})
color.update({face: (0, 0, 255) for vertex in special6 for face in mesh.vertex_faces(vertex)})

artist.draw_faces(
    color=color
)
