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

from PyFePA.fepa import *
from PyFePA.serializer import serializer, ValidateException
from PyFePA import siamm
from openerp import models, api, _
from openerp.exceptions import except_orm
import base64
import datetime

class OdooFatturaPA(models.Model):

    _inherit = 'account.invoice'

    @api.multi
    def invoice_validate(self):

        if self.partner_id.ipa_code:
            try:
                self.crea_fatturapa()
            except (ValidateException, ValueError) as ve:
                raise except_orm(_('Error!'),
                                 _('Errore nella validazione: ' + str(ve)))
        #super call
        return super(OdooFatturaPA,self).invoice_validate()

    @api.multi
    def crea_fatturapa(self):

        if hasattr(self,'siamm_intercettazioni') and self.number and self.siamm_intercettazioni:
            self.generate_siamm_xml()

        fpa = self.fatturapa_from_odoo()
        xmlpa_b64 = base64.encodestring(serializer(fpa,'xml'))
        filename = '{0}{1}_{2}.xml'.format(fpa.FatturaElettronicaHeader.DatiTrasmissione.IdTrasmittente.IdPaese,
                                           fpa.FatturaElettronicaHeader.DatiTrasmissione.IdTrasmittente.IdCodice,
                                           fpa.FatturaElettronicaHeader.DatiTrasmissione.ProgressivoInvio)
        attachment = self.env['ir.attachment'].create({'name': filename,
                                                       'datas_fname': filename,
                                                       'datas': xmlpa_b64,
                                                       'res_model': 'account.invoice',
                                                       'res_id': self.id
                                                       })

    def fatturapa_from_odoo(self):

        fatturapa = FatturaElettronica()
        fatturapa.FatturaElettronicaHeader = self.header_from_odoo()
        fatturapa.FatturaElettronicaBody = self.body_from_odoo()

        return fatturapa

    def header_from_odoo(self):

        header = FatturaElettronicaHeader()
        header.DatiTrasmissione = self.trasmissione_from_odoo()
        header.CedentePrestatore = self.cedenteprestatore_from_odoo()
        header.CessionarioCommittente = self.cessionariocommittente_from_odoo()
        #header.TerzoIntermediarioOSoggettoEmittente = self.terzointermediario_from_odoo()
        #header.SoggettoEmittente = None

        return header

    def body_from_odoo(self):

        lbody = []
        body = FatturaElettronicaBody()
        body.DatiGenerali = self.datigenerali_from_odoo()
        body.DatiBeniServizi = self.datibeniservizi_from_odoo()
        body.DatiPagamento = self.datipagamento_from_odoo()
        body.Allegati = self.allegati_from_odoo()
        lbody.append(body)

        return lbody

    def trasmissione_from_odoo(self):

        dt = DatiTrasmissione()
        dt.IdTrasmittente = IdTrasmittente()

        company = self.company_id

        if not company:
            user_obj = self.pool['res.users']
            company = user_obj.company_id

        dt.IdTrasmittente.IdPaese = company.vat[0:2] if company.vat else None
        dt.IdTrasmittente.IdCodice = company.vat[2:] if company.vat else None
        dt.ProgressivoInvio = 123456
        dt.CodiceDestinatario = self.partner_id.ipa_code if self.partner_id.ipa_code else None

        if company.phone or company.email:
            dt.ContattiTrasmittente = ContattiTrasmittente()
            dt.ContattiTrasmittente.Email = company.email if company.email else None
            dt.ContattiTrasmittente.Telefono = company.phone if company.phone else None

        return dt

    def cedenteprestatore_from_odoo(self):

        company = self.company_id

        if not company:
            user_obj = self.pool['res.users']
            company = user_obj.company_id

        cp = CedentePrestatore()
        cp.DatiAnagrafici = DatiAnagraficiCP()
        cp.DatiAnagrafici.IdFiscaleIVA = IdFiscaleIVA()
        cp.DatiAnagrafici.IdFiscaleIVA.IdPaese = company.vat[0:2] if company.vat else None
        cp.DatiAnagrafici.IdFiscaleIVA.IdCodice = company.vat[2:] if company.vat else None
        #cp.DatiAnagrafici.CodiceFiscale = None
        cp.DatiAnagrafici.Anagrafica = Anagrafica()
        cp.DatiAnagrafici.Anagrafica.Denominazione = company.name if company.name else None
        #cp.DatiAnagrafici.Anagrafica.Nome = None
        #cp.DatiAnagrafici.Anagrafica.Cognome = None
        #cp.DatiAnagrafici.Anagrafica.Titolo = None
        #cp.DatiAnagrafici.Anagrafica.CodEORI = None
        cp.DatiAnagrafici.RegimeFiscale = company.regime_fiscale if company.regime_fiscale else None
        cp.Sede = Sede()
        if company.street and company.street2:
            cp.Sede.Indirizzo = company.street + company.street2
        else:
            cp.Sede.Indirizzo = company.street if company.street else None
        #cp.Sede.NumeroCivico = None
        cp.Sede.CAP = company.zip if company.zip else None
        cp.Sede.Comune = company.city if company.city else None
        cp.Sede.Provincia = company.state_id.code if company.state_id.code else None
        cp.Sede.Nazione = company.country_id.code if company.country_id.code else None
        cp.IscrizioneREA = IscrizioneREA()
        cp.IscrizioneREA.Ufficio = company.company_registry[0:2] if company.company_registry else None
        cp.IscrizioneREA.NumeroREA = company.company_registry[2:] if company.company_registry else None
        cp.IscrizioneREA.CapitaleSociale = company.capitale_sociale if company.capitale_sociale else None
        cp.IscrizioneREA.SocioUnico = 'SU' if company.socio_unico else 'SM'
        cp.IscrizioneREA.StatoLiquidazione = 'LS' if company.stato_liquidazione else 'LN'
        cp.Contatti = Contatti()
        cp.Contatti.Telefono = company.phone if company.phone else None
        cp.Contatti.Email = company.email if company.email else None
        cp.Contatti.Fax = company.fax if company.fax else None

        return cp

    def cessionariocommittente_from_odoo(self):

        cc = CessionarioCommittente()
        cc.DatiAnagrafici = DatiAnagraficiCC()
        #cc.DatiAnagrafici.IdFiscaleIVA = IdFiscaleIVA()
        #cc.DatiAnagrafici.IdFiscaleIVA.IdPaese = None
        #cc.DatiAnagrafici.IdFiscaleIVA.IdCodice = None
        cc.DatiAnagrafici.CodiceFiscale = self.partner_id.fiscalcode if self.partner_id.fiscalcode else None
        cc.DatiAnagrafici.Anagrafica = Anagrafica()
        cc.DatiAnagrafici.Anagrafica.Denominazione = self.partner_id.name if self.partner_id.name else None
        #cc.DatiAnagrafici.Anagrafica.Nome = None
        #cc.DatiAnagrafici.Anagrafica.Cognome = None
        #cc.DatiAnagrafici.Anagrafica.Titolo = None
        #cc.DatiAnagrafici.Anagrafica.CodEORI = None
        cc.Sede = Sede()
        cc.Sede.Indirizzo = self.partner_id.street if self.partner_id.street else None
        #cc.Sede.NumeroCivico = None
        cc.Sede.CAP = self.partner_id.zip if self.partner_id.zip else None
        cc.Sede.Comune = self.partner_id.city if self.partner_id.city else None
        #cc.Sede.Provincia = None
        cc.Sede.Nazione = self.partner_id.country_id.code if self.partner_id.country_id.code else None

        return cc

    def terzointermediario_from_odoo(self):

        tz = TerzoIntermediarioOSoggettoEmittente()
        tz.DatiAnagrafici = DatiAnagraficiCC()
        tz.DatiAnagrafici.IdFiscaleIVA = IdFiscaleIVA()
        tz.DatiAnagrafici.IdFiscaleIVA.IdPaese = None
        tz.DatiAnagrafici.IdFiscaleIVA.IdCodice = None
        tz.DatiAnagrafici.CodiceFiscale = None
        tz.DatiAnagrafici.Anagrafica = Anagrafica()
        tz.DatiAnagrafici.Anagrafica.Denominazione = None
        tz.DatiAnagrafici.Anagrafica.Nome = None
        tz.DatiAnagrafici.Anagrafica.Cognome = None
        tz.DatiAnagrafici.Anagrafica.Titolo = None
        tz.DatiAnagrafici.Anagrafica.CodEORI = None

        return tz

    def datigenerali_from_odoo(self):

        dg = DatiGenerali()
        dg.DatiGeneraliDocumento = DatiGeneraliDocumento()
        dg.DatiGeneraliDocumento.TipoDocumento = 'TD01'
        dg.DatiGeneraliDocumento.Divisa = self.currency_id.name if self.currency_id.name else None
        dg.DatiGeneraliDocumento.Data = self.date_invoice if self.date_invoice else None
        dg.DatiGeneraliDocumento.Numero = self.number if self.number else None
        #dg.DatiGeneraliDocumento.ScontoMaggiorazione = ScontoMaggiorazione()
        #dg.DatiGeneraliDocumento.ScontoMaggiorazione.Tipo = None
        #dg.DatiGeneraliDocumento.ScontoMaggiorazione.Percentuale = None
        #dg.DatiGeneraliDocumento.ScontoMaggiorazione.Importo = None
        dg.DatiGeneraliDocumento.ImportoTotaleDocumento = self.amount_total if self.amount_total else None
        #dg.DatiGeneraliDocumento.Arrotondamento = None
        if hasattr(self, 'siamm_intercettazioni') and self.siamm_intercettazioni:
            dg.DatiGeneraliDocumento.Causale = 'PM: {0} {1} - NR-RG: {2} - Servizio dal {3} al {4} - {5}'.format(
                self.siamm_nomemagistrato,
                self.siamm_cognomemagistrato,
                self.siamm_nrrg if self.siamm_nrrg else None,
                self.siamm_datainizioprestazione,
                self.siamm_datafineprestazione,
                self.comment if self.comment else None
            )
        else:
            dg.DatiGeneraliDocumento.Causale = self.comment if self.comment else None

        return dg

    def datibeniservizi_from_odoo(self):

        dbs = DatiBeniServizi()

        linee = []

        linea_nu = 1

        for line in self.invoice_line:

            dtl = DettaglioLinee()
            dtl.NumeroLinea = linea_nu
            if line.product_id.code:
                dtl.CodiceArticolo = CodiceArticolo()
                dtl.CodiceArticolo.CodiceTipo = 'INTERNO'
                dtl.CodiceArticolo.CodiceValore = line.product_id.code if line.product_id.code else None
            dtl.Descrizione = line.name
            dtl.Quantita = line.quantity if line.quantity else None
            dtl.UnitaMisura = line.uos_id.name if line.uos_id.name else None
            dtl.PrezzoUnitario = line.price_unit if line.price_unit else None

            if line.discount:
                dtl.ScontoMaggiorazione = ScontoMaggiorazione()
                dtl.ScontoMaggiorazione.Tipo = 'SC'
                dtl.ScontoMaggiorazione.Percentuale = line.discount

            dtl.PrezzoTotale = line.price_subtotal if line.product_id else None
            #To-Do: Tasse multiple sulla stessa linea vedere come risolvere eventuale errore
            dtl.AliquotaIVA = line.invoice_line_tax_id[0].amount*100
            linea_nu += 1
            linee.append(dtl)

        dbs.DettaglioLinee = linee

        dr = []
        for tl in self.tax_line:
            drt = DatiRiepilogo()

            #To-Do: esiste un modo migliore?
            amount = self.env['account.tax'].search([('tax_code_id', '=', tl.tax_code_id.id)])[0].amount
            drt.AliquotaIVA = amount*100

            drt.ImponibileImporto = tl.base if tl.base else None
            drt.Imposta = tl.amount if tl.amount else None
            #To-Do: sistemare esigibilita iva
            drt.EsigibilitaIVA = 'S'
            drt.RiferimentoNormativo = 'Scissione nei pagamenti, IVA versata dal committente art 17 ter  D.P.R. n.633/ 72'
            dr.append(drt)

        dbs.DatiRiepilogo = dr

        return dbs

    def datipagamento_from_odoo(self):

        company = self.company_id
        dp = None

        if not company:
            user_obj = self.pool['res.users']
            company = user_obj.company_id

        bank = self.partner_bank_id

        if not bank:
            bank = company.bank_ids[0] if company.bank_ids else None

        if bank:
            dp = DatiPagamento()
            #to-do: implementare esterno
            dp.CondizioniPagamento = 'TP02'
            dp.DettaglioPagamento = DettaglioPagamento()
            dp.DettaglioPagamento.ModalitaPagamento = 'MP05'
            dp.DettaglioPagamento.ImportoPagamento = self.amount_total if self.amount_total else None
            dp.DettaglioPagamento.IBAN = bank.iban.replace(' ', '') if bank.iban else None
            dp.DettaglioPagamento.BIC = bank.bank_bic if bank.bank_bic else None

        return dp

    def allegati_from_odoo(self):

        attachments = self.env['ir.attachment'].search([('res_model', '=', 'account.invoice'),
                                                        ('res_id', '=', self.id)])
        allegati = []

        for f in attachments:
            if f.datas_fname[0:5] == 'FEPA_':
                print f.datas_fname[0:5]
                all = Allegati()
                all.NomeAttachment = f.datas_fname if f.datas_fname else None
                #all.FormatoAttachment = f.mimetype if f.mimetype else None
                all.DescrizioneAttachment = f.description if f.description else None
                all.Attachment = f.datas
                allegati.append(all)

        if len(allegati) > 0:
            return allegati
        else:
            return None

    @api.one
    def generate_siamm_xml(self):

        if not hasattr(self,'siamm_intercettazioni') or not self.number or not self.siamm_intercettazioni:
            raise except_orm(_('Error!'),
                             _('File SIAMM generabile solo su fatture intercettazioni confermate'))

        company = self.company_id

        if not company:
            user_obj = self.pool['res.users']
            company = user_obj.company_id

        siamm_data = {'beneficiario': company.vat,
                      'tipopagamento': 'AC',
                      'id': 1,
                      'entepagante': self.siamm_entepagante if self.siamm_entepagante else None,
                      'numerofattura': self.number,
                      'registro': self.siamm_registro if self.siamm_registro else '',
                      'datafattura': datetime.datetime.strptime(self.date_invoice, '%Y-%m-%d'),
                      'importototale': self.amount_untaxed,
                      'importoiva': self.amount_tax,
                      'nr_rg': self.siamm_nrrg if self.siamm_registro else '',
                      'sede': self.siamm_sede if self.siamm_sede else '',
                      'numeromodello37': self.siamm_numeromodello37 if self.siamm_numeromodello37 else '',
                      'datainizioprestazione': datetime.datetime.strptime(self.siamm_datainizioprestazione,
                                                                          '%Y-%m-%d') if self.siamm_datainizioprestazione else '',
                      'datafineprestazione': datetime.datetime.strptime(self.siamm_datafineprestazione,
                                                                        '%Y-%m-%d') if self.siamm_datafineprestazione else '',
                      'nomemagistrato': self.siamm_cognomemagistrato if self.siamm_cognomemagistrato else None,
                      'cognomemagistrato': self.siamm_nomemagistrato if self.siamm_nomemagistrato else None,
                      'tipointercettazione': self.siamm_tipointercettazione if self.siamm_tipointercettazione else None}

        filename = 'FEPA_SIAMM_' + self.number.replace('/','-')+ '.xml'


        try:
            datas = base64.encodestring(siamm.serialize(siamm_data))
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