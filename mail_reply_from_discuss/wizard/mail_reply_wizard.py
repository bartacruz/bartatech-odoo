from odoo import models, fields, api


class MailReplyWizard(models.TransientModel):
    _name = "mail.reply.wizard"
    _description = "Wizard to reply incomming mails"

    message_id = fields.Many2one("mail.message", string="Original message")
    email_to = fields.Char(string="To", required=True)
    subject = fields.Char(required=True)
    body = fields.Html(required=True)
    mail_server_id = fields.Many2one("ir.mail_server", string="Send from")

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        msg_id = self.env.context.get("default_message_id")
        if msg_id:
            msg = self.env["mail.message"].browse(msg_id)
            res.update(
                {
                    "message_id": msg.id,
                    "email_to": msg.email_from,
                    "subject": "Re: " + (msg.subject or ""),
                }
            )
        return res

    def send_reply(self):
        mail_values = {
            "subject": self.subject,
            "body_html": self.body,
            "email_to": self.email_to,
            "email_from": self.mail_server_id.smtp_user,
            "mail_server_id": self.mail_server_id.id,
            "auto_delete": True,
        }
        # print("send", mail_values)
        self.env["mail.mail"].create(mail_values).send()
