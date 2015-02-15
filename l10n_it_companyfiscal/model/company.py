# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 KTec S.r.l.
#    (<http://www.ktec.it>).
#
#    Copyright (C) 2014 Associazione Odoo Italia
#    (<http://www.odoo-italia.org>).
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

RF = [('RF01', 'Ordinario'),
      ('RF02', 'Contribuenti minimi (art.1, c.96-117, L. 244/07) '),
      ('RF03', 'Nuove iniziative produttive (art.13, L. 388/00) '),
      ('RF04', 'Agricoltura e attivita connesse e pesca (artt.34 e 34-bis, DPR 633/72) '),
      ('RF05', 'Vendita sali e tabacchi (art.74, c.1, DPR. 633/72)'),
      ('RF06', 'Commercio fiammiferi (art.74, c.1, DPR 633/72) '),
      ('RF07', 'Editoria (art.74, c.1, DPR 633/72)'),
      ('RF08', 'Gestione servizi telefonia pubblica (art.74, c.1, DPR 633/72)'),
      ('RF09', 'Rivendita documenti di trasporto pubblico e di sosta (art.74, c.1, DPR 633/72)'),
      ('RF10', 'Intrattenimenti, giochi e altre attivita di cui alla tariffa allegata '
               'al DPR 640/72 (art.74, c.6, DPR 633/72)'),
      ('RF11', 'Agenzie viaggi e turismo (art.74-ter, DPR 633/72)'),
      ('RF12', 'Agriturismo (art.5, c.2, L. 413/91)'),
      ('RF13', 'Vendite a domicilio (art.25-bis, c.6, DPR 600/73)'),
      ('RF14', 'Rivendita beni usati, oggetti d’arte, d’antiquariato o da collezione (art.36, DL 41/95)'),
      ('RF15', 'Agenzie di vendite all’asta di oggetti d’arte, antiquariato o da collezione (art.40-bis, DL 41/95)'),
      ('RF16', 'IVA per cassa P.A. (art.6, c.5, DPR 633/72)'),
      ('RF17', 'IVA per cassa soggetti con vol. d’affari inferiore ad euro 200.000 (art.7, DL 185/2008)'),
      ('RF18', 'Altro'),
      ('RF19', 'Regime forfettario (art.1, c.54-89, L. 190/2014)')]


class res_company(models.Model):

    _inherit = "res.company"

    capitale_sociale = fields.Float(
        string='Capital'
    )
    socio_unico = fields.Boolean(
        string='Sole Shareholder'
    )
    stato_liquidazione = fields.Boolean(
        string='Closeout'
    )
    regime_fiscale = fields.Selection(RF,
        string='Tax Regime'
    )
