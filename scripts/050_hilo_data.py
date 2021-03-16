import os
from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
FILE = os.path.join(DATA, 'mesh.json')

mesh = Mesh.from_json(FILE)

artist = MeshArtist(mesh, layer="HiLo::Mesh")
artist.clear_layer()

artist.draw()
