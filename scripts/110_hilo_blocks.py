import os
import compas
from compas.utilities import pairwise
from compas.geometry import offset_polygon

from compas_rhino.artists import MeshArtist

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
FILE = os.path.join(DATA, 'session.json')

session = compas.json_load(FILE)

mesh = session['mesh']
edos = session['edos']

for face in edos.faces():

    vertices = edos.face_vertices(face)
    if len(vertices) != 4:
        continue

    # offsets

    normals = [edos.vertex_attributes(vertex, ['nx', 'ny', 'nz']) for vertex in vertices]
    points = [edos.vertex_coordinates(vertex) for vertex in vertices]
    distances = [mesh.edge_attribute(edge, 'offset') for edge in pairwise(vertices + vertices[0:1])]

    offset = offset_polygon(points, distances)

    base, normal = proxy.bestfit_plane_numpy(offset)

    plane1 = base, normalize_vector(normal)
    plane2 = add_vectors(plane1[0], scale_vector(plane1[1], THICKNESS)), plane1[1]

    bottom = []
    top = []
    for a, n in zip(offset, normals):
        b = add_vectors(a, n)
        x1 = intersection_line_plane((a, b), plane1)
        x2 = intersection_line_plane((a, b), plane2)
        bottom.append(x1)
        top.append(x2)

    # construct the block

    faces = [[0, 3, 2, 1], [4, 5, 6, 7], [3, 0, 4, 7], [2, 3, 7, 6], [1, 2, 6, 5], [0, 1, 5, 4]]
    mesh = Mesh.from_vertices_and_faces(bottom + top, faces)
    mesh.update_default_edge_attributes({'is_bottom': False})
    mesh.attributes['strip'] = stripname
    mesh.attributes['name'] = stripname
    mesh.attributes['fkey'] = fkey

    blocks.append(mesh)
