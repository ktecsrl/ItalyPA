# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 KTec S.r.l.
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

class siamm_sedi(models.Model):

    _name = 'l10n_it_siamm.siamm_sedi'

    siamm_id_sede = fields.Char(string='Identificativo SIAMM per le Sedi')
    siamm_descrizione_sede = fields.Char(string='Siamm Descrizione')
    siamm_sede = fields.Char(string='Siamm sede')
    name = fields.Char(string='Descrizone della Sede', compute='_sede', store=True)

    @api.depends('siamm_descrizione_sede', 'siamm_sede')
    def _sede(self):
        name = self.siamm_sede + ' - ' + self.siamm_descrizione_sede