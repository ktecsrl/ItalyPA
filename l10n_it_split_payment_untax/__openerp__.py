# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 KTec S.r.l.
#    (<http://www.ktec.it>).
#
#    Copyright (C) 2014 Associazione Odoo Italia
#    (<http://www.openerp-italia.org>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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
{
    'name': 'Split Payment Untax',
    'version': '8.0.1.0',
    'category': 'Localisation/Italy',
    'description': """
Italian Localisation module - Split Payment
============================================

This module extend l10n_it_split_payment

Funcionalities
--------------
    * TAG fiscal position for use only untax amount on net to pay
""",
    'author': 'KTec S.r.l.',
    'website': 'http://www.ktec.it',
    'license': 'AGPL-3',
    "depends": ['l10n_it_split_payment'],
    "data": [
        'view/sp_fiscal_position_view.xml',
    ],
    "qweb": [],
    "demo": [],
    "test": [],
    "active": False,
    'installable': True
}