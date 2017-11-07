import psycopg2
import random

RETAILERS = [
    'Buffalo Wild Wings',
    'Chipotle',
    'Red Robin',
    'OReilly',
]

retailer = 'Chipotle'
ids = []

try:
    conn = psycopg2.connect("dbname='datastore' user='panelists' host='panelists1.cxanyskfu563.us-west-1.rds.amazonaws.com' password='GtF4qK2l9SWbMD87'")
except:
    print "I am unable to connect to the database"
cur = conn.cursor()

def build_mass_insert_query(ids, cohort_id=1):
    # Cohort ID is hard set to 1 right now
    i = "INSERT INTO panelist_cohorts (cohort_id, panelist_id) VALUES "
    values = []
    for panelist_id in ids:
        values.append("(" + str(cohort_id) + ",  " + str(panelist_id) + ")")
    return i + ",".join(values) + ";"

def gen_random_cohort(count=20001):
    cur.execute("""SELECT panelist_id from panelist_stats WHERE is_valid=true""")
    rows = cur.fetchall()
    ids = set()
    for row in rows:
        #print "   ", row[0], row[1], row[2]
        ids.add(row[0])

    ids_list = list(ids)
    random.shuffle(ids_list)
    return ids_list[0:count]

def build_statement(retailer, q_start, q_end, ids, t='transactions'):
    statement = ''
    if t == 'transactions':
        statement = """SELECT count(*) from transactions WHERE \
        is_valid=True AND \
        retailer=""" + "'" + retailer + "'" + " AND " + \
        """ transaction_date >= '""" + q_start + "' AND transaction_date <='" + q_end + "' AND " + \
        """ panelist_id IN (""" + ",".join(str(x) for x in ids) + """)"""
    elif t == 'basket_total':
        statement = """SELECT sum(basket_total) from transactions WHERE \
        is_valid=True AND \
        retailer=""" + "'" + retailer + "'" + " AND " + \
        """ transaction_date >= '""" + q_start + "' AND transaction_date <='" + q_end + "' AND " + \
        """ panelist_id IN (""" + ",".join(str(x) for x in ids) + """)"""
    return statement

# years = ['2015', '2016', '2017']
# q1 = ['01-01','03-31']
# q2 = ['04-01','06-30']
# q3 = ['07-01','09-30']
# q4 = ['08-01','12-31']
# quarters = [q1,q2,q3,q4]
# q_start = quarter[0] + '-' + year
#   q_end = quarter[1] + '-' + year
quarter_mapping = {
    '4Q2015': ['08-01-2015', '12-31-2015'],
    '1Q2016': ['01-01-2016', '03-31-2016'],
    '2Q2016': ['04-01-2016', '06-30-2016'],
    '3Q2016': ['07-01-2016', '09-30-2016'],
    '4Q2016': ['10-01-2016', '12-31-2016'],
    '1Q2017': ['01-01-2017', '03-31-2017'],
    '2Q2017': ['04-01-2017', '06-30-2017'],
    '3Q2017': ['07-01-2017', '09-30-2017']
}

def cal_trans(retailer):
    current_cohort_stats = {}
    ids = gen_random_cohort()

    print ids[0:10]

    for k in quarter_mapping:
        q_start = quarter_mapping[k][0]
        q_end = quarter_mapping[k][1]
        print "quarter: ", q_start, q_end
        current_cohort_stats[k] = {}
        statement = build_statement(retailer, q_start, q_end, ids, t='transactions')

        cur.execute(statement)
        rows = cur.fetchall()
        for row in rows:
            print "transaction", row[0]
            current_cohort_stats[k]['transactions'] = row[0]

        statement = build_statement(retailer, q_start, q_end, ids, t='basket_total')

        cur.execute(statement)
        rows = cur.fetchall()
        for row in rows:
            # print "basket_total: ", row[0]
            current_cohort_stats[k]['basket_total'] = row[0]
        # print
    return current_cohort_stats

# pick random group of 20k to 30k
#print len(gen_random_cohort())
#print cal_trans()
# test_data = {}
# for retailer in RETAILERS:
#     test_data[retailer] = cal_trans(retailer)

test_data = cal_trans(retailer)

# print test_data
# test_data = {'3Q2017': {'basket_total': 205836.0, 'transactions': 6219L}, '3Q2016': {'basket_total': 177637.0, 'transactions': 5731L}, '4Q2016': {'basket_total': 204729.0, 'transactions': 6277L}, '4Q2015': {'basket_total': 138098.0, 'transactions': 4110L}, '2Q2016': {'basket_total': 166282.0, 'transactions': 5230L}, '2Q2017': {'basket_total': 208228.0, 'transactions': 6424L}, '1Q2017': {'basket_total': 212621.0, 'transactions': 6846L}, '1Q2016': {'basket_total': 176936.0, 'transactions': 5743L}}

ALL_QUARTERS = [
    '4Q2015',
    '1Q2016',
    '2Q2016',
    '3Q2016',
    '4Q2016',
    '1Q2017',
    '2Q2017',
    '3Q2017'
]

actual_results_mapping = {
    'Buffalo Wild Wings': {
            '4Q2015': {},
            '1Q2016': {},
            '2Q2016': {},
            '3Q2016': {},
            '4Q2016': {},
            '1Q2017': {},
            '2Q2017': {},
            '3Q2017': {},
        },
    'Red Robin': {
            '4Q2015': {},
            '1Q2016': {},
            '2Q2016': {},
            '3Q2016': {},
            '4Q2016': {},
            '1Q2017': {},
            '2Q2017': {},
            '3Q2017': {},
        },
    'OReilly': {
            '4Q2015': {},
            '1Q2016': {},
            '2Q2016': {},
            '3Q2016': {},
            '4Q2016': {},
            '1Q2017': {},
            '2Q2017': {},
            '3Q2017': {},
        },
    'Chipotle': {
            '4Q2015': {},
            '1Q2016': {},
            '2Q2016': {},
            '3Q2016': {},
            '4Q2016': {},
            '1Q2017': {},
            '2Q2017': {},
            '3Q2017': {},
        }
    }

# Retrieve Real Data

for retailer in RETAILERS:
    cur.execute("""SELECT quarter, yy_sales_growth, seq_sales_growth, comp_store_sales, yy_absolute_seq_change_comp_store_sales from actual_results WHERE retailer='""" + retailer + "'")
    rows = cur.fetchall()
    for row in rows:
        actual_results_mapping[retailer][row[0]]['quarter'] = row[0]
        actual_results_mapping[retailer][row[0]]['yy_sales_growth'] = row[1]
        actual_results_mapping[retailer][row[0]]['seq_sales_growth']= row[2]
        actual_results_mapping[retailer][row[0]]['comp_store_sales'] = row[3]
        actual_results_mapping[retailer][row[0]]['yy_absolute_seq_change_comp_store_sales']= row[4]
    # print "yy_sales_growth", row[0], row[1]

# Then calculate all of the metrics
# (Y/Y sales growth,
#     seq sales growth,
#     and sequential change in y/y sales growth)
def yy_sales_growth(retailer):
    # yy_sales_growth (this year - last year) / last year
    # sales_growth is basket_total
    # [this year, last year]
    sequence = [
        ['4Q2016', '4Q2015'],
        ['1Q2017', '1Q2016'],
        ['2Q2017', '2Q2016'],
        ['3Q2017', '3Q2016']
    ]
    result = {}

    # Retrieval Calculated Data
    # print 'quarter', 'yy_sales_growth'
    for s in sequence:
        result[s[0]] = {}
        this_year = test_data[s[0]]['basket_total']
        last_year = test_data[s[1]]['basket_total']
        calculated = (this_year - last_year)/last_year
        result[s[0]]['calculated'] = calculated
        # print s[0], calculated

    sum_of_diff = 0

    # Look at Diff
    # print 'quarter', 'diff'
    for s in sequence:
        this_year = test_data[s[0]]['basket_total']
        last_year = test_data[s[1]]['basket_total']
        calculated = (this_year - last_year)/last_year
        # print actual_results_mapping[retailer]
        # print actual_results_mapping[retailer][s[0]]
        if actual_results_mapping[retailer][s[0]] == {}:
            continue
        actual = actual_results_mapping[retailer][s[0]]['yy_sales_growth']
        if actual != None:
            diff = calculated - actual
        result[s[0]]['actual'] = actual
        result[s[0]]['diff'] = diff
        # print s[0], diff
        sum_of_diff += abs(diff)

    # print "sum of abs diff: " + str(sum_of_diff)
    return result

#TODO:
# wrong
# start with seq comp yy
# should be only 2 numbers
# looks at change of sales
# if Q1 -> Q2 change is -4 and Q2->Q3 change is -1, then seq is -1 - -4 = +3
def seq_sales_growth(retailer):
    # seq_sales_growth: (this quarter - last quarter) / last quarter
    #

    # sales_growth is basket_total
    # [this year, last year]
    sequence = [
        ['1Q2016','4Q2015'],
        ['2Q2016','1Q2016'],
        ['3Q2016','2Q2016'],
        ['4Q2016','3Q2016'],
        ['1Q2017','4Q2016'],
        ['2Q2017','1Q2017'],
        ['3Q2017','2Q2017']
    ]

    result = {}

    # Retrieval Calculated Data
    # print 'quarter', 'yy_sales_growth'
    for s in sequence:
        result[s[0]] = {}
        this_year = test_data[s[0]]['basket_total']
        last_year = test_data[s[1]]['basket_total']
        calculated = (this_year - last_year)/last_year
        result[s[0]]['calculated'] = calculated
        # print s[0], calculated

    sum_of_diff = 0

    # Look at Diff
    # print 'quarter', 'diff'
    for s in sequence:
        this_year = test_data[s[0]]['basket_total']
        last_year = test_data[s[1]]['basket_total']
        calculated = (this_year - last_year)/last_year
        actual = actual_results_mapping[retailer][s[0]]['yy_sales_growth']
        if actual != None:
            diff = calculated - actual
        result[s[0]]['actual'] = actual
        result[s[0]]['diff'] = diff
        # print s[0], diff
        sum_of_diff += abs(diff)

    # print "sum of abs diff: " + str(sum_of_diff)
    return result


def yy_seq_sales_growth(retailer):
    # sequential change in y/y sales growth

    yy_sales = yy_sales_growth(retailer)

    # print "yy_sales"
    # print yy_sales

    sequence = [
            # ['1Q2017','4Q2016'],
            # ['2Q2017','1Q2017'],
            # ['3Q2017','2Q2017']
            ['4Q2016'],
            ['1Q2017'],
            ['2Q2017'],
        ]

    result = {}

    
    Q12017 = yy_sales['1Q2017']['calculated'] - yy_sales['4Q2016']['calculated']
    Q22017 = yy_sales['1Q2017']['calculated'] - yy_sales['2Q2017']['calculated']

    return Q12017 + Q22017

    # # Retrieval Calculated Data
    # # print 'quarter', 'yy_seq_sales_growth'
    # for s in sequence:
    #     result[s[0]] = {}
    #     this_quarter = yy_sales[s[0]]['calculated']
    #     last_quarter = yy_sales[s[1]]['calculated']

    #     # calculated = (this_year - last_year)/last_year
    #     # result[s[0]]['calculated'] = calculated
    #     # print s[0], calculated

    # sum_of_diff = 0

    # # Look at Diff
    # # print 'quarter', 'diff'
    # for s in sequence:
    #     this_year = test_data[s[0]]['basket_total']
    #     last_year = test_data[s[1]]['basket_total']
    #     calculated = (this_year - last_year)/last_year
    #     actual = actual_results_mapping[retailer][s[0]]['yy_sales_growth']
    #     if actual != None:
    #         diff = calculated - actual
    #     result[s[0]]['actual'] = actual
    #     result[s[0]]['diff'] = diff
    #     # print s[0], diff
    #     sum_of_diff += abs(diff)

    # print "sum of abs diff: " + str(sum_of_diff)
    # return result
    # comp_store_sales: (this year - last year) / last year
    # sales_growth is basket_total
    # [this year, last year]
    # sequence = [
    #     ['4Q2016', '4Q2015'],
    #     ['1Q2017', '1Q2016'],
    #     ['2Q2017', '2Q2016'],
    #     ['3Q2017', '3Q2016']
    # ]

    # # Retrieval Calculated Data
    # print 'quarter', 'yy_sales_growth'
    # for s in sequence:
    #     this_year = test_data[s[0]]['basket_total']
    #     last_year = test_data[s[1]]['basket_total']
    #     calculated = (this_year - last_year)/last_year
    #     print s[0], calculated

    # sum_of_diff = 0

    # # Look at Diff
    # print 'quarter', 'diff'
    # for s in sequence:
    #     this_year = test_data[s[0]]['basket_total']
    #     last_year = test_data[s[1]]['basket_total']
    #     calculated = (this_year - last_year)/last_year
    #     actual = actual_results_mapping[retailer][s[0]]['yy_sales_growth']
    #     if actual != None:
    #         diff = calculated - actual
    #     print s[0], diff
    #     sum_of_diff += abs(diff)

    # print sum_of_diff
# '4Q2015': ['08-01-2015', '12-31-2015'],
# '1Q2016': ['01-01-2016', '03-31-2016'],
# '2Q2016': ['04-01-2016', '06-30-2016'],
# '3Q2016': ['07-01-2016', '09-30-2016'],
# '4Q2016': ['10-01-2016', '12-31-2016'],
# '1Q2017': ['01-01-2017', '03-31-2017'],
# '2Q2017': ['04-01-2017', '06-30-2017'],
# '3Q2017': ['07-01-2017', '09-30-2017']
# yy_sales_growth: (this year - last year) / last year
#
# seq_sales_growth: yy_sales_growth change
#
# comp_store_sales: (this year - last year) / last year
#
# yy_absolute_seq_change_comp_store_sales
#
# yy_relative_seq_change_comp_store_sales

# write to a file
# print('yy_sales_growth')
# print(yy_sales_growth(retailer))
# print("\n")
#print('seq_sales_growth')
#print(seq_sales_growth(retailer))
#print("\n")

cur.execute("""SELECT seq_sales_error FROM successful_cohorts WHERE cohort_id=1""")

current_seq_growth_error_margin = 1
calculated_seq_growth_error_margin = yy_seq_sales_growth(retailer)
print('yy_seq_sales_growth')
print(calculated_seq_growth_error_margin)
print(abs(calculated_seq_growth_error_margin))
print abs(calculated_seq_growth_error_margin) < current_seq_growth_error_margin
if abs(calculated_seq_growth_error_margin) < current_seq_growth_error_margin:

    cur.execute("""DELETE FROM panelist_cohorts WHERE cohort_id=1""")
    cur.execute(build_mass_insert_query(ids, cohort_id=1))
