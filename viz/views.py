import mimetypes
from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import re

from .server import server
def clean_dash_content(dash_content):
    ''' This is a hack to get rid of carriage returns in the html returned by the call to dash_dispatcher'''
    print("Function: clean_dash_content")

    string_content = str(dash_content)
    string_content = string_content.replace("\\n   ", "")
    string_content = string_content.replace("\\\\n", "")
    string_content = string_content.replace("\\\'", "")
    string_content = string_content.replace(">\\n<", "><")
    string_content = string_content[:-6]
    string_content = string_content[1:]
    string_content = re.sub('\s+',' ', string_content)
    string_content = string_content[1:]
    cleaned_dash_content = string_content

    return cleaned_dash_content

def home(request):
    return render(request,'viz/home.html')



def dispatcher(request):
    '''
    Main function
    @param request: Request object
    '''

    params = {
        'data': request.body,
        'method': request.method,
        'content_type': request.content_type
    }
    with server.test_request_context(request.path, **params):
        server.preprocess_request()

        try:
            response = server.full_dispatch_request()
        except Exception as e:
            response = server.make_response(server.handle_exception(e))

        response.direct_passthrough = False
        return response.get_data()


@csrf_exempt
def dash_json(request, **kwargs):
    """Handle Dash JSON API requests"""
    print(request.get_full_path())
    return HttpResponse(dispatcher(request), content_type='application/json')

'''
def dash_index(request, **kwargs):
    """Handle Dash CSS requests"""
    return HttpResponse(dispatcher(request), content_type='text/html')
'''
def dash_index(request, **kwargs):
    """Handle Dash CSS requests"""
    dash_content=HttpResponse(dispatcher(request), content_type='text/html').getvalue()
    content={'dash_content':dash_content}
    return render(request,'viz/dash.html',content)


def dash_guess_mimetype(request, **kwargs):
    """Handle Dash requests and guess the mimetype. Needed for static files."""
    url = request.get_full_path().split('?')[0]
    content_type, _encoding = mimetypes.guess_type(url)
    return HttpResponse(dispatcher(request), content_type=content_type)
