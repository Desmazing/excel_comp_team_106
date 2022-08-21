import os
from django.shortcuts import render,redirect
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import pandas as pd
from dashboard import comp_code


@login_required
def download(request):

    
    name = request.session.get('game')
    name2 = request.session.get('came')
    C = request.session.get('stay')
    D = request.session.get ('hay')
    g = request.session.get('ana')
    number = request.session.get ('num')
    diff, sim = number

    if request.method == 'POST':
        dat = request.POST
        action = dat.get("down")
        if action == "download":
            file_path = os.path.join(settings.MEDIA_ROOT, name)
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        if action == "download2":
            file_path = os.path.join(settings.MEDIA_ROOT, name2)
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
    
    return render(request, "dash/result.html", {"first":C, "second":D, "analysis":g, "diff":diff,"sim":sim, "name1":name,"name2":name2})

@login_required
def result_view(request):

    if request.method == 'POST':
        
        file1=request.FILES['file_one']
        file2=request.FILES['file_two']

        data = request.POST
        action = data.get("criteria")
        compare = data.get("compare")

        name = '{}'.format(file1)
        name2 = '{}'.format(file2)

        fileA = pd.read_excel(file1)
        fileB = pd.read_excel(file2)
        fileI = pd.read_excel(file1)
        fileII = pd.read_excel(file2) 

        f,z=[],[]
        for i, j in zip(fileA,fileB):
            a,b = 0,0
            a,b = [],[]
            for m,n in zip(fileA[i],fileB[j]):
                a.append(m)
                b.append(n)
            for m,n in zip(range(len(a)),range(len(b))):
                if a[m] != b[n]:
                    z.append(a[m])
                if a[m] == b[n]:
                    f.append(a[m])
                
        number = len(z), len(f)
        request.session['num'] = number

        if action == "highlight":
            ask = "not"
            fileA,fileB = comp_code.high(fileA,fileB, ask),comp_code.high(fileII,fileI, ask)
        
            A = fileA.style.applymap(comp_code.highlight_cells)
            B = fileB.style.applymap(comp_code.highlight_cells)
    
            A = comp_code.color(A)
            B = comp_code.color(B)

            C = A.to_html(index=False)
            D = B.to_html(index=False)

            z=[]
            for i, j in zip(fileA,fileB):
                 a,b = 0,0
                 a,b = [],[]
                 for m,n in zip(fileA[i],fileB[j]):
                    a.append(m)
                    b.append(n)
                 for m,n in zip(range(len(a)),range(len(b))):
                    if a[m] != b[n]:
                        z.append("Value in {};  Column: {}, Row: {}, was changed from {} to {}".format(name,i,m,a[m],b[n]))
            g = z

            file_pathA = os.path.join(settings.MEDIA_ROOT, name)
            A.to_excel(file_pathA,index = False, header = True, engine = 'openpyxl')
            file_pathB = os.path.join(settings.MEDIA_ROOT, name2)
            B.to_excel(file_pathB,index = False, header = True, engine = 'openpyxl')

            request.session['game'] = name
            request.session['came'] = name2
            request.session['stay'] = C
            request.session['hay'] = D
            request.session['ana'] = g

            return redirect("result")

        if action == 'merge':
            ask = "merge"
            fileA = comp_code.high(fileA,fileB, ask)
        
            A = fileA.style.applymap(comp_code.highlight_cells)
    
            A = comp_code.color(A)
            C = A.to_html(index=False)

            z=[]
            for i, j in zip(fileA,fileB):
                 a,b = 0,0
                 a,b = [],[]
                 for m,n in zip(fileA[i],fileB[j]):
                    a.append(m)
                    b.append(n)
                 for m,n in zip(range(len(a)),range(len(b))):
                    if a[m] != b[n]:
                        z.append("Value in {};  Column: {}, Row: {}, was changed from {}".format(name,i,m,a[m]))
            g = z

            file_pathA = os.path.join(settings.MEDIA_ROOT, name)
            A.to_excel(file_pathA,index = False, header = True, engine = 'openpyxl')

            request.session['game'] = name
            request.session['stay'] = C
            request.session['ana'] = g 

            return redirect("result")

        elif action == "remove":
            fileA,fileB = comp_code.rem(fileA,fileB),comp_code.rem(fileII,fileI)
        
            A = fileA.style.applymap(comp_code.remove_cells)
            B = fileB.style.applymap(comp_code.remove_cells)

            A = comp_code.color(A)
            B = comp_code.color(B)
    
            C = A.to_html(index=False)
            D = B.to_html(index=False)

            z=[]
            for i, j in zip(fileA,fileB):
                 a,b = 0,0
                 a,b = [],[]
                 for m,n in zip(fileA[i],fileB[j]):
                    a.append(m)
                    b.append(n)
                 for m,n in zip(range(len(a)),range(len(b))):
                    if a[m] != b[n]:
                        z.append("Value in {};  Column: {}, Row: {}, was changed from {} to {}".format(name,i,m,a[m],b[n]))
            g = z
            
            file_pathA = os.path.join(settings.MEDIA_ROOT, name)
            fileA.to_excel(file_pathA,index = False, header = True, engine = 'openpyxl')
            file_pathB = os.path.join(settings.MEDIA_ROOT, name2)
            fileB.to_excel(file_pathB,index = False, header = True, engine = 'openpyxl')

            request.session['game'] = name
            request.session['came'] = name2
            request.session['stay'] = C
            request.session['hay'] = D
            request.session['ana'] = g

            return redirect("result")

    return render(request, "index.html")



def contactview(request):
    return render(request, "dash/contact.html")
    

def aboutusview(request):
    return render(request, "dash/aboutus.html")


def policyview(request):
    return render(request, "dash/privacypolicy.html")
    





    


    
    
        
        
        
        
        
