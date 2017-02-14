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
BASELINE = 0
TREATMENTS_NAMES = {BASELINE: "BASELINE"}
INCONDITIONNELLE = 0
CONDITIONNELLE = 1

# parameters -------------------------------------------------------------------
TREATMENT = 0
TAUX_CONVERSION = 1
NOMBRE_PERIODES = 0
TAILLE_GROUPES = 5
GROUPES_CHAQUE_PERIODE = False
MONNAIE = u"ecu"
DOTATION = 20

TAUX_CI = 1
TAUX_CC = 0.5

# DECISION
DECISION_MIN = 0
DECISION_MAX = DOTATION
DECISION_STEP = 1

