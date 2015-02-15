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

import base64
import datetime
from openerp import models, fields, api, _
from openerp.exceptions import except_orm
from PyFePA import siamm
from PyFePA.siamm import ValidateException



class generate_siammxml(models.TransientModel):

    _name = "generate.siammxml"
    _description = "Generate SIAMM xml"

    @api.one
    def generate_xml(self):
        active_id = self._context.get('active_id')
        invoice = self.env['account.invoice'].browse(active_id)

        if not invoice.siamm_intercettazioni or not invoice.number:
            raise except_orm(_('Error!'),
                             _('File SIAMM generabile solo su fatture intercettazioni confermate'))

        siamm_data = {'beneficiario': invoice.company_id.vat,
                      'tipopagamento': 'AC',
                      'id': 1,
                      'entepagante': invoice.siamm_entepagante,
                      'numerofattura': invoice.number,
                      'registro': invoice.siamm_registro,
                      'datafattura': datetime.datetime.strptime(invoice.date_invoice, '%Y-%m-%d'),
                      'importototale': invoice.amount_untaxed,
                      'importoiva': invoice.amount_tax,
                      'nr_rg': invoice.siamm_nrrg,
                      'sede': invoice.siamm_sede,
                      'numeromodello37': invoice.siamm_numeromodello37,
                      'datainizioprestazione': datetime.datetime.strptime(invoice.siamm_datainizioprestazione,
                                                                          '%Y-%m-%d'),
                      'datafineprestazione': datetime.datetime.strptime(invoice.siamm_datafineprestazione,
                                                                        '%Y-%m-%d'),
                      'nomemagistrato': invoice.siamm_cognomemagistrato,
                      'cognomemagistrato': invoice.siamm_nomemagistrato,
                      'tipointercettazione': invoice.siamm_tipointercettazione}

        filename = 'FEPA_SIAMM_' + invoice.number.replace('/','-')


        try:
            datas = base64.encodestring(siamm.serialize(siamm_data))
        except ValidateException as ve:
            raise except_orm(_('Error!'),
                             _('Errore nella validazione mod37: ' + invoice.siamm_numeromodello37 + ' ' + str(ve)))

        attachment = self.env['ir.attachment'].create({'name': filename,
                                                       'datas_fname': filename,
                                                       'datas': datas,
                                                       'res_model': 'account.invoice',
                                                       'res_id': invoice.id
                                                       })