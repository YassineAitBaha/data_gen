#licence MIT 

import numpy as np
import pandas as pd


def random_indexes(arr, rate = 0.1):
    index_of_arr = np.arange(len(arr))
    np.random.shuffle(index_of_arr)
    return index_of_arr[0:int(len(arr)*rate)]

def random_nan(arr, rate = 0.1):
    index_to_nan = random_indexes(arr, rate)
    if arr.dtype == np.int:
        arr = arr.astype('float')
    arr[index_to_nan] = np.nan
    return arr


def generate_random_string(vocab, string_length):

    return " ".join(list(np.random.choice(vocab, string_length)))


def generate_fake_email(n):
    """

    :param n: int number of email to generate
    :return: numpy array of emails
    """
    import faker
    fake = faker.Faker()
    return np.array([fake.email() for i in range(n)])


def format_column_name(col):

    return col.replace(' ', '_')


#mettre if pour is_nan => null (lowercase "nan")
def format_value(v):
    if isinstance(v, (str)):
        v = v.lower()
        if v == "nan":
            value = v.replace("nan", "NULL")
            return str(value)

        value = v.replace("'", "\\'")

        return "'" + str(value) + "'"
    if isinstance(v, np.float) and v is np.nan:
        return 'NULL'
    else:
        return str(v)

def create_table_schema(table_name, df):

    engine = create_engine('mysql+pymysql://', echo=False)

    sql = pd.io.sql.get_schema(df, table_name, con=engine).strip()
    return sql + ";"

def create_table_schemas(tables_names, dfs):

    sql = ""
    for table_name, df in zip(tables_names, dfs):
        sql += create_table_schema(table_name, df) + "\n"

    return sql

def df_to_sql_table(table_name, df):

    schema = create_table_schema(table_name, df)
    inserts = df_to_sql_insert(table_name, df)
    return "{}\n{}".format(schema, inserts)

def df_to_sql_insert(table_name, df):

    inserts = []
    for row in df.to_dict(orient='records'):
        insert = generate_insert_statement(table_name, row)
        inserts.append(insert)

    inserts_str = '\n'.join(inserts)

    return inserts_str + '\n'


def generate_insert_statement(table_name, values_as_dict):

    d = values_as_dict
    columns = ", ".join(list(d.keys()))
    values = ", ".join([format_value(v) for v in d.values()])

    s = "INSERT INTO {} ({}) VALUES ({});".format(table_name, columns, values)
    return s


def dfs_to_sql(tables_names, dfs, file_path=None):

    schemas = create_table_schemas(tables_names, dfs)

    inserts = ""
    for table_name, df in zip(tables_names, dfs):
        inserts += df_to_sql_insert(table_name, df)

    sql = "{}\n{}".format(schemas, inserts)

    if not file_path is None:
        with open(file_path, 'w') as f:
            f.write(sql)

    return sql



def df_to_sql_file(table_name, df, filepath):

    statements = df_to_sql_table(table_name, df)
    with open(filepath, 'w') as f:
        f.write(statements)


def generate_df(requirements, nrows):

    df = pd.DataFrame(index=np.arange(nrows))
    for requirement in requirements:

        colname = requirement['name']
        generator = requirement['generator']
        df[colname] = generator(nrows, df)

    return df




def sigmoid(x):
    return 1 / (1 + np.exp(-x))
