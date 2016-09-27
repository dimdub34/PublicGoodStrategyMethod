# -*- coding: utf-8 -*-
"""=============================================================================
This modules contains the variables and the parameters.
Do not change the variables.
Parameters that can be changed without any risk of damages should be changed
by clicking on the configure sub-menu at the server screen.
If you need to change some parameters below please be sure of what you do,
which means that you should ask to the developer ;-)
============================================================================="""

# variables --------------------------------------------------------------------
TREATMENTS = {0: "baseline"}
INCONDITIONNELLE = 0
CONDITIONNELLE = 1

# parameters -------------------------------------------------------------------
TREATMENT = 0
TAUX_CONVERSION = 0.5
NOMBRE_PERIODES = 0
TAILLE_GROUPES = 2
GROUPES_CHAQUE_PERIODE = False
MONNAIE = u"ecu"
DOTATION = 20
MPCR = 0.5

# DECISION
DECISION_MIN = 0
DECISION_MAX = DOTATION
DECISION_STEP = 1


def get_treatment(code_or_name):
    if type(code_or_name) is int:
        return TREATMENTS.get(code_or_name, None)
    elif type(code_or_name) is str:
        for k, v in TREATMENTS.viewitems():
            if v.lower() == code_or_name.lower():
                return k
    return None
