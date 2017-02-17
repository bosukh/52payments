import logging

from .models import Company
from .memcache import mc_getsert

def parse_search_criteria(search_criteria):
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
    types = [('Business_Type', 'provided_srvs'),
             ('Complimentary_Service', 'complementary_srvs'),
             ('Terminal', 'equipment'),
             ('Pricing_Method', 'pricing_method')]
    gql_query = "WHERE "
    where_clause = []
    for col, col_name in types:
        criteria = search_criteria.get(col)
        if criteria:
            for value in criteria:
                where_clause.append("%s = '%s'"%(col_name, value))
            #where_clause.append("%s IN (%s)"%(col_name, "'" + "', '".join(criteria) + "'"))
    gql_query += ' AND '.join(where_clause) + " ORDER BY share DESC"
    logging.debug(gql_query)
    res =  Company.gql(gql_query).fetch()
    logging.debug('Query Resulted in %s'%str(len(res)))
    return res

def search_company(search_criteria):
    if not search_criteria:
        logging.debug('Search Returning all comapnies')
        return mc_getsert('all_verified_companies', Company.gql("ORDER BY share DESC").fetch)
    search_criteria = parse_search_criteria(search_criteria)
    search_result = company_search_query(search_criteria)
    for company in search_result:
        company.avg_rating = round(company.avg_rating, 1)
        #session['search_criteria'] = search_criteria
    return search_result
