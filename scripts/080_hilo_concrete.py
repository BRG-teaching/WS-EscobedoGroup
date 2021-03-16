import os
import compas
from compas.utilities import pairwise

from compas_rhino.artists import MeshArtist

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
FILE = os.path.join(DATA, 'session.json')

session = compas.json_load(FILE)

mesh = session['mesh']

# ==============================================================================
# Idos
# ==============================================================================

idos = mesh.copy()

for face in mesh.faces_where({'is_loaded': False}):
    idos.delete_face(face)
idos.remove_unused_vertices()

offset = 0.02

for vertex, attr in idos.vertices(True):
    x, y, z = mesh.vertex_coordinates(vertex)
    nx, ny, nz = mesh.vertex_normal(vertex)

    if attr['nx'] is not None:
        nx = attr['nx']
    if attr['ny'] is not None:
        ny = attr['ny']
    if attr['nz'] is not None:
        nz = attr['nz']

    attr['x'] = x + offset * nx
    attr['y'] = y + offset * ny
    attr['z'] = z + offset * nz

# ==============================================================================
# Edos
# ==============================================================================

edos = idos.copy()

offset = 0.06

for vertex, attr in edos.vertices(True):

    x, y, z = idos.vertex_coordinates(vertex)
    nx, ny, nz = idos.vertex_normal(vertex)

    if attr['nx'] is not None:
        nx = attr['nx']
    if attr['ny'] is not None:
        ny = attr['ny']
    if attr['nz'] is not None:
        nz = attr['nz']

    attr['x'] = x + offset * nx
    attr['y'] = y + offset * ny
    attr['z'] = z + offset * nz

# ==============================================================================
# Volume
# ==============================================================================

volume = idos.copy()

volume.flip_cycles()

max_vertex = volume._max_vertex + 1
max_face = volume._max_face + 1

for vertex, attr in edos.vertices(True):
    volume.add_vertex(key=vertex + max_vertex, **attr)

for face in edos.faces():
    vertices = edos.face_vertices(face)
    vertices = [vertex + max_vertex for vertex in vertices]
    volume.add_face(vertices)

boundary = edos.vertices_on_boundary()
boundary.append(boundary[0])

for a, b in pairwise(boundary):
    volume.add_face([b, a, a + max_vertex, b + max_vertex])

# ==============================================================================
# Export
# ==============================================================================

session['idos'] = idos
session['edos'] = edos
session['volume'] = volume

compas.json_dump(session, FILE)

# ==============================================================================
# visualize
# ==============================================================================

artist = MeshArtist(idos, layer="HiLo::Concrete1::Idos")
artist.clear_layer()
artist.draw_mesh(disjoint=True, color=(255, 0, 0))

artist = MeshArtist(edos, layer="HiLo::Concrete1::Edos")
artist.clear_layer()
artist.draw_mesh(disjoint=True, color=(0, 0, 255))

artist = MeshArtist(volume, layer="HiLo::Concrete1::Volume")
artist.clear_layer()
artist.draw_mesh(disjoint=True)
