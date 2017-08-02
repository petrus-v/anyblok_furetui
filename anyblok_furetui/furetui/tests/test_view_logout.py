# This file is a part of the AnyBlok / FuretUI project
#
#    Copyright (C) 2017 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from anyblok_pyramid.tests.testcase import PyramidBlokTestCase
from pyramid.response import Response


def update_session_connection(request):
    state = request.matchdict['state']
    request.session['state'] = state
    request.session.save()
    return Response('ok')


def get_connection_state(request):
    return Response(request.session['state'])


class TestViewLogout(PyramidBlokTestCase):

    def connection_state(self, config):
        config.add_route('test_connection_state', '/test/connection/{state}')
        config.add_view(
            update_session_connection, route_name='test_connection_state')
        config.add_route('test_connection', '/test/connection')
        config.add_view(get_connection_state, route_name='test_connection')

    def setUp(self):
        super(TestViewLogout, self).setUp()
        self.includemes.append(self.connection_state)

    def test_logout_when_disconnected(self):
        webserver = self.webserver
        resp = webserver.get('/test/connection/disconnected')
        resp = webserver.get('/test/connection')
        self.assertEqual(resp.body.decode('utf8'), 'disconnected')
        resp = webserver.post_json('/furetui/client/logout', {})
        self.assertEqual(resp.status, '200 OK')
        self.assertEqual(
            resp.json,
            [
                {
                    "type": "UPDATE_ROUTE",
                    "name": "homepage"
                },
                {
                    "type": "RELOAD"
                },
            ]
        )
        resp = webserver.get('/test/connection')
        self.assertEqual(resp.body.decode('utf8'), 'disconnected')

    def test_logout_when_connected(self):
        webserver = self.webserver
        webserver.get('/test/connection/connected')
        resp = webserver.get('/test/connection')
        self.assertEqual(resp.body.decode('utf8'), 'connected')
        resp = webserver.post_json('/furetui/client/logout', {})
        self.assertEqual(resp.status, '200 OK')
        self.assertEqual(
            resp.json,
            [
                {
                    "type": "UPDATE_ROUTE",
                    "name": "homepage"
                },
                {
                    "type": "RELOAD"
                },
            ]
        )
        resp = webserver.get('/test/connection')
        self.assertEqual(resp.body.decode('utf8'), 'disconnected')

    def test_custom_view_logout(self):
        webserver = self.webserver
        resp = webserver.post_json('/furetui/custom/view/Logout', {})
        self.assertEqual(resp.status, '200 OK')
        self.assertEqual(resp.json, [])