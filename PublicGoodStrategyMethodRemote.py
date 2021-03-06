# -*- coding: utf-8 -*-

import logging
import random

from twisted.internet import defer
from client.cltremote import IRemote
import PublicGoodStrategyMethodParams as pms
from PublicGoodStrategyMethodGui import GuiInconditionnel, GuiConditionnel
import PublicGoodStrategyMethodTexts as texts_PGSM


logger = logging.getLogger("le2m")


class RemotePGSM(IRemote):
    """
    Class remote, remote_ methods can be called by the server
    """
    def __init__(self, le2mclt):
        IRemote.__init__(self, le2mclt)
        # self._histo_vars = [
        #     "PGSM_period", "PGSM_decision",
        #     "PGSM_periodpayoff", "PGSM_cumulativepayoff"]
        # self._histo.append(texts_PGSM.get_histo_head())

    def remote_configure(self, params):
        """
        Set the same parameters as in the server side
        :param params:
        :return:
        """
        logger.info(u"{} configure".format(self._le2mclt.uid))
        for k, v in params.viewitems():
            setattr(pms, k, v)

    def remote_newperiod(self, period):
        """
        Set the current period and delete the history
        :param period: the current period
        :return:
        """
        logger.info(u"{} Period {}".format(self._le2mclt.uid, period))
        self.currentperiod = period
        if self.currentperiod == 1:
            del self.histo[1:]


    def remote_display_inconditionnel(self):
        """
        Display the decision screen
        :return: deferred
        """
        logger.info(u"{} Decision".format(self._le2mclt.uid))
        if self._le2mclt.simulation:
            decision = random.randrange(
                    pms.DECISION_MIN,
                    pms.DECISION_MAX + pms.DECISION_STEP,
                    pms.DECISION_STEP)
            logger.info(u"{} Send back {}".format(self._le2mclt.uid, decision))
            return decision
        else: 
            defered = defer.Deferred()
            ecran_decision = GuiInconditionnel(
                defered, self._le2mclt.automatique, self._le2mclt.screen)
            ecran_decision.show()
            return defered

    def remote_display_conditionnel(self):
        """
        Display the decision screen
        :return: deferred
        """
        logger.info(u"{} Decision".format(self._le2mclt.uid))
        if self._le2mclt.simulation:
            decisions = {}
            for i in range(21):
                decisions[
                    "conditionnel_{}".format(i)] = random.randrange(
                    pms.DECISION_MIN,
                    pms.DECISION_MAX + pms.DECISION_STEP,
                    pms.DECISION_STEP)
            logger.info(
                u"{} Send back {}".format(self._le2mclt.uid, decisions))
            return decisions
        else:
            defered = defer.Deferred()
            ecran_conditionnel = GuiConditionnel(
                defered, self._le2mclt.automatique, self._le2mclt.screen)
            ecran_conditionnel.show()
            return defered

    def remote_set_period_content(self, period_content):
        txt = texts_PGSM.get_text_final(period_content)
        # txt += u"<br />" + self.payoff_text
        self.payoff_text = txt

    def remote_display_payoffs(self):
        logger.debug(u"{} display_payoffs".format(self.le2mclt.uid))
        return self.le2mclt.get_remote("base").remote_display_information(
            self.payoff_text, screensize=(450, 180))

    # def remote_display_summary(self, period_content):
    #     """
    #     Display the summary screen
    #     :param period_content: dictionary with the content of the current period
    #     :return: deferred
    #     """
    #     logger.info(u"{} Summary".format(self._le2mclt.uid))
    #     self.histo.append([period_content.get(k) for k in self._histo_vars])
    #     if self._le2mclt.simulation:
    #         return 1
    #     else:
    #         defered = defer.Deferred()
    #         ecran_recap = GuiRecapitulatif(
    #             defered, self._le2mclt.automatique, self._le2mclt.screen,
    #             self.currentperiod, self.histo,
    #             texts_PGSM.get_text_summary(period_content))
    #         ecran_recap.show()
    #         return defered
