import psycopg2
import random
import sys

RETAILERS = [
    'Buffalo Wild Wings',
    'Chipotle',
    'Red Robin',
    'OReilly',
]

# Burlington Coat Factory
# ORLY
# Ulta_OLD
# Five Below
# SBH
# Sprouts Farmers Market

RETAILER = sys.argv[1]
COHORT_ID = int(sys.argv[2])
COHORT_SIZE = int(sys.argv[3])

try:
    conn = psycopg2.connect("dbname='datastore' user='panelists' host='panelists1.cxanyskfu563.us-west-1.rds.amazonaws.com' password='GtF4qK2l9SWbMD87'")
except:
    print "I am unable to connect to the database"
cur = conn.cursor()

def build_mass_insert_query(ids, cohort_id=COHORT_ID):
    print ids[0:10]
    # Cohort ID is hard set to 1 right now
    i = "INSERT INTO panelist_cohorts (cohort_id, panelist_id) VALUES "
    values = []
    for panelist_id in ids:
        values.append("(" + str(cohort_id) + ",  " + str(panelist_id) + ")")
    return i + ",".join(values) + ";"

def gen_random_cohort(count=COHORT_SIZE, cohort_id=COHORT_ID):
    cur.execute("""SELECT panelist_id from panelist_stats WHERE is_valid=true""")
    rows = cur.fetchall()
    ids = set()
    for row in rows:
        #print "   ", row[0], row[1], row[2]
        ids.add(row[0])

    ids_list = list(ids)
    random.shuffle(ids_list)
    return [ids_list[0:count], cohort_id]

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
    ids, cohort_id = gen_random_cohort()

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
    current_cohort_stats['ids'] = ids
    current_cohort_stats['cohort_id'] = cohort_id
    return current_cohort_stats

test_data = cal_trans(RETAILER)
print(test_data)

ALL_QUARTERS = [
    '4Q2015',
    '1Q2016',
    '2Q2016',
    '3Q2016',
    '4Q2016',
    '1Q2017',
    '2Q2017',
    '3Q2017',
    '4Q2017',
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
        },
    'Burlington Coat Factory': {
            '4Q2015': {},
            '1Q2016': {},
            '2Q2016': {},
            '3Q2016': {},
            '4Q2016': {},
            '1Q2017': {},
            '2Q2017': {},
            '3Q2017': {},
        },
    'ORLY': {
            '4Q2015': {},
            '1Q2016': {},
            '2Q2016': {},
            '3Q2016': {},
            '4Q2016': {},
            '1Q2017': {},
            '2Q2017': {},
            '3Q2017': {},
        },
    'Ulta_OLD': {
            '4Q2015': {},
            '1Q2016': {},
            '2Q2016': {},
            '3Q2016': {},
            '4Q2016': {},
            '1Q2017': {},
            '2Q2017': {},
            '3Q2017': {},
        },
    'Five Below': {
            '4Q2015': {},
            '1Q2016': {},
            '2Q2016': {},
            '3Q2016': {},
            '4Q2016': {},
            '1Q2017': {},
            '2Q2017': {},
            '3Q2017': {},
        },
    'SBH': {
            '4Q2015': {},
            '1Q2016': {},
            '2Q2016': {},
            '3Q2016': {},
            '4Q2016': {},
            '1Q2017': {},
            '2Q2017': {},
            '3Q2017': {},
        },
    'Sprouts Farmers Market': {
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
        print('which retailer am i comparing with?')
        print(retailer)
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
    ids = test_data['ids']
    cohort_id = test_data['cohort_id']
    result['ids'] = ids
    result['cohort_id'] = cohort_id
    result['number_of_panelists'] = len(ids)
    return result

#TODO:
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
            ['3Q2017'],
        ]

    Q12017 = yy_sales['1Q2017']['calculated'] - yy_sales['4Q2016']['calculated']
    Q22017 = yy_sales['1Q2017']['calculated'] - yy_sales['2Q2017']['calculated']
    Q32017 = yy_sales['2Q2017']['calculated'] - yy_sales['3Q2017']['calculated']
    ids = yy_sales['ids']
    result = {
        'ids': ids,
        '1Q2017': Q12017,
        '2Q2017': Q22017,
        '3Q2017': Q32017, # predication quarter
        'cohort_id': yy_sales['cohort_id'], 
        'number_of_panelists': len(ids)
    }
    return result


##### 
cohort_id = COHORT_ID
current_seq_growth_error_margin = 99999

# cur.execute("""SELECT seq_sales_error FROM successful_cohorts WHERE cohort_id=""" + str(cohort_id) )
print(RETAILER)
statement = """SELECT seq_sales_error FROM successful_cohorts WHERE retailer='""" + RETAILER + """' ORDER BY seq_sales_error LIMIT 1""" 
print(statement)
cur.execute(statement)
try:
    current_seq_growth_error_margin = cur.fetchone()[0]
    print('found last current_seq_growth_error_margin', current_seq_growth_error_margin)
except:
    print('No successful cohort. seq_sales_error set to 99999')

print('current_seq_growth_error_margin')
print(current_seq_growth_error_margin)
print('retailer')
print(RETAILER)
calculated_seq_growth_error_margin = yy_seq_sales_growth(RETAILER)

ids = calculated_seq_growth_error_margin['ids']
aggregate = calculated_seq_growth_error_margin['1Q2017'] + calculated_seq_growth_error_margin['2Q2017']
cohort_id = calculated_seq_growth_error_margin['cohort_id']
print(cohort_id)
number_of_panelists = calculated_seq_growth_error_margin['number_of_panelists']
seq_sales_error = abs(aggregate)

print('yy_seq_sales_growth')
print(aggregate)
print(abs(aggregate))
print('current_seq_growth_error_margin', current_seq_growth_error_margin)
print('abs(aggregate) < current_seq_growth_error_margin', abs(aggregate) < current_seq_growth_error_margin)
if abs(aggregate) < current_seq_growth_error_margin:
    # cur.execute("""DELETE FROM panelist_cohorts WHERE cohort_id=""" + str(cohort_id))
    # conn.commit()
    # cur.execute("""DELETE FROM successful_cohorts WHERE cohort_id=""" + str(cohort_id))
    # conn.commit()
    statement = """INSERT INTO successful_cohorts (retailer,number_of_panelists,seq_sales_error,created_at) VALUES ('""" +RETAILER+"'," + str(number_of_panelists) + "," + str(seq_sales_error) + ",NOW());"
    # print(statement)
    # cur.execute(statement)
    # conn.commit()
    statement = """SELECT id FROM successful_cohorts WHERE retailer='""" + RETAILER + """' ORDER BY seq_sales_error LIMIT 1""" 
    # print(statement)
    # cur.execute(statement)
    # conn.commit()
    try:
        cohort_id = cur.fetchone()[0]
        print('found last corhort_id', cohort_id)
        # conn.commit()

        # cur.execute(build_mass_insert_query(ids, cohort_id=cohort_id))
        # conn.commit()
        print('next quarter prediction')
        print(calculated_seq_growth_error_margin['3Q2017'])
        next_quarter_prediction = calculated_seq_growth_error_margin['3Q2017']
        statement = "UPDATE successful_cohorts SET seq_sales_prediction=" + str(next_quarter_prediction) + " WHERE id=" + str(cohort_id)
        print(statement)
        # cur.execute(statement)
        # conn.commit()
    except:
        print('No successful cohort. seq_sales_error set to 99999')



# cur.execute("""INSERT INTO successful_cohorts (cohort_id,retailer,number_of_panelists,seq_sales_error) VALUES (1,'foo',20001,999)""");
# conn.commit()
# for idx, retailer in enumerate(RETAILERS):
#     print(idx, retailer)
#     runner(idx, retailer)
