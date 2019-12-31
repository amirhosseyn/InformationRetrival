from django.shortcuts import render
from django.core.paginator import Paginator
from . import ss
from . import searchclass
import time
import simplejson as json
NORESULT = "Nothing ..."
TIME=0

def homepage(request):
    return render(request, 'home.html')


def search(request):
    print(request.GET['select'])
    query=request.GET['search']
    qu = searchclass.Query(query)
    docids = qu.final_results()
    but_num=len(docids)/10
    but_num=int(but_num) + 1
    butts=[]
    for i in range(but_num):
        butts.append(i + 1)
    results = ss.query(docids)
    for key in results:
        key['doc_number'] = int(key['doc_number'])
    # t2=time.time_ns()
    if docids:
        info = f"Found {len(docids)} results in {(1)/10**6 } miliseconds"
    else:
        info = NORESULT
    print(results[0])
    return render(request, 'search.html', {'lists': json.dumps(results), 'info' : info,'query':query,'buttons':butts})

# def viewresults(request):



def func(request, id):
    temp=ss.urls[id-1]
    return render(request, 'content.html', {'list': temp})
