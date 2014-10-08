import unittest
import datetime
import pymongo
import json

from pyramid import testing
from pyramid import httpexceptions


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.collection = pymongo.Connection('mongodb://localhost/')['test_scielo_network']['accesses']

    def tearDown(self):
        testing.tearDown()
        self.collection.remove()

    def test_index(self):
        from ratchet.views import index
        request = testing.DummyRequest()

        response = index(request)

        self.assertEqual(response.text, 'Ratchet API')

    def test_endpoints(self):
        from ratchet.views import endpoints
        request = testing.DummyRequest()
        response = endpoints(request)

        self.assertEqual(response['articles']['list_endpoint'], '/api/v1/articles/')
        self.assertEqual(response['journals']['list_endpoint'], '/api/v1/journals/')
        self.assertEqual(response['issues']['list_endpoint'], '/api/v1/issues/')
        self.assertEqual(response['general']['list_endpoint'], '/api/v1/general/')


    def test_articles(self):
        from ratchet.views import articles, general_post

        post_data = {'code': 'S0104-77602014000100002', 'page': 'html', 'type': 'article', 'access_date': '2014-12-25'}

        request = testing.DummyRequest(post=post_data, db=self.collection)

        try:
            general_post(request)
        except:
            pass

        post_data = {'code': 'S0100-07602014000100002', 'page': 'abstract', 'type': 'article', 'access_date': '2014-12-25'}

        request = testing.DummyRequest(post=post_data, db=self.collection)

        try:
            general_post(request)
        except:
            pass

        request = testing.DummyRequest(db=self.collection)

        response = articles(request)        

        self.assertEqual(len(response['objects']), 2)

    def test_articles_offset_exceeded_lt(self):
        from ratchet.views import articles, general_post

        post_data = {'code': 'S0104-77602014000100002', 'page': 'html', 'type': 'article', 'access_date': '2014-12-25'}

        request = testing.DummyRequest(post=post_data, db=self.collection)

        try:
            general_post(request)
        except:
            pass

        post_data = {'code': 'S0100-07602014000100002', 'page': 'abstract', 'type': 'article', 'access_date': '2014-12-25'}

        request = testing.DummyRequest(post=post_data, db=self.collection)

        try:
            general_post(request)
        except:
            pass

        request = testing.DummyRequest(params={'offset': -1}, db=self.collection)
    
        with self.assertRaises(httpexceptions.HTTPBadRequest):
            response = articles(request)        

    def test_articles_offset_exceeded_gt(self):
        from ratchet.views import articles, general_post

        post_data = {'code': 'S0104-77602014000100002', 'page': 'html', 'type': 'article', 'access_date': '2014-12-25'}

        request = testing.DummyRequest(post=post_data, db=self.collection)

        try:
            general_post(request)
        except:
            pass

        post_data = {'code': 'S0100-07602014000100002', 'page': 'abstract', 'type': 'article', 'access_date': '2014-12-25'}

        request = testing.DummyRequest(post=post_data, db=self.collection)

        try:
            general_post(request)
        except:
            pass

        request = testing.DummyRequest(params={'offset': 3}, db=self.collection)
    
        with self.assertRaises(httpexceptions.HTTPBadRequest):
            response = articles(request) 

    def test_article(self):
        from ratchet.views import article, general_post

        post_data = {'code': 'S0104-77602014000100002', 'page': 'abstract', 'type': 'article', 'access_date': '2014-12-25'}

        request = testing.DummyRequest(post=post_data, db=self.collection)

        try:
            general_post(request)
        except:
            pass

        request = testing.DummyRequest(db=self.collection)
        request.matchdict.update(dict(code='S0104-77602014000100002'))

        response = article(request)        

        self.assertEqual(response['code'], 'S0104-77602014000100002')
        self.assertEqual(response['total'], 1)

    def test_article_invalid_issn(self):
        from ratchet.views import article

        request = testing.DummyRequest(db=self.collection)
        request.matchdict.update(dict(code='xxx'))

        with self.assertRaises(httpexceptions.HTTPBadRequest):
            article(request)

    def test_issues(self):
        from ratchet.views import issues, general_post

        post_data = {'code': '0104-776020140001', 'page': 'toc', 'type': 'issue', 'access_date': '2014-12-25'}

        request = testing.DummyRequest(post=post_data, db=self.collection)

        try:
            general_post(request)
        except:
            pass

        post_data = {'code': '0100-076020140001', 'page': 'toc', 'type': 'issue', 'access_date': '2014-12-25'}

        request = testing.DummyRequest(post=post_data, db=self.collection)

        try:
            general_post(request)
        except:
            pass

        request = testing.DummyRequest(db=self.collection)

        response = issues(request)        

        self.assertEqual(len(response['objects']), 2)

    def test_issues_offset_exceeded_lt(self):
        from ratchet.views import issues, general_post

        post_data = {'code': '0104-776020140001', 'page': 'toc', 'type': 'issue', 'access_date': '2014-12-25'}

        request = testing.DummyRequest(post=post_data, db=self.collection)

        try:
            general_post(request)
        except:
            pass

        post_data = {'code': '0100-076020140001', 'page': 'toc', 'type': 'issue', 'access_date': '2014-12-25'}

        request = testing.DummyRequest(post=post_data, db=self.collection)

        try:
            general_post(request)
        except:
            pass

        request = testing.DummyRequest(params={'offset': -1}, db=self.collection)
    
        with self.assertRaises(httpexceptions.HTTPBadRequest):
            response = issues(request)        

    def test_issues_offset_exceeded_gt(self):
        from ratchet.views import issues, general_post

        post_data = {'code': '0104-776020140001', 'page': 'toc', 'type': 'issue', 'access_date': '2014-12-25'}

        request = testing.DummyRequest(post=post_data, db=self.collection)

        try:
            general_post(request)
        except:
            pass

        post_data = {'code': '0100-076020140001', 'page': 'toc', 'type': 'issue', 'access_date': '2014-12-25'}

        request = testing.DummyRequest(post=post_data, db=self.collection)

        try:
            general_post(request)
        except:
            pass

        request = testing.DummyRequest(params={'offset': 3}, db=self.collection)
    
        with self.assertRaises(httpexceptions.HTTPBadRequest):
            response = issues(request) 

    def test_issue(self):
        from ratchet.views import issue, general_post

        post_data = {'code': '0104-776020140001', 'page': 'toc', 'type': 'issue', 'access_date': '2014-12-25'}

        request = testing.DummyRequest(post=post_data, db=self.collection)

        try:
            general_post(request)
        except:
            pass

        request = testing.DummyRequest(db=self.collection)
        request.matchdict.update(dict(code='0104-776020140001'))

        response = issue(request)        

        self.assertEqual(response['code'], '0104-776020140001')
        self.assertEqual(response['total'], 1)

    def test_issue_invalid_issn(self):
        from ratchet.views import issue

        request = testing.DummyRequest(db=self.collection)
        request.matchdict.update(dict(code='xxx'))

        with self.assertRaises(httpexceptions.HTTPBadRequest):
            issue(request)

    def test_journals(self):
        from ratchet.views import journals, general_post

        post_data = {'code': '0104-7760', 'page': 'journal', 'type': 'journal', 'access_date': '2014-12-25'}

        request = testing.DummyRequest(post=post_data, db=self.collection)

        try:
            general_post(request)
        except:
            pass

        post_data = {'code': '0100-0760', 'page': 'journal', 'type': 'journal', 'access_date': '2014-12-25'}

        request = testing.DummyRequest(post=post_data, db=self.collection)

        try:
            general_post(request)
        except:
            pass

        request = testing.DummyRequest(db=self.collection)

        response = journals(request)        

        self.assertEqual(len(response['objects']), 2)

    def test_journals_offset_exceeded_lt(self):
        from ratchet.views import journals, general_post

        post_data = {'code': '0104-7760', 'page': 'journal', 'type': 'journal', 'access_date': '2014-12-25'}

        request = testing.DummyRequest(post=post_data, db=self.collection)

        try:
            general_post(request)
        except:
            pass

        post_data = {'code': '0100-0760', 'page': 'journal', 'type': 'journal', 'access_date': '2014-12-25'}

        request = testing.DummyRequest(post=post_data, db=self.collection)

        try:
            general_post(request)
        except:
            pass

        request = testing.DummyRequest(params={'offset': -1}, db=self.collection)
    
        with self.assertRaises(httpexceptions.HTTPBadRequest):
            response = journals(request)        

    def test_journals_offset_exceeded_gt(self):
        from ratchet.views import journals, general_post

        post_data = {'code': '0104-7760', 'page': 'journal', 'type': 'journal', 'access_date': '2014-12-25'}

        request = testing.DummyRequest(post=post_data, db=self.collection)

        try:
            general_post(request)
        except:
            pass

        post_data = {'code': '0100-0760', 'page': 'journal', 'type': 'journal', 'access_date': '2014-12-25'}

        request = testing.DummyRequest(post=post_data, db=self.collection)

        try:
            general_post(request)
        except:
            pass

        request = testing.DummyRequest(params={'offset': 3}, db=self.collection)
    
        with self.assertRaises(httpexceptions.HTTPBadRequest):
            response = journals(request) 

    def test_journal(self):
        from ratchet.views import journal, general_post

        post_data = {'code': '0104-7760', 'page': 'journal', 'type': 'journal', 'access_date': '2014-12-25'}

        request = testing.DummyRequest(post=post_data, db=self.collection)

        try:
            general_post(request)
        except:
            pass

        request = testing.DummyRequest(db=self.collection)
        request.matchdict.update(dict(code='0104-7760'))

        response = journal(request)        

        self.assertEqual(response['code'], '0104-7760')
        self.assertEqual(response['total'], 1)

    def test_journal_invalid_issn(self):
        from ratchet.views import journal

        request = testing.DummyRequest(db=self.collection)
        request.matchdict.update(dict(code='xxx'))

        with self.assertRaises(httpexceptions.HTTPBadRequest):
            journal(request)

    def test_general_get_invalid_type_doc(self):
        from ratchet.views import general_get

        params = {'code': 'scl', 'type': 'xxx'}

        request = testing.DummyRequest(params=params, db=self.collection)

        with self.assertRaises(httpexceptions.HTTPBadRequest):
            general_get(request)

    def test_general_get_invalid_offset_out_of_range_gt(self):
        from ratchet.views import general_get

        params = {'code': 'scl', 'type': 'journal', 'offset': 1000}

        request = testing.DummyRequest(params=params, db=self.collection)

        with self.assertRaises(httpexceptions.HTTPBadRequest):
            general_get(request)

    def test_general_get_invalid_offset_out_of_range_lt(self):
        from ratchet.views import general_get

        params = {'code': 'scl', 'type': 'journal', 'offset': -1}

        request = testing.DummyRequest(params=params, db=self.collection)

        with self.assertRaises(httpexceptions.HTTPBadRequest):
            general_get(request)

    def test_general_bulk(self):
        from ratchet.views import general_bulk

        post_data = {
            'data': json.dumps({
                "code": "S0034-89102009000400003",
                "journal": "0034-8910",
                "issue": "0034-891020090004",
                "abstract.y2011.m10.d01": 100,
                "abstract.y2011.m10.d02": 100,
                "abstract.y2011.m10.d03": 100,
                "abstract.y2012.m11.d01": 10,
                "abstract.y2012.m11.a02": 10,
                "abstract.y2012.m11.a03": 10,
                "abstract.y2012.m10.total": 300,
                "abstract.y2012.m11.total": 30,
                "abstract.y2012.total": 330,
                "abstract.total": 330,
                "total": 330,
                "type": "article"
            })
        }

        request = testing.DummyRequest(post=post_data, db=self.collection)

        with self.assertRaises(httpexceptions.HTTPCreated):
            general_bulk(request)

        self.assertEqual(
            self.collection.find_one()['abstract']['y2011']['m10']['d01'],
            100
        )

    def test_general_bulk_unauthorized(self):
        from ratchet.views import general_bulk

        post_data = {
            'admintoken': 'invalid',
            'data': json.dumps({
                "code": "S0034-89102009000400003",
                "journal": "0034-8910",
                "issue": "0034-891020090004",
                "abstract.y2011.m10.d01": 100,
                "abstract.y2011.m10.d02": 100,
                "abstract.y2011.m10.d03": 100,
                "abstract.y2012.m11.d01": 10,
                "abstract.y2012.m11.a02": 10,
                "abstract.y2012.m11.a03": 10,
                "abstract.y2012.m10.total": 300,
                "abstract.y2012.m11.total": 30,
                "abstract.y2012.total": 330,
                "abstract.total": 330,
                "total": 330,
                "type": "article"
            })
        }

        request = testing.DummyRequest(post=post_data, db=self.collection)

        with self.assertRaises(httpexceptions.HTTPUnauthorized):
            general_bulk(request)

    def test_general_post(self):
        from ratchet.views import general_post

        post_data = {'code': 'scl', 'page': 'journal', 'access_date': '2014-12-25'}

        request = testing.DummyRequest(post=post_data, db=self.collection)

        with self.assertRaises(httpexceptions.HTTPCreated):
            general_post(request)

        self.assertEqual(
            self.collection.find_one()['journal']['y2014']['m12']['d25'],
            1
        )

    def test_general_post_unauthorized(self):
        from ratchet.views import general_post

        post_data = {'code': 'scl', 'page': 'journal', 'access_date': '2014-12-25', 'admintoken': 'invalid'}

        request = testing.DummyRequest(post=post_data, db=self.collection)

        with self.assertRaises(httpexceptions.HTTPUnauthorized):
            general_post(request)

    def test_general_post_invalid_date(self):
        from ratchet.views import general_post

        post_data = {'code': 'scl', 'page': 'journal', 'access_date': '2014-1x-25'}

        request = testing.DummyRequest(post=post_data, db=self.collection)

        with self.assertRaises(httpexceptions.HTTPBadRequest):
            general_post(request)

    def test_general_post_invalid_type_doc(self):
        from ratchet.views import general_post

        post_data = {'code': 'scl', 'page': 'journal', 'type': 'xxxx', 'access_date': '2014-12-25'}

        request = testing.DummyRequest(post=post_data, db=self.collection)

        with self.assertRaises(httpexceptions.HTTPBadRequest):
            general_post(request)

    def test_general_post_current_datetime(self):
        from ratchet.views import general_post

        post_data = {'code': 'scl', 'page': 'journal'}

        request = testing.DummyRequest(post=post_data, db=self.collection)

        try:
            general_post(request)
        except:
            pass

        day = 'd%02d' % datetime.date.today().day
        month = 'm%02d' % datetime.date.today().month
        year = 'y%02d' % datetime.date.today().year

        self.assertEqual(
            self.collection.find_one()['journal'][year][month][day],
            1
        )