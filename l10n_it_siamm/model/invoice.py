# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 KTec S.r.l.
#    (<http://www.ktec.it>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models
from openerp import fields


EP = [('F', 'Funzionario Delegato'),
      ('T', 'Sezione tesoreria provinciale dello stato'),
      ('C', 'Concessionario'),
      ('P', 'Ufficio Postale')]

RG = [('M8P', "Mod. 8"),
      ('M9P', "Mod. 9"),
      ('M10P', "Mod. 10"),
      ('M11P', "Mod. 11"),
      ('M12P', "Mod. 12"),
      ('M13P', "Mod. 13"),
      ('M14P', "Mod. 14"),
      ('M15P', "Mod. 15"),
      ('NOTI', "Mod. 21"),
      ('NOTIB', "Mod. 21 BIS"),
      ('M22P', "Mod. 22"),
      ('M35P', "Mod. 35"),
      ('M36P', "Mod. 36"),
      ('M37P', "Mod. 37"),
      ('M38P', "Mod. 38"),
      ('M39P', "Mod. 39"),
      ('M40P', "Mod. 40"),
      ('M42P', "Mod. 42"),
      ('IGN', "Mod. 44"),
      ('M45P', "Mod. 45"),
      ('M46P', "Mod. 46"),
      ('M52P', "Mod. 52"),
      ('M53P', "Mod. 53"),
      ('M54P', "Mod. 54"),
      ('MAIP', "registro attivita investigative preventive")]

TI = [('A', 'ambientale con noleggio'),
      ('B', 'ambientale senza noleggio'),
      ('C', 'noleggio apparecchiature'),
      ('I', 'informatiche'),
      ('D', 'tabulati e/o documentazione traffico'),
      ('T', 'telefonia fissa'),
      ('M', 'telefonia mobile'),
      ('N', 'internazionali')]


class account_invoice(models.Model):
    _inherit = 'account.invoice'

    siamm_intercettazioni = fields.Boolean(
        string='Fattura Intercettazioni'
    )
    siamm_entepagante = fields.Selection(EP,
        string='Ente Pagante', default='F'
    )
    siamm_numeromodello37 = fields.Char(
        string='Numero Modello 37', size=11
    )
    siamm_registro = fields.Selection(RG,
        string='Mod. Registro'
    )
    siamm_nrrg = fields.Char(
        string='NR RG', size=11
    )
    siamm_sede = fields.Char(
        string='Sede'
    )
    siamm_datainizioprestazione = fields.Date(
        string='Data Inizio Prestazione'
    )
    siamm_datafineprestazione = fields.Date(
        string='Data Fine Prestazione'
    )
    siamm_nomemagistrato = fields.Char(
        string='Nome Magistrato'
    )
    siamm_cognomemagistrato = fields.Char(
        string='Cognome Magistrato'
    )
    siamm_tipointercettazione = fields.Selection(TI,
        string='Tipo Intercettazione'
    )
    inter_decreto = fields.Char(
        string='Numero Decreto'
    )
    inter_organopg = fields.Many2one('res.partner',
        string='Organo PG',
    )