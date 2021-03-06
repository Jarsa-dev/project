# -*- coding: utf-8 -*-
{
    "name": """Gantt view from odoo 8""",
    "summary": """Ported view from odoo 8""",
    "category": "Hidden",
    "images": [],
    "version": "9.0.1.0.0",
    "author": "IT-Projects LLC, Pavel Romanchenko, "
    "Odoo Community Association (OCA)",
    "website": "https://it-projects.info",
    "license": "AGPL-3",
    "depends": [
        "web",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        'views/web_gantt.xml',
        # 'static/src/xml/css.xml',
    ],
    "qweb": [
        'static/src/xml/*.xml',
    ],
    "demo": [],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "installable": True,
    "auto_install": False,
    "application": False,
}
