import os
from pathlib import Path

from mydevoirs.constants import BASE_DIR

"""
On dispatch les datas sous la forme :
    type_nom : "nom_du_fichier"
qui donnera le path : racine_de_base/data/genres/nom_du_fichier

Permet :
- de gerer le root pour  dev et pyinstaller
- utiliser des variables  pour désigner les datas
"""

DATAS = {
    "icon_precedant": "chevron-left.png",
    "icon_suivant": "chevron-right.png",
    "icon_agenda": "014-calendar.png",
    "icon_todo": "010-test.png",
    "icon_new": "012-add.png",
    "icon_remove": "garbage.png",
    "icon_unchecked": "017-cancel.png",
    "icon_checked": "apply-64.png",
    "icon_logo": "logo.png",
    "icon_settings": "params.png",
    "icon_aide": "qmark.png",
    "icon_colorchooser": "colorchooser.png",
    "icon_arrowmove": "arrowmove.png",
}

def get_datas():
    res = {}
    for k, v in DATAS.items():

        genre, nom = k.split("_")
        res[k] = os.path.join(BASE_DIR, "data", genre + "s", v)
        res[k] = str(BASE_DIR / "data" / (genre + "s") / v)
    return res
