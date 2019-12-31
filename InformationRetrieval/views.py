from django.shortcuts import render
from django.core.paginator import Paginator
from . import ss
from . import searchclass
import time
import simplejson as json
NORESULT = "Nothing ..."
def homepage(request):
    return render(request, 'home.html')


def search(request):
    print(request.GET['select'])
    query=request.GET['search']
    qu = searchclass.Query(query)
    docids = qu.final_results()
    #Change Query list here!
    query_list=["سلام","محمد","تهران"]
    query_list=json.dumps(query_list)
    results = ss.query(docids)
    for key in results:
        key['doc_number'] = int(key['doc_number'])
    # t2=time.time_ns()
    if docids:
        info = f"Found {len(docids)} results in {(1)/10**6 } miliseconds"
    else:
        info = NORESULT
    return render(request, 'search.html', {'lists': json.dumps(results), 'info' : info,'query':query_list})

# def viewresults(request):



def func(request, id):
    temp=ss.urls[id-1]
    print(query_list)
    return render(request, 'content.html', {'list': temp,'query':query_list})
