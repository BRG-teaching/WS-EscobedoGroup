from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import scriptcontext as sc  # type: ignore
import compas_rhino

from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist


__commandname__ = "EGloadmesh"


HERE = compas_rhino.get_document_dirname()
HOME = os.path.expanduser('~')
CWD = HERE or HOME


def RunCommand(is_interactive):

    if 'EG' not in sc.sticky:
        compas_rhino.display_message("EscobedoGroup UI no available.")
        return

    path = compas_rhino.select_file(folder=CWD, filter='JSON files (*.json)|*.json||')
    if not path:
        return

    mesh = Mesh.from_json(path)
    artist = MeshArtist(mesh, layer="HiLo::Mesh")
    artist.clear_layer()
    artist.draw()

    compas_rhino.rs.EnableRedraw(True)
    compas_rhino.rs.Redraw()

    sc.sticky["EG"] = {
        'mesh': mesh
    }
    compas_rhino.display_message("Mesh loaded.")


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
