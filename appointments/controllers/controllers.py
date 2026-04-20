# from odoo import http


# class TimeSlots(http.Controller):
#     @http.route('/time_slots/time_slots', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/time_slots/time_slots/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('time_slots.listing', {
#             'root': '/time_slots/time_slots',
#             'objects': http.request.env['time_slots.time_slots'].search([]),
#         })

#     @http.route('/time_slots/time_slots/objects/<model("time_slots.time_slots"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('time_slots.object', {
#             'object': obj
#         })
