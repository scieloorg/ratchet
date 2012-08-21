from tornado import (
    httpserver,
    ioloop,
    options,
    web
    )

from tornado.options import (
    define,
    options
    )

from datetime import date
import tornado
import asyncmongo
import urllib2

define("port", default=8888, help="run on the given port", type=int)
define("mongodb_port", default=27017, help="run MongoDB on the given port", type=int)
define("mongodb_host", default='localhost', help="run MongoDB on the given hostname")
define("mongodb_database", default='analytics', help="Record accesses on the given database")
define("mongodb_max_connections", default=200, help="run MongoDB with the given max connections", type=int)
define("mongodb_max_cached", default=20, help="run MongoDB with the given max cached", type=int)
define("resources", default=None, help="indicates a txt file with api resources. Once this parameter is defined, the API will just work as accesses delivery.", type=str)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/api/v1/journal", JournalHandler),
            (r"/api/v1/issue", IssueHandler),
            (r"/api/v1/article", ArticleHandler),
            (r"/api/v1/pdf", PdfHandler),
        ]

        self.db = asyncmongo.Client(
            pool_id='accesses',
            host=options.mongodb_host,
            port=options.mongodb_port,
            maxcached=options.mongodb_max_cached,
            maxconnections=options.mongodb_max_connections,
            dbname=options.mongodb_database
        )

        # Local is the default the default way that ratchet works.
        self.api_style = 'local'

        self.resources = []

        if options.resources:
            with open(options.resources) as f:
                for line in f:
                    self.resources.append(line)

            if len(self.resources) > 0:
                self.api_style = 'global'

        tornado.web.Application.__init__(self, handlers)


class PdfHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        self._db = self.application.db
        return self._db

    def post(self):
        code = self.get_argument('code')
        region = self.get_argument('region')
        journal = self.get_argument('journal')
        access_date = self.get_argument('access_date')
        iso_date = access_date
        month_date = iso_date[:7]

        self.db.accesses.update(
            {'code': code},
            {'$set': {'type': 'article', 'journal': journal}, '$inc': {region: 1, iso_date: 1, month_date: 1, 'total': 1}},
            safe=False,
            upsert=True
        )


class ArticleHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        self._db = self.application.db
        return self._db

    def post(self):
        code = self.get_argument('code')
        region = self.get_argument('region')
        journal = self.get_argument('journal')
        iso_date = date.isoformat(date.today())
        month_date = iso_date[:7]

        self.db.accesses.update(
            {'code': code},
            {'$set': {'type': 'article', 'journal': journal}, '$inc': {region: 1, iso_date: 1, month_date: 1, 'total': 1}},
            safe=False,
            upsert=True
        )

    @tornado.web.asynchronous
    def get(self):
        code = self.get_argument('code')

        old_data = self.db.accesses.find_one({"code": code}, limit=1)
        journal = old_data['journal']

        if self.api_style == 'global':
            self.db.accesses.remove({'code': code})
            for resource in self.resources:
                url = "http://%s/api/v1/journal?code=%s" % (resource, code)
                data = urllib2.urlopen(url).read()
                self.db.accesses.update(
                    {'code': code},
                    {'$set': {'type': 'article', 'journal': journal}, '$inc': data},
                    safe=False,
                    upsert=True
                )

        self.db.accesses.find_one({"code": code}, limit=1, callback=self._on_get_response)

    def _on_get_response(self, response, error):
        if error:
            raise tornado.web.HTTPError(500)

        self.write(str(response))
        self.finish()


class IssueHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        self._db = self.application.db
        return self._db

    def post(self):
        code = self.get_argument('code')
        region = self.get_argument('region')
        journal = self.get_argument('journal')
        iso_date = date.isoformat(date.today())
        month_date = iso_date[:7]

        self.db.accesses.update(
            {'code': code},
            {'$set': {'type': 'issue', 'journal': journal}, '$inc': {region: 1, iso_date: 1, month_date: 1, 'total': 1}},
            safe=False,
            upsert=True
        )

    @tornado.web.asynchronous
    def get(self):
        code = self.get_argument('code')
        self.db.accesses.find_one({"code": code}, limit=1, callback=self._on_get_response)

    def _on_get_response(self, response, error):
        if error:
            raise tornado.web.HTTPError(500)

        self.write(str(response))
        self.finish()


class JournalHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        self._db = self.application.db
        return self._db

    def post(self):
        code = self.get_argument('code')
        region = self.get_argument('region')
        iso_date = date.isoformat(date.today())
        month_date = iso_date[:7]

        self.db.accesses.update(
            {'code': code},
            {'$set': {'type': 'journal'}, '$inc': {region: 1, iso_date: 1, month_date: 1, 'total': 1}},
            safe=False,
            upsert=True
        )

    @tornado.web.asynchronous
    def get(self):
        code = self.get_argument('code')
        self.db.accesses.find_one({"code": code}, limit=1, callback=self._on_get_response)

    def _on_get_response(self, response, error):
        if error:
            raise tornado.web.HTTPError(500)

        self.write(str(response))
        self.finish()

if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
