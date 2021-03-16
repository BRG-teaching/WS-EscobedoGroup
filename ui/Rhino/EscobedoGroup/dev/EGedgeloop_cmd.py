from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os

import scriptcontext as sc  # type: ignore
import compas_rhino

from compas.utilities import flatten
from compas_rhino.objects import MeshObject


__commandname__ = "EGedgeloop"


HERE = compas_rhino.get_document_dirname()
HOME = os.path.expanduser('~')
CWD = HERE or HOME


def RunCommand(is_interactive):

    if 'EG' not in sc.sticky:
        compas_rhino.display_message("EscobedoGroup UI no available.")
        return

    mesh = sc.sticky["EG"].get('mesh')
    if not mesh:
        compas_rhino.display_message("No mesh is loaded.")
        return

    obj = MeshObject(mesh, layer="HiLo::Mesh")
    obj.clear_layer()
    obj.draw()

    compas_rhino.rs.EnableRedraw(True)
    compas_rhino.rs.Redraw()

    edges = obj.select_edges()
    if not edges:
        return

    loops = []
    for edge in edges:
        loop = mesh.edge_loop(edge)
        loops.append(loop)

    obj.settings['color.edges'] = {}
    obj.settings['color.edges'].update({(u, v): (255, 0, 0) for u, v in flatten(loops)})
    obj.settings['color.edges'].update({(v, u): (255, 0, 0) for u, v in flatten(loops)})

    obj.clear()
    obj.draw()

    compas_rhino.rs.EnableRedraw(True)
    compas_rhino.rs.Redraw()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
