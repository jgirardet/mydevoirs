
from mydevoirs.constants import MATIERES_TREE

def build_matiere(tree):
    mat = {}
    for k, v in tree.items():
        if isinstance(v, tuple):
            mat[k] = v
        else:
            # base = None
            for x, y in v.items():
                if not mat.get(k, None):
                    mat[k] = y
                mat[x] = y
    return mat


# MATIERES = build_matiere(MATIERES_TREE)