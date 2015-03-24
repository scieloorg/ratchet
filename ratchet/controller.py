# coding: utf-8

LIMIT = 20

def get_next_endpoint(endpoint, total, limit, offset, fltr=None):

    offset += limit
    if offset >= total:
        return None

    fltrs = ''
    if fltr:
        fltrs += '&%s' % '&'.join(set(['='.join([key, value]) for key, value in fltr.items()]))

    return '/api/v1/%s/?offset=%s%s' % (endpoint, offset, fltrs)


def get_previous_endpoint(endpoint, total, limit, offset, fltr=None):
    offset -= limit
    if offset < 0:
        return None

    fltrs = ''
    if fltr:
        fltrs += '&%s' % '&'.join(set(['='.join([key, value]) for key, value in fltr.items()]))

    return '/api/v1/%s/?offset=%s%s' % (endpoint, offset, fltrs)


class Ratchet(object):

    def __init__(self, database):

        self._db = database


    def general(self, type_doc=None, collection=None, code=None, limit=LIMIT, offset=0):
        """
        Metodo para retorno de qualquer tipo de registro a partir de um codigo.
        O código pode ser um PID de artigo, fascículo, ISSN e path de arquivo pdf.
        """

        query = {}

        if type_doc:
            query['type_doc'] = type_doc

        if code:
            query['code'] = code

        if collection:
            query['code'] = collection

        data = {}

        total = self._db.find(query).count()

        meta = data.setdefault('meta', {})
        meta['limit'] = limit
        meta['offset'] = offset
        meta['total'] = total
        meta['next'] = get_next_endpoint('general', meta['total'], limit, int(meta['offset']), query)
        meta['previous'] = get_previous_endpoint('general', meta['total'], limit, int(meta['offset']), query)

        records = self._db.find(
            query,
            {"_id": 0},
            limit=limit,
            skip=offset,
            sort=[('total', -1)]
        )


        data['objects'] = [i for i in records]

        return data

    def general_post(self, code, page, type_doc, access_date):
        """
            code: ISSUE_PID, PID, ISSN, pdf path
            page: ['journal', 'issue_toc', 'abstract', 'html']
            type_doc: ['article', 'issue', 'journal', 'website']
            acess_date: YYYY-DD-MM
        """

        day = access_date[8:10]
        month = access_date[5:7]
        year = access_date[0:4]

        lday = 'y{0}.m{1}.d{2}'.format(year, month, day)
        lmonth = 'y{0}.m{1}.total'.format(year, month)
        lyear = 'y{0}.total'.format(year)

        inc = {
            lday: 1,
            lmonth: 1,
            lyear: 1,
            'total': 1
        }

        data = {}
        if page:
            inc[page + '.' + lday] = 1
            inc[page + '.' + lmonth] = 1
            inc[page + '.' + lyear] = 1
            inc[page + '.total'] = 1
            data['$inc'] = inc

        if type_doc:
            data['$set'] = {'type': type_doc}

        self._db.update({'code': code}, data, safe=False, upsert=True)


    def general_bulk(self, data):
        """
           Expected data set: http://docs.scielo.org/projects/ratchet/en/latest/api.html#bulk-general-accesses
        """

        code = data['code']

        include_set = {}

        if 'journal' in data:
            include_set['journal'] = data['journal']
            del(data['journal'])

        if 'issue' in data:
            include_set['issue'] = data['issue']
            del(data['issue'])

        if 'page' in data:
            include_set['page'] = data['page']
            del(data['page'])

        if 'type' in data:
            include_set['type'] = data['type']
            del(data['type'])

        del data['code']

        self._db.update(
            {'code': code},
            {'$set': include_set, '$inc': data},
            safe=False,
            upsert=True
        )


    def journals(self, collection=None, limit=LIMIT, offset=0):

        data = {}

        query = {
            'type': 'journal'
        }

        if collection:
            query['collection'] = collection

        total = self._db.find(query).count()

        meta = data.setdefault('meta', {})
        meta['limit'] = limit
        meta['offset'] = offset
        meta['total'] = total
        meta['next'] = get_next_endpoint('journals', meta['total'], limit, int(meta['offset']))
        meta['previous'] = get_previous_endpoint('journals', meta['total'], limit, int(meta['offset']))

        records = self._db.find(
            query,
            {"_id": 0},
            limit=limit,
            skip=offset,
            sort=[('total', -1)]
        )

        data['objects'] = [i for i in records]

        return data

    def journal(self, code):

        query = {
            'type': 'journal',
            'code': code
        }

        record = self._db.find_one(query, {"_id": 0})

        return record

    def issues(self, collection=None, limit=LIMIT, offset=0):

        data = {}

        query = {
            'type': 'issue'
        }

        total = self._db.find(query).count()

        meta = data.setdefault('meta', {})
        meta['limit'] = limit
        meta['offset'] = offset
        meta['total'] = total
        meta['next'] = get_next_endpoint('journals', meta['total'], limit, int(meta['offset']))
        meta['previous'] = get_previous_endpoint('journals', meta['total'], limit, int(meta['offset']))

        records = self._db.find(
            query,
            {"_id": 0},
            limit=limit,
            skip=offset,
            sort=[('total', -1)]
        )

        data['objects'] = [i for i in records]

        return data

    def issue(self, code):

        query = {
            'type': 'issue',
            'code': code
        }

        record = self._db.find_one(query, {"_id": 0})

        return record

    def articles(self, collection=None, limit=LIMIT, offset=0):

        data = {}
        query = {'type': 'article'}

        total = self._db.find(query).count()

        meta = data.setdefault('meta', {})
        meta['limit'] = limit
        meta['offset'] = offset
        meta['total'] = total
        meta['next'] = get_next_endpoint('journals', meta['total'], limit, int(meta['offset']))
        meta['previous'] = get_previous_endpoint('journals', meta['total'], limit, int(meta['offset']))

        records = self._db.find(
            query,
            {"_id": 0},
            limit=limit,
            skip=offset,
            sort=[('total', -1)]
        )

        data['objects'] = [i for i in records]

        return data


    def article(self, code):

        query = {
            'type': 'article',
            'code': code
        }

        record = self._db.find_one(query, {"_id": 0})

        return record



