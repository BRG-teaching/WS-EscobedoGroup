from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import scriptcontext as sc  # type: ignore
import compas_rhino


__commandname__ = "EGsavemesh"


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

    folder = compas_rhino.select_folder()
    if not folder:
        return

    path = os.path.join(folder, 'mesh_update.json')

    mesh.to_json(path)

    compas_rhino.display_message("Mesh saved in {}.".format(path))


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
