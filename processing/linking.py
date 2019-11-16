import os
from shutil import copyfile
from win32api import (MessageBeep, MessageBox)

# временно 
from interface.mainUi import MainUi

def make_dist(restored, form):
    """ creates the main directory of the application.
        
        Keyword arguments:
            restored -> all restored data
            form -> completed form
    
        return (static_path, dynamic_path, payment_path)
        
    """

    general = restored['general']
    collected_path = '/%s/%s/%s/Торг №%s'%\
        (form['method'], form['name'], form['category'], form['regnumber'])

    full_path = '{}{}'.format(general['mainPath'], collected_path)

    path_model = restored['pathModel']
    static_path = '%s/%s' % (full_path, path_model['staticPath'])
    dynamic_path = '%s/%s' % (full_path, path_model['dynamicPath'])
    
    if form['calculation']: # расчет
        payment_name = 'Расчет %s(%s).xlsx' % (form['name'], form['category'])
        payment_path = '%s/%s/%s' %\
                        (full_path, path_model['payment'], payment_name)
        payment_path = payment_path.replace('//', '/')
    else: 
        payment_path = False


    try:
        os.makedirs(static_path)
        os.makedirs(dynamic_path)
    except FileExistsError:
        pass

    for link in restored['pathModel']['otherPaths']:
        path = '%s/%s' % (full_path, link)
        try:
            os.makedirs(path)
        except FileExistsError:
            pass

    
    return (static_path, dynamic_path, full_path, payment_path)

def make_static_srcs(docs, form):
    """ Create static files paths from Doc List and Form data.
        
        Keyword arguments:
            docs -> [{}] list of all attached documents
            form -> completed form
        
    """
    paths = []
    for doc in docs:
        if doc['law'] == form['law']:
            if doc['method'] == form['method']:
                if doc['checked']:
                    paths.append(doc['dir'])
    return paths


def push_files(dist, static_files, dynamic_files, payment):
    """ copies Files from sources to dists.
        
        Keyword arguments:
            dist, static_files, dynamic_files
    """
    static_dist = dist[0]
    dynamic_dist = dist[1]
    payment_dist = dist[-1]

    links = []
    for file in static_files:
        name = os.path.basename(file)
        path = '%s/%s' % (static_dist, name)
        copyfile( file, path )
        if not path in links:
            links.append(path)
    
    for file in dynamic_files:
        name = os.path.basename(file)
        path = '%s/%s' % (dynamic_dist, name)
        copyfile( file, path )
        if not path in links:
            links.append(path)

    if payment_dist:
        print(payment)
        copyfile(payment, payment_dist)
        links.append(payment_dist)

    return links