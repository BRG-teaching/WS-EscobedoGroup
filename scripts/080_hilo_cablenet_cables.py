import os
import compas
from compas.geometry import Line, Circle
from compas.geometry import project_point_plane, distance_point_point
from compas.geometry import subtract_vectors, normalize_vector, add_vectors, scale_vector
from compas.datastructures import Mesh
from compas_rhino.artists import LineArtist, CircleArtist

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
FILE_I = os.path.join(DATA, 'cablenet.json')
FILE_O = os.path.join(DATA, 'session.json')

# ==============================================================================
# Data
# ==============================================================================

mesh = Mesh.from_json(FILE_I)

mesh.attributes['radius'] = {
    'S': 0.023,
    'M': 0.0305,
    'L': 0.0275,
    'M_': 0.0275,
    'XL': 0.0375
}
mesh.attributes['bracket'] = {
    'S': 0.026,
    'M': 0.039,
    'L': 0.046,
    'M_': 0.046,
}
mesh.attributes['connector'] = {
    '6': 38,
    '8': 48,
    '10': 60,
    '12': 72,
    '14': 90,
    '16': 90
}
mesh.attributes['pin'] = {
    '6': 3.5,
    '8': 5,
    '10': 5,
    '12': 6.5,
    '14': 6.5,
    '16': 6.5,
}
mesh.attributes['hole'] = {
    '6': 4.5,
    '8': 5.5,
    '10': 5.5,
    '12': 7,
    '14': 7,
    '16': 7,
}
mesh.attributes['code'] = {
    '6' : '30948-0600-30',
    '8' : '30948-0800-30',
}

mesh.update_default_edge_attributes({
    'is_beam': False,
    'is_clamp': False,
})

# ==============================================================================
# Session
# ==============================================================================

session = {
    'mesh': mesh,
    'export': None
}

# ==============================================================================
# Beam Cables
# ==============================================================================

beam = []

for u in mesh.vertices_where({'is_beam': True}):

    nbrs = mesh.vertex_neighbors(u)
    v = None
    for nbr in nbrs:
        if mesh.vertex_attribute(nbr, 'is_anchor'):
            v = nbr
            break
    if v is None:
        continue

    nbrs = mesh.vertex_neighbors(v, ordered=True)
    i = nbrs.index(u)
    w = nbrs[i - 2]

    ring_w = mesh.vertex_attribute(w, 'ring')
    if not ring_w:
        continue

    length_uv = mesh.edge_length(u, v)
    size_uv = str(mesh.edge_attribute((u, v), 'size'))
    radius_w = mesh.attributes['radius'][ring_w]

    xyz_u = mesh.vertex_coordinates(u)
    xyz_w = mesh.vertex_coordinates(w)

    normal_w = mesh.vertex_normal(w)
    plane_w = xyz_w, normal_w

    u_on_plane_w = project_point_plane(xyz_u, plane_w)
    wu_dir = normalize_vector(subtract_vectors(u_on_plane_w, xyz_w))
    xyz_w_1 = add_vectors(xyz_w, scale_vector(wu_dir, radius_w))
    uw_dir_real = normalize_vector(subtract_vectors(xyz_w_1, xyz_u))
    wu_dir_real = normalize_vector(subtract_vectors(xyz_u, xyz_w_1))

    connector_u = mesh.attributes['connector'][size_uv]
    pin = mesh.attributes['pin'][size_uv]
    hole = mesh.attributes['hole'][size_uv]

    xyz_u_1 = add_vectors(xyz_u, scale_vector(uw_dir_real, 1e-3 * (0.5 * connector_u + 100)))
    xyz_u_2 = add_vectors(xyz_u, scale_vector(uw_dir_real, -1e-3 * 100))
    xyz_v_1 = add_vectors(xyz_u, scale_vector(uw_dir_real, length_uv - 1e-3 * (80 + 4 + 5 + pin)))

    mesh.edge_attribute((u, v), 'is_beam', True)
    mesh.edge_attribute((v, w), 'is_clamp', True)

    beam.append([
        Line(xyz_u_2, xyz_v_1),
        Line(xyz_v_1, xyz_w_1)
    ])

# ==============================================================================
# Internal Cables
# ==============================================================================

internal = []
export = {'6': [], '8': []}

for edge in mesh.edges_where({'is_edge': True, 'is_joint': False, 'is_beam': False, 'is_clamp': False}):
    u, v = edge

    # get data

    ring_u = mesh.vertex_attribute(u, 'ring') or 'S'
    ring_v = mesh.vertex_attribute(v, 'ring') or 'S'

    radius_u = mesh.attributes['radius'][ring_u]
    radius_v = mesh.attributes['radius'][ring_v]

    name = mesh.edge_attribute(edge, 'name')
    size = mesh.edge_attribute(edge, 'size')
    force = mesh.edge_attribute(edge, 'f')
    length = mesh.edge_attribute(edge, 'l')
    l0 = mesh.edge_attribute(edge, 'l0')
    eps = length/l0

    link_size = str(size)
    size = int(size)
    cap = 1.5 * (size + 2)

    if ring_u == 'S':
        bracket_u = mesh.attributes['bracket']['S']
    elif size in (6, 8, 10):
        bracket_u = mesh.attributes['bracket']['M']
    elif size in (12, 14):
        bracket_u = mesh.attributes['bracket']['L']

    if ring_v == 'S':
        bracket_v = mesh.attributes['bracket']['S']
    elif size in (6, 8, 10):
        bracket_v = mesh.attributes['bracket']['M']
    elif size in (12, 14):
        bracket_v = mesh.attributes['bracket']['L']

    # project onto the ring planes

    xyz_u = mesh.vertex_coordinates(u)
    xyz_v = mesh.vertex_coordinates(v)

    normal_u = mesh.vertex_normal(u)
    normal_v = mesh.vertex_normal(v)

    plane_u = xyz_u, normal_u
    plane_v = xyz_v, normal_v

    v_on_plane_u = project_point_plane(xyz_v, plane_u)
    u_on_plane_v = project_point_plane(xyz_u, plane_v)

    uv_dir = normalize_vector(subtract_vectors(v_on_plane_u, xyz_u))
    vu_dir = normalize_vector(subtract_vectors(u_on_plane_v, xyz_v))

    # ring to ring distances

    xyz_u_1 = add_vectors(xyz_u, scale_vector(uv_dir, radius_u))
    xyz_v_1 = add_vectors(xyz_v, scale_vector(vu_dir, radius_v))

    uv_dir_real = normalize_vector(subtract_vectors(xyz_v_1, xyz_u_1))
    vu_dir_real = normalize_vector(subtract_vectors(xyz_u_1, xyz_v_1))

    xyz_u_2 = add_vectors(xyz_u_1, scale_vector(uv_dir_real, bracket_u))
    xyz_v_2 = add_vectors(xyz_v_1, scale_vector(vu_dir_real, bracket_v))

    # length

    length = distance_point_point(xyz_u_2, xyz_v_2)
    length = length / eps
    confection_length = 1e3 * length + 2 * cap

    # for visualisation

    internal.append([
        Line(xyz_u_1, xyz_u_2),
        Line(xyz_u_2, xyz_v_2),
        Line(xyz_v_2, xyz_v_1)
    ])

    # for export

    if link_size in ('6', '8'):
        export[link_size].append({
            'Label'        : name or '-',
            'Code A'       : mesh.attributes['code'][link_size],
            'Code B'       : mesh.attributes['code'][link_size],
            'Edge Length'  : 1e3 * mesh.edge_length(u, v),
            'Ring A'       : 1e3 * radius_u,
            'Ring B'       : 1e3 * radius_v,
            'Bracket A'    : 1e3 * bracket_u,
            'Bracket B'    : 1e3 * bracket_v,
            'Cap A'        : cap,
            'Cap B'        : cap,
            'Cable Length' : 1e3 * length,
            'Confection Length' : confection_length,
        })

# ==============================================================================
# Joints
# ==============================================================================

# ==============================================================================
# Export
# ==============================================================================

session['export'] = export

compas.json_dump(session, FILE_O)

# ==============================================================================
# Visualize Rings
# ==============================================================================

for vertex in mesh.vertices_where({'is_beam': False, 'is_anchor': False}):
    ring = mesh.vertex_attribute(vertex, 'ring') or 'S'

    point = mesh.vertex_coordinates(vertex)
    normal = mesh.vertex_normal(vertex)
    plane = point, normal
    radius = mesh.attributes['radius'][ring]

    circle = Circle(plane, radius)
    artist = CircleArtist(circle, color=(255, 255, 255), layer="HiLo::Cablenet::Rings")
    artist.draw()

# ==============================================================================
# Visualize Internal Cables
# ==============================================================================

for bracket1, cable, bracket2 in internal:
    artist = LineArtist(bracket1, color=(0, 255, 255), layer="HiLo::Cablenet::Cables::Internal")
    artist.draw()

    artist = LineArtist(cable, color=(0, 0, 255), layer="HiLo::Cablenet::Cables::Internal")
    artist.draw()

    artist = LineArtist(bracket2, color=(0, 255, 255), layer="HiLo::Cablenet::Cables::Internal")
    artist.draw()

# ==============================================================================
# Visualize Boundary Cables
# ==============================================================================

for cable, plate in beam:
    artist = LineArtist(cable, color=(255, 255, 255), layer="HiLo::Cablenet::Cables::Beam")
    artist.draw()

    artist = LineArtist(plate, color=(0, 0, 0), layer="HiLo::Cablenet::Cables::Beam")
    artist.draw()
