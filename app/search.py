from .models import Company

def parse_search_criteria(search_criteria):
    search_criteria = search_criteria.split(',')
    search_criteria = map(lambda x: x.split(': '),search_criteria)
    temp = {}
    for k, v in search_criteria:
        if k in temp.keys():
            temp[k] += [v]
        else:
            temp[k] = [v]
    return temp

def company_search(search_criteria):
    types = [('Business Types', 'provided_srvs'),
             ('Complimentary Services', 'complementary_srvs'),
             ('Equipments', 'equipment'),
             ('Pricing Method', 'pricing_method')]
    gql_query = "WHERE "
    where_clause = []
    for col, col_name in types:
        criteria = search_criteria.get(col)
        if criteria:
            where_clause.append("%s IN (%s)"%(col_name, "'" + "', '".join(criteria) + "'"))
    gql_query += ' AND '.join(where_clause) + " ORDER BY pricing_range ASC"
    return Company.gql(gql_query).fetch()
