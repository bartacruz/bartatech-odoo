import { Message } from "@mail/core/common/message";
import { patch } from "@web/core/utils/patch";

patch(Message.prototype, {
  /**
   * Abrir nuestro Wizard al hacer clic
   */
  onClickReplyEmail() {
    this.env.services.action.doAction({
      type: "ir.actions.act_window",
      res_model: "mail.reply.wizard",
      views: [[false, "form"]],
      target: "new",
      context: {
        default_message_id: this.message.id,
        active_id: this.message.id,
      },
    });
  },
});
