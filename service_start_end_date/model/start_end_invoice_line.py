# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 KTec S.r.l.
#    (<http://www.ktec.it>).
#
#    Copyright (C) 2014 Associazione Odoo Italia
#    (<http://www.openerp-italia.org>).
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

from openerp import models, fields, api, _
from openerp.exceptions import except_orm

class start_end_invoice_line(models.Model):
    _inherit = 'account.invoice.line'

    start_date = fields.Date(
        string='Start Date'
    )

    end_date = fields.Date(
        string='Start Date'
    )

    @api.one
    @api.constrains('start_date', 'end_sate')
    def _check_start_end_dates(self):
        if self.start_date and not self.end_date:
            raise except_orm(
                _('Error:'),
                _("Missing End Date for sale order line with "
                    "Description '%s'.")
                % (line.name))
        if self.end_date and not self.start_date:
            raise except_orm(
                _('Error:'),
                _("Missing Start Date for sale order line with "
                    "Description '%s'.")
                % (line.name))
        if self.end_date and self.start_date and \
                self.start_date > self.end_date:
            raise except_orm(
                _('Error:'),
                _("Start Date should be before or be the same as "
                    "End Date for sale order line with Description '%s'.")
                % (self.name))
        return True