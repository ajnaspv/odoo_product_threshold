from odoo import api, fields, models,Command

class ResPartner(models.Model):
    _inherit = "res.partner"

    product_ids = fields.Many2many('product.product', string="Products")
    threshold = fields.Float(string="Threshold", readonly=True)

    def action_recalculate_btn(self):
        """ Action for recalculate button
        using threshold, sale.report
        return products meet the threshold frequency
        """
        self.threshold = self.env['ir.config_parameter'].sudo().get_float('product_threshold.threshold')
        sale_orders = self.env['sale.report'].search([('partner_id', 'in', self.id)])
        self.write({'product_ids': [Command.clear()]})
        for rec in sale_orders:
            if rec.product_uom_qty >= self.threshold:
                self.write({'product_ids': [Command.link(rec.product_id.id)]})

    def action_add_so_btn(self):
        """ Action for add sale order button
        adding threshold met products to sale order """
        order_lines = []
        for rec in self.product_ids:
            order_lines.append({
                'product_id': rec.id,
                'product_uom_qty': self.threshold,
                'tax_ids': False
            })
        sale_order = self.env["sale.order"].create({
            "partner_id": self.id,
            "partner_invoice_id": self.id,
            "partner_shipping_id": self.id,
            "order_line": [Command.create(vals) for vals in order_lines]
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': sale_order.id,
            'target': 'current',
        }