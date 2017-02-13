# -*- coding: utf-8 -*-

import logging
from collections import OrderedDict
from twisted.internet import defer
from util import utiltools
from util.utili18n import le2mtrans
import PublicGoodStrategyMethodParams as pms
from PublicGoodStrategyMethodTexts import trans_PGSM
from random import choice
import numpy as np
from PublicGoodStrategyMethodGui import DConfigure


logger = logging.getLogger("le2m.{}".format(__name__))


class Serveur(object):
    def __init__(self, le2mserv):
        self._le2mserv = le2mserv

        # creation of the menu (will be placed in the "part" menu on the
        # server screen)
        actions = OrderedDict()
        actions[le2mtrans(u"Configure")] = self._configure
        actions[le2mtrans(u"Display parameters")] = \
            lambda _: self._le2mserv.gestionnaire_graphique. \
            display_information2(
                utiltools.get_module_info(pms), le2mtrans(u"Parameters"))
        actions[le2mtrans(u"Start")] = lambda _: self._demarrer()
        actions[le2mtrans(u"Display payoffs")] = \
            lambda _: self._le2mserv.gestionnaire_experience.\
            display_payoffs_onserver("PublicGoodStrategyMethod")
        self._le2mserv.gestionnaire_graphique.add_topartmenu(
            u"Public Good - Strategy Method", actions)

    def _configure(self):
        screen_configure = DConfigure(self._le2mserv.gestionnaire_graphique.screen)
        if screen_configure.exec_():
            self._le2mserv.gestionnaire_graphique.infoserv(
                trans_PGSM(u"Treatment") + u": {}".format(
                    pms.TREATMENTS_NAMES[pms.TREATMENT]))
            self._le2mserv.gestionnaire_graphique.infoserv(
                trans_PGSM(u"Groups' size") + u": {}".format(pms.TAILLE_GROUPES))
            self._le2mserv.gestionnaire_graphique.infoserv(
                trans_PGSM(u"Rate for the individual account") + u": {}".format(
                    pms.TAUX_CI))
            self._le2mserv.gestionnaire_graphique.infoserv(
                trans_PGSM(u"Rate for the collective account") + u": {}".format(
                    pms.TAUX_CC))

    @defer.inlineCallbacks
    def _demarrer(self):
        """
        Start the part
        :return:
        """
        # check conditions =====================================================
        if not self._le2mserv.gestionnaire_graphique.question(
                        le2mtrans(u"Start") + u" PublicGoodStrategyMethod?"):
            return

        # init part ============================================================
        yield (self._le2mserv.gestionnaire_experience.init_part(
            "PublicGoodStrategyMethod", "PartiePGSM",
            "RemotePGSM", pms))
        self._tous = self._le2mserv.gestionnaire_joueurs.get_players(
            'PublicGoodStrategyMethod')

        # set parameters on remotes
        yield (self._le2mserv.gestionnaire_experience.run_step(
            le2mtrans(u"Configure"), self._tous, "configure"))
        
        # form groups
        if pms.TAILLE_GROUPES > 0:
            try:
                self._le2mserv.gestionnaire_groupes.former_groupes(
                    self._le2mserv.gestionnaire_joueurs.get_players(),
                    pms.TAILLE_GROUPES, forcer_nouveaux=True)
            except ValueError as e:
                self._le2mserv.gestionnaire_graphique.display_error(
                    e.message)
                return
    
        # Start part ===========================================================
        for period in range(1 if pms.NOMBRE_PERIODES else 0,
                        pms.NOMBRE_PERIODES + 1):

            if self._le2mserv.gestionnaire_experience.stop_repetitions:
                break

            # init period
            self._le2mserv.gestionnaire_graphique.infoserv(
                [None, le2mtrans(u"Period") + u" {}".format(period)])
            self._le2mserv.gestionnaire_graphique.infoclt(
                [None, le2mtrans(u"Period") + u" {}".format(period)],
                fg="white", bg="gray")
            yield (self._le2mserv.gestionnaire_experience.run_func(
                self._tous, "newperiod", period))
            
            # decision
            yield(self._le2mserv.gestionnaire_experience.run_step(
                le2mtrans(u"Decision"), self._tous, "display_decision"))

            # dans chaque groupe on en choisit un pour une décision
            # inconditionnelle et l'autre pour une décision conditionnelle
            for k, v in self._le2mserv.gestionnaire_groupes.get_groupes(
                    "PublicGoodStrategyMethod").viewitems():
                cond_player = choice(v)
                cond_player.currentperiod.PGSM_payoff_decision_type = pms.CONDITIONNELLE
                incond_dec = []
                for j in v:
                    if j == cond_player:
                        continue
                    j.currentperiod.PGSM_payoff_decision_type = pms.INCONDITIONNELLE
                    incond_dec.append(j.currentperiod.PGSM_inconditionnel)
                incond_mean = int(np.around(np.mean(incond_dec), decimals=0))
                cond_dec = getattr(cond_player.currentperiod,
                                   "PGSM_conditionnel_{}".format(incond_mean))
                total_groupe = np.sum(incond_dec) + cond_dec
                for j in v:
                    j.currentperiod.PGSM_payoff_decision_incond_mean = incond_mean
                    j.currentperiod.PGSM_payoff_decision_cond = cond_dec
                    j.currentperiod.PGSM_public_account = total_groupe
                self._le2mserv.gestionnaire_graphique.infoserv(
                    u"G{}: cond. {}, incond. mean {}, cond. {} -> total {}".format(
                        k.split("_")[2], cond_player.joueur, incond_mean, cond_dec,
                        total_groupe))

            # period payoffs
            self._le2mserv.gestionnaire_experience.compute_periodpayoffs(
                "PublicGoodStrategyMethod")
        
            # summary
            # yield(self._le2mserv.gestionnaire_experience.run_step(
            #     le2mtrans(u"Summary"), self._tous, "display_summary"))
        
        # End of part ==========================================================
        yield (self._le2mserv.gestionnaire_experience.finalize_part(
            "PublicGoodStrategyMethod"))
