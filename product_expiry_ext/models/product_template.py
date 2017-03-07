# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import models, fields, api, exceptions, _
import logging
_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

   
    @api.multi
    def action_production_lot_list(self):
        self.ensure_one()
        
        action = self.env.ref('stock.action_production_lot_form')
        result = action.read()[0]
     
        result['domain'] = [('product_id', 'in', [v.id for v in self.product_variant_ids] )]
        return result

    @api.multi
    def _get_closest_date(self):
        now = fields.Datetime.now()
        for prod in self:     
            available_lots = []
            for lot in prod.lot_ids :
                stock = prod.with_context(
                    lot_id=lot.id,
                    )._product_available(name=None, arg=False)        
                if stock[prod.id]['qty_available'] > 0.0 : available_lots.append(lot)
            dates = filter(lambda x: x.life_date >= now, [l for l in available_lots])
            if len(dates) ==0 :
                continue
            sort_dates = list([d.life_date for d in dates])
            sort_dates.sort()
            prod.closest_expiry_date = sort_dates[0]

    @api.multi
    def _get_lot_ids(self):
        lots = self.env['stock.production.lot']
        for prod in self:
            var_ids = [v.id for v in prod.product_variant_ids]
            prod.lot_ids = lots.search([('product_id', 'in', var_ids)])
            

    closest_expiry_date = fields.Date(compute=_get_closest_date,
        string='Expiry closest date')
        
    lot_ids = fields.One2many(comodel_name="stock.production.lot",
                                compute=_get_lot_ids)


class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    @api.multi
    def action_production_lot_list(self):
        self.ensure_one()
        
        action = self.env.ref('stock.action_production_lot_form')
        result = action.read()[0]
     
        result['domain'] = [('product_id', 'in', [v.id for v in self] )]
        return result
    
    
    @api.multi
    def _get_closest_date(self):
        now = fields.Datetime.now()
        for prod in self:            
            available_lots = []
            for lot in prod.lot_ids :
                stock = prod.with_context(
                    lot_id=lot.id,
                    )._product_available(field_names=None, arg=False)        
                if stock[prod.id]['qty_available'] > 0.0 : available_lots.append(lot)
            dates = filter(lambda x: x.life_date >= now, [l for l in available_lots])
            if len(dates) ==0 :
                continue
            sort_dates = list([d.life_date for d in dates])
            sort_dates.sort()
            prod.closest_expiry_date = sort_dates[0]
            

    @api.multi
    def _get_lot_ids(self):
        lots = self.env['stock.production.lot']
        for prod in self:
            var_ids = [v.id for v in prod.product_variant_ids]
            prod.lot_ids = lots.search([('product_id', 'in', var_ids)])
            

    closest_expiry_date = fields.Date(compute=_get_closest_date,
        string='Expiry closest date')
        
    lot_ids = fields.One2many(comodel_name="stock.production.lot",
                                inverse_name="product_id")