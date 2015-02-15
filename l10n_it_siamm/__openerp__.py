# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 KTec S.r.l.
#    (<http://www.ktec.it>).
#
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
    'name': 'SIAMM (Itercettazioni)',
    'version': '1.0',
    'category': 'Localisation/Italy',
    'description': """
Italian Localisation module - SIAMM - Intercettazioni
=====================================================

This module adds SIAMM (Itercettazioni) field to invoive and the ability to create
SIAMM complaint XML file  to be used at https://lsg.giustizia.it

Funcionalities
--------------
    * Fields
    * SIAMM XML Generation
""",
    'author': 'KTec S.r.l.',
    'website': 'http://www.ktec.it',
    'license': 'AGPL-3',
    "depends": ['account'],
    "data": [
        'view/invoice_view.xml',
        'wizard/generate_siammxml_view.xml'
    ],
    "qweb": [],
    "demo": [],
    "test": [],
    "active": False,
    'installable': True
}
