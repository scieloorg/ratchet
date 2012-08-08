import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
from tornado.options import define, options

import asyncmongo

define("port", default=8888, help="run on the given port", type=int)
define("mongodb_host", default="127.0.0.1:12707", help="analytics database host")
define("mongodb_database", default="analytics", help="analytics database name")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/journal", JournalHandler),
            #(r"/issue", IssueHandler),
            #(r"/article", ArticleHandler),
            #(r"/pdf", PdfHandler),
        ]

        tornado.web.Application.__init__(self, handlers)

        # Have one global connection to the analytics DB across all handlers
        #self.db = tornado.database.Connection(
            #host=options.mysql_host, database=options.mysql_database,
            #user=options.mysql_user, password=options.mysql_password)


class JournalHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        if not hasattr(self, '_db'):
            self._db = asyncmongo.Client(pool_id='accesses', host='127.0.0.1', port=27017, 
            								maxcached=10, maxconnections=50, dbname='anaytics')

        return self._db

    @tornado.web.asynchronous
    def get(self):
    	code = self.get_arguments('code')
    	import pdb
    	pdb.set_trace()
        self.db.accesses.update({"_id" : code}, {'$inc' : {'test_count' : 1}}, safe=False, upsert=True)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
