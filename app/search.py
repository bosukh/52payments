import logging

from .models import Company
from .memcache import mc_getsert

def parse_search_criteria(search_criteria):
    '''
    Search criteria comes in as a list of <Category>: <Characteristic>
    ex) ['Business_Types: Retail', 'Pricing_Methods: Flat']
    '''
    search_criteria = search_criteria.split(',')
    search_criteria = map(lambda x: x.split(': '),search_criteria)
    temp = {}
    for k, v in search_criteria:
        if k in temp.keys():
            temp[k] += [v]
        else:
            temp[k] = [v]
    logging.debug(temp)
    return temp

def company_search_query(search_criteria):
    types = [('Business_Types', 'provided_srvs'),
             ('Complementary_Services', 'complementary_srvs'),
             ('Terminals', 'equipment'),
             ('Pricing_Methods', 'pricing_method')]
    gql_query = "WHERE "
    where_clause = []
    for col, col_name in types:
        criteria = search_criteria.get(col)
        if criteria:
            for value in criteria:
                where_clause.append("%s = '%s'"%(col_name, value))
    gql_query += ' AND '.join(where_clause) + " ORDER BY share DESC"
    logging.debug(gql_query)
    res =  Company.gql(gql_query).fetch()
    logging.debug('Query Resulted in %s'%str(len(res)))
    return res

def search_company(search_criteria):
    if not search_criteria:
        logging.debug('Search Returning all comapnies')
        return mc_getsert('all_verified_companies', Company.make_query("ORDER BY share DESC"))
    search_result = company_search_query(parse_search_criteria(search_criteria))
    return search_result
