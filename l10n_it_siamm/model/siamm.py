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

from openerp import models,fields, api, _
from openerp.exceptions import except_orm, Warning
from PyFePA.fepa import *
from PyFePA import siamm
import base64


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
      ('N', 'internazionali'),
      ('GPS', 'GPS Video')]


class siamm_account_invoice(models.Model):
    _inherit = 'account.invoice'

    siamm_intercettazioni = fields.Boolean(
        string='Fattura Intercettazioni'
    )
    siamm_entepagante = fields.Selection(EP,
        string='Ente Pagante', default='F'
    )
    siamm_numeromodello37 = fields.Char(
        string='Decreto/Modello 37', size=11
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
    siamm_dataemissioneprovv = fields.Date(
        string='Data Emissione Provvedimento'
    )
    inter_decreto = fields.Char(
        string='Altro'
    )
    inter_nrvg = fields.Char(
        string='NR VG'
    )
    inter_organopg = fields.Many2one('res.partner',
        string='Organo PG',
    )
    inter_addsiam_toinvoice = fields.Boolean(
        string = 'Aggiungi SIAMM'
    )

    def _generate_siamm(invoice, id_siamm = None):

        company = invoice.company_id

        if not company:
            user_obj = invoice.pool['res.users']
            company = user_obj.company_id

        siamm_data = {'beneficiario': company.vat,
                      'tipopagamento': 'AC',
                      'id': id_siamm if id_siamm else 1,
                      'entepagante': invoice.siamm_entepagante if invoice.siamm_entepagante else None,
                      'numerofattura': invoice.number,
                      'registro': invoice.siamm_registro if invoice.siamm_registro else '',
                      'datafattura': datetime.datetime.strptime(invoice.date_invoice, '%Y-%m-%d'),
                      'importototale': invoice.amount_untaxed,
                      'importoiva': invoice.amount_tax,
                      'nr_rg': invoice.siamm_nrrg if invoice.siamm_registro else '',
                      'sede': invoice.siamm_sede if invoice.siamm_sede else '',
                      'numeromodello37': invoice.siamm_numeromodello37 if invoice.siamm_numeromodello37 else '',
                      'datainizioprestazione': datetime.datetime.strptime(invoice.siamm_datainizioprestazione,
                                                                          '%Y-%m-%d') if invoice.siamm_datainizioprestazione else '',
                      'datafineprestazione': datetime.datetime.strptime(invoice.siamm_datafineprestazione,
                                                                        '%Y-%m-%d') if invoice.siamm_datafineprestazione else '',
                      'nomemagistrato': invoice.siamm_cognomemagistrato if invoice.siamm_cognomemagistrato else None,
                      'cognomemagistrato': invoice.siamm_nomemagistrato if invoice.siamm_nomemagistrato else None,
                      'tipointercettazione': invoice.siamm_tipointercettazione if invoice.siamm_tipointercettazione else None}

        return siamm_data

    @api.multi
    def generate_siamm_xml(self,add_to=False):

        siamm_list_intercettazioni = []

        id_siamm = 1
        sequence_obj = self.pool['ir.sequence']
        id_file_siamm = sequence_obj.next_by_code(self.env.cr, self.env.uid, 'account.siamm.idsiamm')

        for invoice in self:
            if not invoice.siamm_intercettazioni:
                raise except_orm(_('Error!'),
                                 _('File SIAMM generabile solo su fatture intercettazioni'))
            dict_siamm = self._generate_siamm(invoice,id_siamm)
            siamm_list_intercettazioni.append(dict_siamm)
            if add_to:
                filename = 'FEPA_SIAMM_' + id_file_siamm.replace('/','-')+ '.xml'

                try:
                    datas = base64.encodestring(siamm.serialize(dict_siamm))
                except ValueError as ve:
                    raise except_orm(_('Error!'),
                                     _('Errore nella validazione: ' + str(ve)))

                attachment = self.env['ir.attachment'].create({'name': filename,
                                                               'datas_fname': filename,
                                                               'datas': datas,
                                                               'mimetype': 'application/xml',
                                                               'res_model': 'account.invoice',
                                                               'res_id': self.id
                                                               })
            id_siamm += 1
        try:
            return siamm.serialize(siamm_list_intercettazioni)
        except ValueError as ve:
            raise except_orm(_('Error!'),
                             _('Errore nella validazione: ' + str(ve)))

    def dati_generali_documento_from_odoo(self):

        dgd = super(siamm_account_invoice,self).dati_generali_documento_from_odoo()

        decode_registro = None
        if self.siamm_registro:
            for registro in RG:
                if registro[0] == self.siamm_registro:
                    decode_registro = registro[1]

        siamm_causale = ''
        if self.siamm_nomemagistrato:
            siamm_causale += 'PM: {0} {1} - '.format(self.siamm_nomemagistrato, self.siamm_cognomemagistrato)
        if self.siamm_nrrg:
            siamm_causale += 'N.R.R.G.: {} - '.format(self.siamm_nrrg)
        if decode_registro:
            siamm_causale += '{} - '.format(decode_registro)
        if self.inter_nrvg:
            siamm_causale += 'N.R.V.G.: {} - '.format(self.inter_nrvg)
        if self.siamm_numeromodello37:
            siamm_causale += 'Modello37 n.ro : {} - '.format(self.siamm_numeromodello37)
        if self.siamm_datainizioprestazione and self.siamm_datafineprestazione:
            siamm_causale += 'Servizio dal {0} al {1}'.format(self.siamm_datainizioprestazione,
                                                              self.siamm_datafineprestazione)
        if siamm_causale:
            dgd.Causale = dgd.Causale.append(siamm_causale) if dgd.Causale else [siamm_causale]

        return dgd

