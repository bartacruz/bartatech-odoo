# from odoo import http


# class TestDelegate(http.Controller):
#     @http.route('/test_delegate/test_delegate', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/test_delegate/test_delegate/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('test_delegate.listing', {
#             'root': '/test_delegate/test_delegate',
#             'objects': http.request.env['test_delegate.test_delegate'].search([]),
#         })

#     @http.route('/test_delegate/test_delegate/objects/<model("test_delegate.test_delegate"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('test_delegate.object', {
#             'object': obj
#         })
