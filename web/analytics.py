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

define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/api/v1/journal", JournalHandler),
            (r"/api/v1/issue", IssueHandler),
            (r"/api/v1/article", ArticleHandler),
            (r"/api/v1/pdf", PdfHandler),
        ]

        tornado.web.Application.__init__(self, handlers)


class PdfHandler(tornado.web.RequestHandler):
    pass


class ArticleHandler(tornado.web.RequestHandler):
    pass


class IssueHandler(tornado.web.RequestHandler):
    pass


class JournalHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        if not hasattr(self, '_db'):
            self._db = asyncmongo.Client(
                pool_id='accesses',
                host='localhost',
                port=27017,
                maxcached=10,
                maxconnections=600,
                dbname='analytics'
            )

        return self._db

    def post(self):
        code = self.get_argument('code')
        region = self.get_argument('region')
        iso_date = date.isoformat(date.today())
        month_date = iso_date[:7]

        self.db.accesses.update(
            {"code": code},
            {'$inc': {region: 1, iso_date: 1, month_date: 1, 'total': 1}},
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




#define("mongodb_host", default="127.0.0.1:12707", help="analytics database host")
#define("mongodb_database", default="analytics", help="analytics database name")


#

        # Have one global connection to the analytics DB across all handlers
        #self.db = tornado.database.Connection(
            #host=options.mysql_host, database=options.mysql_database,
            #user=options.mysql_user, password=options.mysql_password)


#class JournalHandler(tornado.web.RequestHandler):

    #@property
    #def db(self):
        #if not hasattr(self, '_db'):
            #self._db = asyncmongo.Client(pool_id='accesses', host='127.0.0.1', port=27017, maxcached=10, maxconnections=50, dbname='anaytics')

        #return self._db

    #@tornado.web.asynchronous
    #def get(self):
        #code = self.get_arguments('code')[0]
        #self.write(code)
        #  import pdb
        #  pdb.set_trace()
        #  self.db.accesses.update({"_id" : code}, {'$inc' : {'test_count' : 1}}, safe=False, upsert=True)


#def main():
    #tornado.options.parse_command_line()
    #http_server = tornado.httpserver.HTTPServer(Application())
    #http_server.listen(options.port)
    #tornado.ioloop.IOLoop.instance().start()


#if __name__ == "__main__":
    #main()
