from odoo import api, fields, models



class finish_subscription(models.TransientModel):
    _name = 'finish.subscription'
    _description = 'Wizard finish member subscription'
    
    
    user_id = fields.Many2one(comodel_name='res.users', ondelete='restrict')
    reason = fields.Char(required=True)
    

    def unsubscribe(self):
        #self.env._context
        user_object = (self.env['res.partner'].browse(self.env.context.get('active_id')))
        
        # write the reason
        
        
        # untick the member
        user_object.write({'library_member': False})
        
        # put the reason in the chatter
        output = f"User unsubscribed from the library, reason: {self.reason}"
        user_object.message_post(body=output)
        