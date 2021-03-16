import ast

import Rhino  # type: ignore
import clr  # type: ignore

clr.AddReference('Rhino.UI')
import Rhino.UI  # type: ignore

try:
    from compas_rhino.forms import PropertyListForm
except ImportError:
    from Rhino.UI.Dialogs import ShowPropertyListBox  # type: ignore


def _update_named_values(names, values, message='', title='Update named values'):
    try:
        dialog = PropertyListForm(names, values)
    except Exception:
        values = ShowPropertyListBox(message, title, names, values)
    else:
        if dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow):
            values = dialog.values
        else:
            values = None
    return values


def mesh_update_vertex_attributes(mesh, vertices, names=None):
    """Update the attributes of selected vertices of a given datastructure.

    Parameters
    ----------
    mesh : compas.datastructures.Datastructure
        The data structure.
    vertices : list
        The vertices of the vertices of which the attributes should be updated.
    names : list, optional
        The names of the attributes that should be updated.
        Default is to update all available attributes.

    Returns
    -------
    bool
        True if the attributes were successfully updated.
        False otherwise.

    """
    names = names or mesh.default_vertex_attributes.keys()
    names = sorted(names)
    values = mesh.vertex_attributes(vertices[0], names)
    if len(vertices) > 1:
        for i, name in enumerate(names):
            for vertex in vertices[1:]:
                if values[i] != mesh.vertex_attribute(vertex, name):
                    values[i] = '-'
                    break
    values = map(str, values)
    values = _update_named_values(names, values)
    if values:
        for name, value in zip(names, values):
            if value == '-':
                continue
            for vertex in vertices:
                try:
                    mesh.vertex_attribute(vertex, name, ast.literal_eval(value))
                except (ValueError, TypeError):
                    mesh.vertex_attribute(vertex, name, value)
        return True
    return False
