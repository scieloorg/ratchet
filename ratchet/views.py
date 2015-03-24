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
    collection = request.GET.get('collection', None)
    offset = int(request.GET.get('offset', 0))

    if type_doc and not type_doc in ALLOWED_TYPE_DOCS:
        raise httpexceptions.HTTPBadRequest('expected type invalid, not in range %s' % str(ALLOWED_TYPE_DOCS))

    try:
        data = request.controller.general(
            type_doc=type_doc,
            collection=collection,
            code=code,
            limit=LIMIT,
            offset=offset
        )
    except:
        raise httpexceptions.HTTPInternalServerError('Fail to connect to database')

    return data

@view_config(route_name='general', request_method='POST')
@authenticate
def general_post(request):
    code = request.POST.get('code')
    page = request.POST.get('page', None)
    type_doc = request.POST.get('type', None)
    access_date = request.POST.get('access_date', None)
    query = {}

    if type_doc and not type_doc in ALLOWED_TYPE_DOCS:
        raise httpexceptions.HTTPBadRequest('expected type invalid, not in range %s' % str(ALLOWED_TYPE_DOCS))

    query['type'] = type_doc            

    if access_date:
        try:
            datetime.datetime.strptime(access_date, '%Y-%m-%d')
        except ValueError:
            raise httpexceptions.HTTPBadRequest('Invalid ISO Date %s' % access_date)
    else:
        access_date = datetime.date.today().isoformat()

    try:
        request.controller.general_post(code, page, type_doc, access_date)
    except:
        raise httpexceptions.HTTPInternalServerError('Fail to connect to database')


    raise httpexceptions.HTTPCreated

@view_config(route_name='general_bulk', request_method='POST')
@authenticate
def general_bulk(request):
    data = request.POST.get('data', 'No data received')

    try:
        data = json.loads(data)
    except:
        raise httpexceptions.HTTPBadRequest('Invalid JSON')

    if not 'code' in data:
        raise httpexceptions.HTTPBadRequest('Invalid data, code attribute is mandatory')

    try:
        request.controller.general_bulk(data)
    except:
        raise httpexceptions.HTTPInternalServerError('Fail to connect to database')


    raise httpexceptions.HTTPCreated

@view_config(route_name='journals', request_method='GET', renderer='json')
def journals(request):
    offset = int(request.GET.get('offset', 0))
    collection = request.matchdict.get('collection', None)

    try:
        data = request.controller.journals(collection=collection, limit=LIMIT, offset=offset)
    except:
        raise httpexceptions.HTTPInternalServerError('Fail to connect to database')

    return data

@view_config(route_name='journal', request_method='GET', renderer='json')
def journal(request):
    code = request.matchdict.get('code', None)
    

    if not REGEX_ISSN.search(code):
        raise httpexceptions.HTTPBadRequest('Invalid ISSN CODE %s' % code)

    try:
        record = request.controller.journal(code)
    except:
        raise httpexceptions.HTTPInternalServerError('Fail to connect to database')

    return record

@view_config(route_name='issues', request_method='GET', renderer='json')
def issues(request):
    offset = int(request.GET.get('offset', 0))
    collection = request.matchdict.get('collection', None)

    try:
        data = request.controller.issues(collection=collection, limit=LIMIT, offset=offset)
    except:
        raise httpexceptions.HTTPInternalServerError('Fail to connect to database')

    return data

@view_config(route_name='issue', request_method='GET', renderer='json')
def issue(request):
    code = request.matchdict.get('code', None)

    if not REGEX_ISSUE.search(code):
        raise httpexceptions.HTTPBadRequest('Invalid ISSUE CODE %s' % code)

    try:
        record = request.controller.issue(code)
    except:
        raise httpexceptions.HTTPInternalServerError('Fail to connect to database')

    return record

@view_config(route_name='articles', request_method='GET', renderer='json')
def articles(request):
    offset = int(request.GET.get('offset', 0))
    collection = request.matchdict.get('collection', None)

    try:
        data = request.controller.articles(collection=collection, limit=LIMIT, offset=offset)
    except:
        raise httpexceptions.HTTPInternalServerError('Fail to connect to database')

    return data

@view_config(route_name='article', request_method='GET', renderer='json')
def article(request):
    code = request.matchdict.get('code', None)

    if REGEX_ARTICLE.search(code) or REGEX_FBPE.search(code):
        record = request.controller.article(code)
    else:
        raise httpexceptions.HTTPBadRequest('Invalid ARTICLE CODE %s' % code)

    return record
