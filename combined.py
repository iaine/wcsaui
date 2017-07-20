'''
   Create two named graph
'''
import json

from sparqldao import SparqlDao
from file_ops import FileOps
from similarity import Similarities

class JoinGraph:

    def __init__(self, endpoint):
        self.endpoint = endpoint

    def deduplicate_data(self, a, b):
        '''
           Deduplicating data
        '''
        return list(set(a) - set(b))

    def calculate_similarity_perc(self, lista, listb):
        '''
            Return similarities. Useful for filtering
        '''
        return float(len(lista))/float(len(listb))

    def get_data_list(self, sparql_file, searchstr):
        qry_string = FileOps().open(sparql_file).format(searchstr)
        data = sd.run_remote_sparql(self.endpoint, qry_string)
        return data 

    def join_graphs(self, graph):
        merged_data = []

        original = []
        sd = SparqlDao()
        
        qry_string = FileOps().open('query/original_author.rq') 
        qry_string = qry_string.format(graph)
        original = sd.run_remote_sparql(self.endpoint, qry_string)

        #get the other graphs linked by VIAF
        qry_string = FileOps().open('query/walk_path_query.rq')
        qry_string = qry_string.format(graph)

        merged_data = sd.run_remote_sparql(self.endpoint, qry_string)

        link = []
        unlink = []
        for merge in merged_data:
            for orig in original:
                if orig[2] == merge[2] and orig[1] == merge[1]:
                    link.append(merge)

            if merge[1] not in link:
                unlink.append(merge)

        return json.dumps({"original":original,"link":link,"difference":self.deduplicate_data(unlink,link),"similarity":self.calculate_similarity_perc(link,original)})

    def search_data(self, term):
        '''
           Perform substring search on data and return JSON
        '''
        original = []
        sd = SparqlDao()

        qry_string = FileOps().open('query/search_string.rq')
        qry_string = qry_string.format(term)
        original = sd.autocomplete_sparql(self.endpoint, qry_string)

        terms  = []
        for data in original:
            terms.append({'id': data[0], 'value': data[1]})

        return json.dumps(terms)

    def search_predicates(self, searchterm):
        '''
          Find predicates associated with an object. 
        '''
        original = []
        sd = SparqlDao()
        simil = Similarities()

        qry_string = FileOps().open('query/search_predicates.rq')
        qry_string = qry_string.format(term)
        original = sd.run_remote_sparql(self.endpoint, qry_string)
        
        props = defaultdict(int)
        all_docs = 0
        for merge in original:
            props[merge[1]] += 1
            
        return json.dumps(props)
