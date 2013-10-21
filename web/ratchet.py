import urllib
import urllib2
import json
from datetime import date
from pymongo import Connection

from tornado import (
    httpserver,
    httpclient,
    ioloop,
    options,
    web,
    gen
    )

from tornado.options import (
    define,
    options
    )

import tornado
import asyncmongo

define("port", default=8888, help="run on the given port", type=int)
define("mongodb_port", default=27017, help="run MongoDB on the given port", type=int)
define("mongodb_host", default='localhost', help="run MongoDB on the given hostname")
define("mongodb_database", default='analytics', help="Record accesses on the given database")
define("mongodb_max_connections", default=2000, help="run MongoDB with the given max connections", type=int)
define("mongodb_max_cached", default=0, help="run MongoDB with the given max cached", type=int)
define("mongodb_max_usage", default=0, help="run MongoDB with the given max cached", type=int)
define("mongodb_min_cached", default=1000, help="run MongoDB with the given min cached", type=int)
define("resources", default=None, help="indicates a txt file with api resources. Once this parameter is defined, the API will just work as accesses delivery.", type=str)
define("allowed_hosts", default=None, help="indicates a txt file with hostnames allowed to post data.", type=str)
define("broadcast_timeout", default=1, help="indicates the max timeout in seconds that the broadcast must finish.", type=str)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", RootHandler),
            (r"/api/v1/general", GeneralHandler),
            (r"/api/v1/general/bulk", BulkGeneralHandler),
            (r"/api/v1/journal", JournalHandler),
            (r"/api/v1/journal/bulk", BulkJournalHandler),
            (r"/api/v1/issue", IssueHandler),
            (r"/api/v1/issue/bulk", BulkIssueHandler),
            (r"/api/v1/article", ArticleHandler),
            (r"/api/v1/article/bulk", BulkArticleHandler),
            (r"/api/v1/pdf", PdfHandler),
            (r"/api/v1/pdf/bulk", BulkPdfHandler),
        ]

        # Creating Indexes without asyncmongo.
        coll = Connection(options.mongodb_host, options.mongodb_port)[options.mongodb_database]['accesses']
        coll.ensure_index('code')
        coll.ensure_index('page')
        coll.ensure_index('type')

        self.db = asyncmongo.Client(
            pool_id='accesses',
            host=options.mongodb_host,
            port=options.mongodb_port,
            maxcached=options.mongodb_max_cached,
            maxconnections=options.mongodb_max_connections,
            dbname=options.mongodb_database
        )

        # Loading Alpha-3 Country codes for regions definition
        self.alpha3 = {}
        with open('iso_alpha3.txt') as f:
            for line in f:
                line = line.split(';')
                self.alpha3[line[0].lower()] = line[1]

        # Local is the default the default way that ratchet works.
        self.broadcast_timeout = options.broadcast_timeout
        self.api_style = 'local'
        self.resources = {}
        if options.resources:
            with open(options.resources) as f:
                for line in f:
                    line = line.split(';')
                    self.resources[line[0]] = line[1]

            if len(self.resources) > 0:
                self.api_style = 'global'
                handlers.append((r"/api/v1/resources", ResourcesHandler))

        tornado.web.Application.__init__(self, handlers)


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Methods", "GET, POST")
        self.set_header("Access-Control-Allow-Origin", "*")


class RootHandler(tornado.web.RequestHandler):
    def get(self):
        if self.application.api_style == 'global':
            self.write("Another Ratchet Global Resource")
        else:
            self.write("Another Ratchet Local Resource")
        self.finish()


class ResourcesHandler(tornado.web.RequestHandler):

    def get(self):
        response = {}
        for resource_name, resource_url in self.application.resources.items():

            resource_url = resource_url.strip()
            url = "http://%s/" % resource_url
            response[resource_name] = {}
            response[resource_name]['host'] = resource_url
            try:
                urllib2.urlopen(url)
                response[resource_name]['status'] = 'online'
            except urllib2.URLError:
                response[resource_name]['status'] = 'offline'
                continue

        self.write(str(response))
        self.finish()


class BulkPdfHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        self._db = self.application.db
        return self._db

    def post(self):

        data = self.get_argument('data', 'No data received')

        data = json.loads(data)

        code = data['code']
        journal = data['journal']
        issue = data['issue']

        del data['code']
        del data['journal']
        del data['issue']

        self.db.accesses.update(
            {'code': code},
            {'$set': {'type': 'article', 'journal': journal, 'issue': issue}, '$inc': data},
            safe=False,
            upsert=True
        )


class PdfHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        self._db = self.application.db
        return self._db

    def post(self):
        code = self.get_argument('code')
        region = self.get_argument('region', None)
        journal = self.get_argument('journal')
        issue = self.get_argument('issue')
        access_date = self.get_argument('access_date', None)

        if access_date:
            day = access_date[8:10]
            month = access_date[5:7]
            year = access_date[0:4]
        else:
            day = '%02d' % date.today().day
            month = '%02d' % date.today().month
            year = '%02d' % date.today().year

        lday = 'pdf.y{0}.m{1}.d{2}'.format(year, month, day)
        lmonth = 'pdf.y{0}.m{1}.total'.format(year, month)
        lyear = 'pdf.y{0}.total'.format(year)

        inc = {
            lmonth: 1,
            lday: 1,
            lyear: 1,
            'total': 1
            }

        if region:
            if region in self.application.alpha3:
                inc['region.' + region] = 1

        self.db.accesses.update(
            {'code': code}, {
                '$set': {
                    'type': 'article',
                    'journal': journal,
                    'issue': issue
                    },
                '$inc': inc
                },
            safe=False,
            upsert=True
        )


class GeneralHandler(tornado.web.RequestHandler):

    def _on_get_response(self, response, error):
        if error:
            raise tornado.web.HTTPError(500)

        if len(response) > 0:
            self.write(json.dumps(response))

        self.finish()

    @property
    def db(self):
        self._db = self.application.db
        return self._db

    def post(self):
        code = self.get_argument('code')
        page = self.get_argument('page', None)
        access_date = self.get_argument('access_date', None)

        if access_date:
            day = access_date[8:10]
            month = access_date[5:7]
            year = access_date[0:4]
        else:
            day = '%02d' % date.today().day
            month = '%02d' % date.today().month
            year = '%02d' % date.today().year

        lday = 'y{0}.m{1}.d{2}'.format(year, month, day)
        lmonth = 'y{0}.m{1}.total'.format(year, month)
        lyear = 'y{0}.total'.format(year)

        inc = {
            lday: 1,
            lmonth: 1,
            lyear: 1,
            'total': 1
        }

        if page:
            inc[page + '.' + lday] = 1
            inc[page + '.' + lmonth] = 1
            inc[page + '.' + lyear] = 1
            inc[page + '.total'] = 1

        self.db.accesses.update(
            {'code': code}, {
                '$inc': inc
            },
            safe=False,
            upsert=True)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        code = self.get_argument('code', None)
        type_doc = self.get_argument('type', None)
        limit = int(self.get_argument('limit', 10))

        query = {"code": code}
        if type_doc:
            query = {"type": type_doc}

        self.db.accesses.find(query, {"_id": 0}, limit=limit, callback=self._on_get_response)


class BulkGeneralHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        self._db = self.application.db
        return self._db

    def post(self):
        data = self.get_argument('data', 'No data received')

        data = json.loads(data)

        code = data['code']

        if 'journal' in data:
            journal = data['journal']
            del data['journal']

        if 'issue' in data:
            issue = data['issue']
            del data['issue']

        include_set = {
                        'journal': journal,
                        'issue': issue,
                      }

        del data['code']

        self.db.accesses.update(
            {'code': code}, {
                '$set': include_set,
                '$inc': data
                },
            safe=False,
            upsert=True)


class BulkArticleHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        self._db = self.application.db
        return self._db

    def post(self):

        data = self.get_argument('data', 'No data received')

        data = json.loads(data)

        code = data['code']
        journal = data['journal']
        issue = data['issue']

        del data['code']
        del data['journal']
        del data['issue']

        self.db.accesses.update(
            {'code': code}, {
                '$set': {
                    'type': 'article',
                    'journal': journal,
                    'issue': issue
                    },
                '$inc': data
                },
            safe=False,
            upsert=True)


class ArticleHandler(tornado.web.RequestHandler):

    def _on_get_response(self, response, error):
        if error:
            raise tornado.web.HTTPError(500)

        if len(response) > 0:
            self.write(json.dumps(response[0]))

        self.finish()

    @property
    def db(self):
        self._db = self.application.db
        return self._db

    def post(self):
        code = self.get_argument('code')
        region = self.get_argument('region', None)
        journal = self.get_argument('journal')
        issue = self.get_argument('issue')
        access_date = self.get_argument('access_date', None)

        if access_date:
            day = access_date[8:10]
            month = access_date[5:7]
            year = access_date[0:4]
        else:
            day = '%02d' % date.today().day
            month = '%02d' % date.today().month
            year = '%02d' % date.today().year

        lday = 'article.y{0}.m{1}.d{2}'.format(year, month, day)
        lmonth = 'article.y{0}.m{1}.total'.format(year, month)
        lyear = 'article.y{0}.total'.format(year)

        inc = {
            lmonth: 1,
            lday: 1,
            lyear: 1,
            'total': 1
            }

        if region:
            if region in self.application.alpha3:
                inc['region.' + region] = 1

        self.db.accesses.update(
            {'code': code}, {
                '$set': {
                    'type': 'article',
                    'journal': journal,
                    'issue': issue
                    },
                '$inc': inc
                },
            safe=False,
            upsert=True)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        code = self.get_argument('code')

        self.db.accesses.find({"code": code, "type": "article"}, {"_id": 0}, limit=1, callback=self._on_get_response)


class BulkIssueHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        self._db = self.application.db
        return self._db

    def post(self):

        data = self.get_argument('data', 'No data received')

        data = json.loads(data)

        code = data['code']
        journal = data['journal']

        del data['code']
        del data['journal']

        self.db.accesses.update(
            {'code': code}, {
                '$set': {
                    'type': 'issue',
                    'journal': journal
                    },
                '$inc': data
                },
            safe=False,
            upsert=True)


class IssueHandler(tornado.web.RequestHandler):

    def _on_get_response(self, response, error):
        if error:
            raise tornado.web.HTTPError(500)

        if len(response) > 0:
            self.write(json.dumps(response[0]))

        self.finish()

    @property
    def db(self):
        self._db = self.application.db
        return self._db

    def post(self):
        code = self.get_argument('code')
        region = self.get_argument('region', None)
        journal = self.get_argument('journal')
        access_date = self.get_argument('access_date', None)

        if access_date:
            day = access_date[8:10]
            month = access_date[5:7]
            year = access_date[0:4]
        else:
            day = '%02d' % date.today().day
            month = '%02d' % date.today().month
            year = '%02d' % date.today().year

        lday = 'issue.y{0}.m{1}.d{2}'.format(year, month, day)
        lmonth = 'issue.y{0}.m{1}.total'.format(year, month)
        lyear = 'issue.y{0}.total'.format(year)

        inc = {
            lmonth: 1,
            lday: 1,
            lyear: 1,
            'total': 1
            }

        if region:
            if region in self.application.alpha3:
                inc['region.' + region] = 1

        self.db.accesses.update(
            {'code': code}, {
                '$set': {
                    'type': 'issue',
                    'journal': journal
                    },
                '$inc': inc
                },
            safe=False,
            upsert=True)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        code = self.get_argument('code')

        self.db.accesses.find({"code": code, "type": "issue"}, {"_id": 0}, limit=1, callback=self._on_get_response)


class BulkJournalHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        self._db = self.application.db
        return self._db

    def post(self):

        data = self.get_argument('data', 'No data received')

        data = json.loads(data)

        code = data['code']

        del data['code']

        self.db.accesses.update(
            {'code': code}, {
                '$set': {'type': 'journal'},
                '$inc': data},
            safe=False,
            upsert=True
        )


class JournalHandler(tornado.web.RequestHandler):

    def _on_get_response(self, response, error):
        if error:
            raise tornado.web.HTTPError(500)

        if len(response) > 0:
            self.write(json.dumps(response[0]))

        self.finish()

    @property
    def db(self):
        self._db = self.application.db
        return self._db

    def post(self):
        code = self.get_argument('code')
        region = self.get_argument('region', None)
        access_date = self.get_argument('access_date', None)

        if access_date:
            day = access_date[8:10]
            month = access_date[5:7]
            year = access_date[0:4]
        else:
            day = '%02d' % date.today().day
            month = '%02d' % date.today().month
            year = '%02d' % date.today().year

        lday = 'journal.y{0}.m{1}.d{2}'.format(year, month, day)
        lmonth = 'journal.y{0}.m{1}.total'.format(year, month)
        lyear = 'journal.y{0}.total'.format(year)

        inc = {
            lmonth: 1,
            lday: 1,
            lyear: 1,
            'total': 1
            }

        if region:
            if region in self.application.alpha3:
                inc['region.' + region] = 1

        self.db.accesses.update(
            {'code': code}, {
                '$set': {
                    'type': 'journal'
                    },
                '$inc': inc
                },
            safe=False,
            upsert=True)

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        code = self.get_argument('code')

        self.db.accesses.find({"code": code, "type": "journal"}, {"_id": 0}, limit=1, callback=self._on_get_response)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
