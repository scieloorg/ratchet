import json
import datetime
import re
from functools import wraps

from pyramid.view import view_config
from pyramid.view import view_config, notfound_view_config
from pyramid.response import Response
from pyramid import httpexceptions

LIMIT = 20
ALLOWED_TYPE_DOCS = ['article', 'issue', 'journal', 'website']
REGEX_ISSN = re.compile("^[0-9]{4}-[0-9]{3}[0-9xX]$")
REGEX_ISSUE = re.compile("^[0-9]{4}-[0-9]{3}[0-9xX][0-2][0-9]{3}[0-9]{4}$")
REGEX_ARTICLE = re.compile("^S[0-9]{4}-[0-9]{3}[0-9xX][0-2][0-9]{3}[0-9]{4}[0-9]{5}$")
REGEX_FBPE = re.compile("^S[0-9]{4}-[0-9]{3}[0-9xX]\([0-9]{2}\)[0-9]{8}$")

def get_next(endpoint, total, limit, offset, fltr=None):

    offset += limit
    if offset >= total:
        return None

    fltrs = ''
    if fltr:
        fltrs += '&%s' % '&'.join(set(['='.join([key, value]) for key, value in fltr.items()]))

    return '/api/v1/%s/?offset=%s%s' % (endpoint, offset, fltrs)


def get_previous(endpoint, total, limit, offset, fltr=None):
    offset -= limit
    if offset < 0:
        return None

    fltrs = ''
    if fltr:
        fltrs += '&%s' % '&'.join(set(['='.join([key, value]) for key, value in fltr.items()]))

    return '/api/v1/%s/?offset=%s%s' % (endpoint, offset, fltrs)

def authenticate(func):
    @wraps(func)
    def wrapper(request):
        token = request.registry.settings.get('admintoken', None)
        giventoken = request.POST.get('admintoken', None) or request.GET.get('admintoken', None)
        if giventoken != token:
            raise httpexceptions.HTTPUnauthorized('Invalid admin token')
        result = func(request)
        return result
    return wrapper

@notfound_view_config(append_slash=True)
def notfound(request):
    return httpexceptions.HTTPNotFound('Not found')


@view_config(route_name='index', request_method='GET')
def index(request):
    return Response('Ratchet API')


@view_config(route_name='endpoints', request_method='GET', renderer='json')
def endpoints(request):

    endpoints = ['general', 'journals', 'issues', 'articles']

    available_endpoints = {}
    for endpoint in endpoints:
        available_endpoints[endpoint] = {'list_endpoint': '/api/v1/%s/' % endpoint}

    return available_endpoints

@view_config(route_name='general', request_method='GET', renderer='json')
def general_get(request):
    code = request.GET.get('code', None)
    type_doc = request.GET.get('type', None)
    offset = int(request.GET.get('offset', 0))

    rdata = {}
    total = None

    query = {}

    if type_doc:
        if type_doc in ALLOWED_TYPE_DOCS:
            query['type'] = type_doc
        else:
            raise httpexceptions.HTTPBadRequest('expected type invalid, not in range %s' % str(ALLOWED_TYPE_DOCS))

    if code:
        query['code'] = code

    try:
        total = request.db.find(query).count()
    except:
        raise httpexceptions.HTTPInternalServerError('Fail to connect to the mongodb database')

    if offset > total or offset < 0:
        raise httpexceptions.HTTPBadRequest('offset exceeded the range [0, %s]' % str(total))

    meta = rdata.setdefault('meta', {})
    meta['limit'] = LIMIT
    meta['offset'] = offset
    meta['total'] = total
    meta['next'] = get_next('general', meta['total'], meta['limit'], int(meta['offset']), query)
    meta['previous'] = get_previous('general', meta['total'], meta['limit'], int(meta['offset']), query)

    try:
        records = request.db.find(
            query,
            {"_id": 0},
            limit=LIMIT,
            skip=offset,
            sort=[('total', -1)]
        )
    except:
        raise httpexceptions.HTTPInternalServerError('Fail to connect to the mongodb database')

    rdata['objects'] = [i for i in records]

    return rdata

@view_config(route_name='general', request_method='POST')
@authenticate
def general_post(request):
    code = request.POST.get('code')
    page = request.POST.get('page', None)
    type_doc = request.POST.get('type', None)
    access_date = request.POST.get('access_date', None)
    query = {}

    if type_doc:
        if type_doc in ALLOWED_TYPE_DOCS:
            query['type'] = type_doc
        else:
            raise httpexceptions.HTTPBadRequest('expected type invalid, not in range %s' % str(ALLOWED_TYPE_DOCS))

    if access_date:
        day = access_date[8:10]
        month = access_date[5:7]
        year = access_date[0:4]
        try:
            datetime.datetime(int(year), int(month), int(day))
        except ValueError:
            raise httpexceptions.HTTPBadRequest('Invalid ISO Date %s' % access_date)
    else:
        day = '%02d' % datetime.date.today().day
        month = '%02d' % datetime.date.today().month
        year = '%02d' % datetime.date.today().year

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

    request.db.update(
        {'code': code},
        data,
        safe=False,
        upsert=True
    )

    raise httpexceptions.HTTPCreated

@view_config(route_name='general_bulk', request_method='POST')
@authenticate
def general_bulk(request):
    data = request.POST.get('data', 'No data received')

    data = json.loads(data)

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

    request.db.update(
        {'code': code},
        {'$set': include_set, '$inc': data},
        safe=False,
        upsert=True
    )

    raise httpexceptions.HTTPCreated

@view_config(route_name='journals', request_method='GET', renderer='json')
def journals(request):
    offset = int(request.GET.get('offset', 0))
    rdata = {}
    total = None
    query = {'type': 'journal'}

    total = request.db.find(query).count()

    if offset > total or offset < 0:
        raise httpexceptions.HTTPBadRequest('offset exceeded the range [0, %s]' % str(total))

    meta = rdata.setdefault('meta', {})
    meta['limit'] = LIMIT
    meta['offset'] = offset
    meta['total'] = total
    meta['next'] = get_next('journals', meta['total'], meta['limit'], int(meta['offset']))
    meta['previous'] = get_previous('journals', meta['total'], meta['limit'], int(meta['offset']))

    records = request.db.find(
        query,
        {"_id": 0},
        limit=LIMIT,
        skip=offset,
        sort=[('total', -1)]
    )

    rdata['objects'] = [i for i in records]

    return rdata

@view_config(route_name='journal', request_method='GET', renderer='json')
def journal(request):
    code = request.matchdict.get('code', None)

    query = {'type': 'journal'}

    if REGEX_ISSN.search(code):
        query['code'] = code
    else:
        raise httpexceptions.HTTPBadRequest('Invalid ISSN CODE %s' % code)

    record = request.db.find_one(query, {"_id": 0})

    return record

@view_config(route_name='issues', request_method='GET', renderer='json')
def issues(request):
    offset = int(request.GET.get('offset', 0))
    rdata = {}
    total = None
    query = {'type': 'issue'}

    total = request.db.find(query).count()

    if offset > total or offset < 0:
        raise httpexceptions.HTTPBadRequest('offset exceeded the range [0, %s]' % str(total))

    meta = rdata.setdefault('meta', {})
    meta['limit'] = LIMIT
    meta['offset'] = offset
    meta['total'] = total
    meta['next'] = get_next('journals', meta['total'], meta['limit'], int(meta['offset']))
    meta['previous'] = get_previous('journals', meta['total'], meta['limit'], int(meta['offset']))

    records = request.db.find(
        query,
        {"_id": 0},
        limit=LIMIT,
        skip=offset,
        sort=[('total', -1)]
    )

    rdata['objects'] = [i for i in records]

    return rdata

@view_config(route_name='issue', request_method='GET', renderer='json')
def issue(request):
    code = request.matchdict.get('code', None)

    query = {'type': 'issue'}

    if REGEX_ISSUE.search(code):
        query['code'] = code
    else:
        raise httpexceptions.HTTPBadRequest('Invalid ISSUE CODE %s' % code)

    record = request.db.find_one(query, {"_id": 0})

    return record

@view_config(route_name='articles', request_method='GET', renderer='json')
def articles(request):
    offset = int(request.GET.get('offset', 0))
    rdata = {}
    total = None
    query = {'type': 'article'}

    total = request.db.find(query).count()

    if offset > total or offset < 0:
        raise httpexceptions.HTTPBadRequest('offset exceeded the range [0, %s]' % str(total))

    meta = rdata.setdefault('meta', {})
    meta['limit'] = LIMIT
    meta['offset'] = offset
    meta['total'] = total
    meta['next'] = get_next('journals', meta['total'], meta['limit'], int(meta['offset']))
    meta['previous'] = get_previous('journals', meta['total'], meta['limit'], int(meta['offset']))

    records = request.db.find(
        query,
        {"_id": 0},
        limit=LIMIT,
        skip=offset,
        sort=[('total', -1)]
    )

    rdata['objects'] = [i for i in records]

    return rdata

@view_config(route_name='article', request_method='GET', renderer='json')
def article(request):
    code = request.matchdict.get('code', None)

    query = {'type': 'article'}

    if REGEX_ARTICLE.search(code) or REGEX_FBPE.search(code):
        query['code'] = code
    else:
        raise httpexceptions.HTTPBadRequest('Invalid ARTICLE CODE %s' % code)

    record = request.db.find_one(query, {"_id": 0})

    return record
