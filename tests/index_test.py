from libs.testing import ApiTest

class IndexTest(ApiTest):
    def test_key_test(self):
        jd = self._d(self._app.reverse_url('index'))
        self.assertEquals(jd.get('response_code'), self._httplib.OK)

