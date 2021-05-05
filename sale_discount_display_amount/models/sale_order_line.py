# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    discount_total = fields.Monetary(
        compute="_compute_amount", string="Discount Subtotal", store=True
    )
    price_total_no_discount = fields.Monetary(
        compute="_compute_amount", string="Subtotal Without Discount", store=True
    )

    def _update_discount_display_fields(self):
        for line in self:
            line.price_total_no_discount = 0
            line.discount_total = 0
            if not line.discount:
                line.price_total_no_discount = line.price_subtotal
                continue

            price_total_no_discount = line.price_unit * line.product_uom_qty
            discount_total = price_total_no_discount - line.price_subtotal

            line.update(
                {
                    "discount_total": discount_total,
                    "price_total_no_discount": price_total_no_discount,
                }
            )

    @api.depends("product_uom_qty", "discount", "price_unit", "tax_id")
    def _compute_amount(self):
        res = super(SaleOrderLine, self)._compute_amount()
        self._update_discount_display_fields()
        return res
