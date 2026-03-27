from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    firstname = fields.Char(string="Prénom")
