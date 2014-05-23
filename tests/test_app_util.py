import unittest

import mock
from rhsm import certificate

from crane import app_util
from crane import exceptions
import demo_data

from .views import base


@app_util.authorize_repo_id
def mock_repo_func(repo_id):
    return 'foo'


@app_util.authorize_image_id
def mock_image_func(image_id, repo_info):
    return 'foo'


class FlaskContextBase(base.BaseCraneAPITest):

    def setUp(self):
        super(FlaskContextBase, self).setUp()
        self.ctx = self.app.test_request_context('/')
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()
        super(FlaskContextBase, self).tearDown()


class TestAuthorizeRepoId(FlaskContextBase):

    def test_raises_not_found_if_repo_id_none(self):
        self.assertRaises(exceptions.NotFoundException, mock_repo_func, None)

    def test_raises_not_found_if_repo_id_invalid(self):
        self.assertRaises(exceptions.NotFoundException, mock_repo_func, 'bad_id')

    @mock.patch('crane.app_util._get_certificate')
    def test_raises_auth_error_if_id_invalid(self, mock_get_cert):
        cert = certificate.create_from_file(demo_data.demo_entitlement_cert_path)
        mock_get_cert.return_value = cert
        self.assertRaises(exceptions.AuthorizationFailed, mock_repo_func, 'qux')

    @mock.patch('crane.app_util._get_certificate')
    def test_passes_if_auth_valid(self, mock_get_cert):
        cert = certificate.create_from_file(demo_data.demo_entitlement_cert_path)
        mock_get_cert.return_value = cert
        result = mock_repo_func('baz')
        self.assertEquals(result, 'foo')

    @mock.patch('crane.app_util._get_certificate')
    def test_bypass_if_not_protected(self, mock_get_cert):
        cert = certificate.create_from_file(demo_data.demo_entitlement_cert_path)
        mock_get_cert.return_value = cert
        result = mock_repo_func('redhat/foo')
        self.assertEquals(result, 'foo')


class TestAuthorizeImageId(FlaskContextBase):

    def test_raises_not_found_if_image_id_none(self):
        self.assertRaises(exceptions.NotFoundException, mock_image_func, None)

    def test_raises_not_found_if_image_id_invalid(self):
        self.assertRaises(exceptions.NotFoundException, mock_image_func, 'invalid')

    @mock.patch('crane.app_util._get_certificate')
    def test_raises_auth_error_if_id_invalid(self, mock_get_cert):
        cert = certificate.create_from_file(demo_data.demo_entitlement_cert_path)
        mock_get_cert.return_value = cert
        self.assertRaises(exceptions.AuthorizationFailed, mock_image_func, 'qux123')

    @mock.patch('crane.app_util._get_certificate')
    def test_passes_if_auth_valid(self, mock_get_cert):
        cert = certificate.create_from_file(demo_data.demo_entitlement_cert_path)
        mock_get_cert.return_value = cert
        result = mock_image_func('baz123')
        self.assertEquals(result, 'foo')

    @mock.patch('crane.app_util._get_certificate')
    def test_bypass_if_not_protected(self, mock_get_cert):
        cert = certificate.create_from_file(demo_data.demo_entitlement_cert_path)
        mock_get_cert.return_value = cert
        result = mock_image_func('xyz789')
        self.assertEquals(result, 'foo')


class TestHandlers(unittest.TestCase):

    def test_auth_handler(self):
        string_value, http_code = app_util.error_handler_auth_error(
            exceptions.AuthorizationFailed('Foo Error'))
        self.assertEquals(string_value, 'Foo Error')
        self.assertEquals(http_code, 403)

    def test_not_found_handler(self):
        string_value, http_code = app_util.error_handler_not_found(
            exceptions.NotFoundException('Foo Error'))
        self.assertEquals(string_value, 'Foo Error')
        self.assertEquals(http_code, 404)
