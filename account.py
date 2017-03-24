from openerp.osv import fields,osv
from openerp import tools

 
class account_invoice(osv.osv):
    _name = "account.state.report"
    _description = "State Report"
    _auto = False
    _columns = {
	'company_id': fields.many2one('account.journal','Journal Name'),
	'period_id': fields.many2one('account.journal','Journal Name'),
	'journal_id': fields.many2one('account.journal','Journal Name'),
	'state_id': fields.many2one('res.country.state','State'),
	'base_amount': fields.float('Base Amount',readonly=True,group_operator="sum",digits=(16,2)),
	'amount_total': fields.float('Total Amount',readonly=True,group_operator="sum",digits=(16,2)),
	}
 
    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'account_state_report')
	cr.execute("""
		create or replace view account_tax_vat_report as (
				select a.company_id as company_id,a.period_id as period_id,a.journal_id as journal_id,b.state_id as state_id,sum(a.amount_total) as amount_total, 
					sum(a.amount_untaxed) as amount_untaxed 
					from account_invoice a inner join res_partner b on a.partner_id = b.id 
					where a.state in ('open','paid') and a.type in ('out_invoice','out_refund') 
					group by 1,2,3,4
				)
	""")	
 
account_invoice()

