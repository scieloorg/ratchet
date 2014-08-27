import urllib
import urllib2
import uuid
import json
import re

from datetime import date
from functools import wraps

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

define("host", default='localhost', help="run on the given host")
define("port", default=80, help="run on the given port", type=int)
define("mongodb_port", default=27017, help="run MongoDB on the given port", type=int)
define("mongodb_host", default='localhost', help="run MongoDB on the given hostname")
define("mongodb_database", default='analytics', help="Record accesses on the given database")
define("mongodb_max_connections", default=2000, help="run MongoDB with the given max connections", type=int)
define("mongodb_max_cached", default=0, help="run MongoDB with the given max cached", type=int)
define("mongodb_max_usage", default=0, help="run MongoDB with the given max cached", type=int)
define("mongodb_min_cached", default=1000, help="run MongoDB with the given min cached", type=int)
define("allowed_hosts", default=None, help="indicates a txt file with hostnames allowed to post data.", type=str)
define("manager_token", default=str(uuid.uuid4()), help="indicates a token that must be used to manage allowed_tokens.", type=str)
define("broadcast_timeout", default=1, help="indicates the max timeout in seconds that the broadcast must finish.", type=str)


LIMIT = 20
REGEX_ISSN = re.compile("^[0-9]{4}-[0-9]{3}[0-9xX]$")
REGEX_ISSUE = re.compile("^[0-9]{4}-[0-9]{3}[0-9xX][0-2][0-9]{3}[0-9]{4}$")
REGEX_ARTICLE = re.compile("^S[0-9]{4}-[0-9]{3}[0-9xX][0-2][0-9]{3}[0-9]{4}[0-9]{5}$")
REGEX_FBPE = re.compile("^S[0-9]{4}-[0-9]{3}[0-9xX]\([0-9]{2}\)[0-9]{8}$")


def authenticated(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):

        api_token = self.get_argument('api_token', None)

        if not api_token:
            raise tornado.web.HTTPError(401)

        if api_token != self.application.manager_token:
            raise tornado.web.HTTPError(401)
        else:
            r = func(self, *args, **kwargs)
            return r

    return wrapper


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"^/$", RootHandler),
            (r"^/api/v1/$", EndpointsHandler),
            (r"^/api/v1/general", GeneralHandler),
            (r"^/api/v1/general/bulk", BulkGeneralHandler),
            (r"^/api/v1/journals/", JournalHandler),
            (r"^/api/v1/journals/(?P<code>.*?)/?", JournalHandler),
            (r"^/api/v1/issues/", IssueHandler),
            (r"^/api/v1/issues/(?P<code>.*?)/?", IssueHandler),
            (r"^/api/v1/articles/", ArticleHandler),
            (r"^/api/v1/articles/(?P<code>.*?)/?", ArticleHandler),
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
        self.manager_token = options.manager_token
        self.api_style = 'local'

        tornado.web.Application.__init__(self, handlers)


class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Methods", "GET, POST")
        self.set_header("Access-Control-Allow-Origin", "*")


class RootHandler(tornado.web.RequestHandler):
    def get(self):

        self.write("Ratchet API")
        self.finish()


class GeneralHandler(tornado.web.RequestHandler):

    def _on_get_response(self, response, error):
        if error:
            raise tornado.web.HTTPError(500)

        data = None
        if len(response) == 1:
            data = response[0]

        self.write(json.dumps(data))

        self.finish()

    @property
    def db(self):
        self._db = self.application.db
        return self._db

    @authenticated
    def post(self):
        code = self.get_argument('code')
        page = self.get_argument('page', None)
        type_doc = self.get_argument('type_doc', None)
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

        dat = {}
        if page:
            inc[page + '.' + lday] = 1
            inc[page + '.' + lmonth] = 1
            inc[page + '.' + lyear] = 1
            inc[page + '.total'] = 1
            dat['$inc'] = inc

        if type_doc:
            dat['$set'] = {'type': type_doc}

        self.db.accesses.update(
            {'code': code}, dat,
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

    @authenticated
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


class EndpointsHandler(tornado.web.RequestHandler):

    rdata = {}

    @tornado.web.asynchronous
    @tornado.gen.engine
    @tornado.web.addslash
    def get(self, code=None):

        endpoints = ['general', 'journals', 'issues', 'articles']

        available_endpoints = {}
        for endpoint in endpoints:
            available_endpoints[endpoint] = {'list_endpoint': '/api/v1/%s' % endpoint}

        self.write(json.dumps(available_endpoints))
        self.finish()


def get_next(endpoint, total, limit, offset):

    offset += limit
    if offset >= total:
        return None

    return '/api/v1/%s?offset=%s' % (endpoint, offset)


def get_previous(endpoint, total, limit, offset):
    offset -= limit
    if offset <= 0:
        return None

    return '/api/v1/%s?offset=%s' % (endpoint, offset)


class JournalHandler(tornado.web.RequestHandler):

    rdata = {}
    total = None

    def _on_count_get_response(self, response, error):
        if error:
            raise tornado.web.HTTPError(500)

        self.total = response['n']

    def _on_get_response(self, response, error):
        if error:
            raise tornado.web.HTTPError(500)

        meta = self.rdata.setdefault('meta', {})
        meta['limit'] = LIMIT
        meta['offset'] = self.get_argument('offset', 0)
        self.rdata['objects'] = response

        while not self.total:
            pass

        meta['total'] = self.total
        meta['next'] = get_next('journals', meta['total'], meta['limit'], int(meta['offset']))
        meta['previous'] = get_previous('journals', meta['total'], meta['limit'], int(meta['offset']))

        self.write(json.dumps(self.rdata))
        self.finish()

    @property
    def db(self):
        self._db = self.application.db
        return self._db

    @tornado.web.asynchronous
    @tornado.gen.engine
    @tornado.web.addslash
    def get(self, code=None):
        offset = int(self.get_argument('offset', 0))

        query = {'type': 'journal'}

        if code:
            if REGEX_ISSN.search(code):
                query['code'] = code
            else:
                raise tornado.web.HTTPError(400)

        command = {
            'count': 'accesses',
            'query': query
        }

        self.db.command(command, callback=self._on_count_get_response)

        self.db.accesses.find(
            query,
            {"_id": 0},
            limit=LIMIT,
            skip=offset,
            sort=[('total', -1)],
            callback=self._on_get_response
        )


class IssueHandler(tornado.web.RequestHandler):

    rdata = {}
    total = None

    def _on_count_get_response(self, response, error):
        if error:
            raise tornado.web.HTTPError(500)

        self.total = response['n']

    def _on_get_response(self, response, error):
        if error:
            raise tornado.web.HTTPError(500)

        meta = self.rdata.setdefault('meta', {})
        meta['limit'] = LIMIT
        meta['offset'] = self.get_argument('offset', 0)
        self.rdata['objects'] = response

        while not self.total:
            pass

        meta['total'] = self.total
        meta['next'] = get_next('journals', meta['total'], meta['limit'], int(meta['offset']))
        meta['previous'] = get_previous('journals', meta['total'], meta['limit'], int(meta['offset']))

        self.write(json.dumps(self.rdata))

        self.finish()

    @property
    def db(self):
        self._db = self.application.db
        return self._db

    @tornado.web.asynchronous
    @tornado.gen.engine
    @tornado.web.addslash
    def get(self, code=None):
        offset = int(self.get_argument('offset', 0))

        query = {'type': 'toc'}

        if code:
            if REGEX_ISSUE.search(code):
                query['code'] = code
            else:
                raise tornado.web.HTTPError(400)

        command = {
            'count': 'accesses',
            'query': query
        }

        self.db.command(command, callback=self._on_count_get_response)

        self.db.accesses.find(
            query,
            {"_id": 0},
            limit=LIMIT,
            skip=offset,
            sort=[('total', -1)],
            callback=self._on_get_response
        )


class ArticleHandler(tornado.web.RequestHandler):

    rdata = {}
    total = None

    def _on_count_get_response(self, response, error):
        if error:
            raise tornado.web.HTTPError(500)

        self.total = response['n']

    def _on_get_response(self, response, error):
        if error:
            raise tornado.web.HTTPError(500)

        meta = self.rdata.setdefault('meta', {})
        meta['limit'] = LIMIT
        meta['offset'] = self.get_argument('offset', 0)
        self.rdata['objects'] = response

        while not self.total:
            pass

        meta['total'] = self.total
        meta['next'] = get_next('journals', meta['total'], meta['limit'], int(meta['offset']))
        meta['previous'] = get_previous('journals', meta['total'], meta['limit'], int(meta['offset']))

        self.write(json.dumps(self.rdata))

        self.finish()

    @property
    def db(self):
        self._db = self.application.db
        return self._db

    @tornado.web.asynchronous
    @tornado.gen.engine
    @tornado.web.addslash
    def get(self, code=None):
        offset = int(self.get_argument('offset', 0))

        query = {'type': 'article'}

        if code:
            if REGEX_ARTICLE.search(code) or REGEX_FBPE.search(code):
                query['code'] = code
            else:
                raise tornado.web.HTTPError(400)

        command = {
            'count': 'accesses',
            'query': query
        }

        self.db.command(command, callback=self._on_count_get_response)

        self.db.accesses.find(
            query,
            {"_id": 0},
            limit=LIMIT,
            skip=offset,
            sort=[('total', -1)],
            callback=self._on_get_response
        )


if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(
        Application(),
        no_keep_alive=True
    )
    http_server.listen(options.port, address=options.host)
    tornado.ioloop.IOLoop.instance().start()
