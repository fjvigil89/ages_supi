# -*- coding: utf-8 -*-
# from odoo import http


# class SupiIntegration(http.Controller):
#     @http.route('/supi_integration/supi_integration/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/supi_integration/supi_integration/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('supi_integration.listing', {
#             'root': '/supi_integration/supi_integration',
#             'objects': http.request.env['supi_integration.supi_integration'].search([]),
#         })

#     @http.route('/supi_integration/supi_integration/objects/<model("supi_integration.supi_integration"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('supi_integration.object', {
#             'object': obj
#         })
