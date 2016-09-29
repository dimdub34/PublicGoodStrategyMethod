# -*- coding: utf-8 -*-
"""
This module contains the texts of the part (server and remote)
"""

from util.utiltools import get_pluriel
import PublicGoodStrategyMethodParams as pms
from util.utili18n import le2mtrans
import os
import configuration.configparam as params
import gettext
import logging

logger = logging.getLogger("le2m")
localedir = os.path.join(params.getp("PARTSDIR"), "PublicGoodStrategyMethod", "locale")
try:
    trans_PGSM = gettext.translation(
      "PublicGoodStrategyMethod", localedir, languages=[params.getp("LANG")]).ugettext
except IOError:
    logger.critical(u"Translation file not found")
    trans_PGSM = lambda x: x  # if there is an error, no translation


# def get_histo_head():
#     return [le2mtrans(u"Period"), le2mtrans(u"Decision"),
#              le2mtrans(u"Period\npayoff"), le2mtrans(u"Cumulative\npayoff")]


def get_text_explanation_incond():
    return trans_PGSM(u"Vous disposez d'une dotation de {}.").format(
        get_pluriel(pms.DOTATION, trans_PGSM(u"jeton")))


def get_text_label_incond():
    return trans_PGSM(u"Saisissez le nombre de jetons que vous placez sur "
                      u"le compte collectif")


def get_text_explanation_cond():
    txt = trans_PGSM(u"Vous disposez d'une dotation de {}.").format(
        get_pluriel(pms.DOTATION, trans_PGSM(u"jeton")))
    txt += u"\n"
    if pms.TAILLE_GROUPES > 2 :
        txt += trans_PGSM(u"Saisissez le nombre de jetons que vous placez sur "
                          u"le compte collectif pour chaque placement "
                          u"moyen effectué par les autres membres de votre "
                          u"groupe.")
    else:
        txt += trans_PGSM(u"Saisissez le nombre de jetons que vous placez sur "
                          u"le compte collectif pour chaque placement "
                          u"effectué par l'autre membre de votre groupe.")
    return txt


def get_text_final(period_content):
    txt = u""
    if period_content["PGSM_payoff_decision_type"] == pms.INCONDITIONNELLE:
        txt += trans_PGSM(u"C'est votre décision inconditionnelle qui a été "
                          u"prise en compte. Vous avez placé {} sur le "
                          u"compte collectif.").format(
            get_pluriel(period_content["PGSM_inconditionnel"], u"jeton"))
    else:
        txt += trans_PGSM(u"C'est votre décision conditionnelle qui a été "
                          u"prise en compte.")
        if pms.TAILLE_GROUPES > 2:
            txt += trans_PGSM(u"Les autres membres de votre groupe "
                              u"ont en moyenne placé {} sur le compte collectif, "
                              u"et donc vous {}.").format(
                get_pluriel(period_content["PGSM_payoff_decision_incond_mean"],
                            u"jeton"),
                get_pluriel(period_content["PGSM_payoff_decision_cond"],
                            u"jeton"))
        else:
            txt += trans_PGSM(u"L'autre membres de votre groupe a placé {} "
                              u"sur le compte collectif, et donc "
                              u"vous {}.").format(
                get_pluriel(period_content["PGSM_payoff_decision_incond_mean"],
                            u"jeton"),
                get_pluriel(period_content["PGSM_payoff_decision_cond"],
                            u"jeton"))

    txt += trans_PGSM(u" Au total votre groupe a placé {} sur le compte "
                      u"collectif. "
                      u"Votre gain est donc de {} (compte individuel) + "
                      u"{} (compte collectif) = {}.").format(
        get_pluriel(period_content["PGSM_public_account"], u"jeton"),
        period_content["PGSM_payoff_indiv_account"],
        period_content["PGSM_payoff_public_account"],
        get_pluriel(period_content["PGSM_periodpayoff"], pms.MONNAIE))
    return txt

