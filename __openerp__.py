# -*- coding: utf-8 -*-

{
    "name": "Cambio massivo codice IVA ",
    "version": "1.01",
    "depends": ["product", "account"],
    "author": "C & G Software S.a.s.",
    "category": "Product",
    "description": """Cambio massivo codice IVA sugli articoli e nelle definizioni di base
    """,
    "init_xml": [],
    'update_xml': [
                   'view_cambio_iva.xml',
                   'security/ir.model.access.csv',
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}
