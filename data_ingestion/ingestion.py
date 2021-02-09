from sqlalchemy import create_engine
import pymysql
import sqlalchemy
import os
import pandas as pd
import configparser

# ignore SettingWithCopyWarning
pd.options.mode.chained_assignment = None  # default='warn'

# set working directory in beginning of the python
if not os.path.dirname(__file__) == "":
    os.chdir(os.path.dirname(__file__))

# step 1:
config = configparser.ConfigParser()
if os.path.exists("../config.ini"):
    config.read('../config.ini')
    db_host = config.get('DATABASE', 'DB_HOST')
    db_user = config.get('DATABASE', 'DB_USER')
    db_password = config.get('DATABASE', 'DB_PASS')
    db_port = config.get('DATABASE', 'DB_PORT')
    db_name = config.get('DATABASE', 'DB_NAME')
    db_table = config.get('DATABASE', 'DB_TABLE')
    file_path = config.get('DATA', 'DATA_PATH')
else:
    raise Exception ("Config file is not available...")

# step: 2
def db_connection():
    """
    """
    is_error = False
    try:
        db_conn_str = 'mysql+pymysql://'+ db_user + ':' + db_password + '@' + db_host + ':' + db_port + '/' + db_name
        db_conn = create_engine(db_conn_str)
        return db_conn
    except Exception as e:
        is_error = True
        msg = "Can't connect with the database "
        raise Exception (msg + str(e))

# step: 3
def read_data(file_path):
    """
    args: file path
    return: dataframe
    """
    is_error = False
    try:
        if os.path.exists(file_path): 
            df = pd.read_excel(file_path)
            return df
        else:
            raise ("File doesn't exists")
    except Exception as e:
        is_error = True
        msg = "Unable to read data "
        raise Exception (msg + str(e))

# step 4
def data_cleanup (df):
    """
    args: dataframe
    return: dataframe
    """
    is_error = False
    us_state = {
        'Alabama': 'AL', 'Alaska': 'AK', 'American Samoa': 'AS', 'Arizona': 'AZ', 'Arkansas': 'AR',
        'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL',
        'District of Columbia': 'DC', 'Georgia': 'GA', 'Guam': 'GU', 'Hawaii': 'HI', 'Idaho': 'ID',
        'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA',
        'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN',
        'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'Utah': 'UT',
        'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC',
        'North Dakota': 'ND', 'Northern Mariana Islands': 'MP', 'Oklahoma': 'OK', 'Oregon': 'OR',
        'Pennsylvania': 'PA', 'Puerto Rico': 'PR', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD',
        'Tennessee': 'TN', 'Texas': 'TX', 'Vermont': 'VT', 'Virgin Islands': 'VI', 'Virginia': 'VA',
        'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY', 'Ohio': 'OH'
    }
    us_state = dict((y.upper(), x.upper()) for x, y in us_state.items())
    try:
        df.rename( columns={"WORKSITE_CITY_1": "WORKSITE_CITY", \
                            "WORKSITE_STATE_1": "WORKSITE_STATE", \
                            "WAGE_RATE_OF_PAY_FROM_1": "DISCLOSE_WAGE_RATE", \
                            "WAGE_RATE_OF_PAY_TO_1": "ACTUAL_WAGE_RATE"}, inplace = True)

        df = df[['JOB_TITLE', 'WORKSITE_CITY', \
                 'WORKSITE_STATE', 'DISCLOSE_WAGE_RATE', 'ACTUAL_WAGE_RATE']]
        
        # mapping state short name to full name
        df['WORKSITE_STATE'] = df['WORKSITE_STATE'].map(us_state).fillna(df['WORKSITE_STATE'])

        # make city upper case
        df['WORKSITE_CITY'] = df['WORKSITE_CITY'].str.upper()

        # replace Null value to zero
        df[['DISCLOSE_WAGE_RATE', 'ACTUAL_WAGE_RATE']] = df[['DISCLOSE_WAGE_RATE', 'ACTUAL_WAGE_RATE']] \
            .where(df[['DISCLOSE_WAGE_RATE', 'ACTUAL_WAGE_RATE']].notnull(), 0)
        return df
    except Exception as e:  
        is_error = True
        raise Exception (str(e) + " occured while creating data cleanup")

# step 5
def data_insert(db_conn, df, db_table):
    """
    args: db connection, dataframe, database table name
    return: True, False
    """
    is_error = False
    try:
        df.to_sql(db_table, db_conn, if_exists='append', index=True, index_label='ID',
                  dtype={'JOB_TITLE': sqlalchemy.types.VARCHAR(length=111),
                         'WORKSITE_CITY':  sqlalchemy.types.VARCHAR(length=33),
                         'WORKSITE_STATE': sqlalchemy.types.VARCHAR(length=33),
                         'DISCLOSE_WAGE_RATE': sqlalchemy.types.Float(precision=3, asdecimal=True),
                         'ACTUAL_WAGE_RATE': sqlalchemy.types.Float(precision=3, asdecimal=True)})
        return True
    except Exception as e:
        is_error = True
        msg = "Failed to insert data "
        raise Exception(msg + str(e))
    finally:
        if is_error == False:
            print("Succesfully data inserted...")

def main():
    is_error = False
    try:
        df = read_data(file_path)
        df = data_cleanup(df)
        db_conn = db_connection()
        data_insert(db_conn, df, db_table)
    except Exception as e:
        is_error = True
        raise e
    finally:
        if is_error == False:
            print ("Succes...")

if __name__ == "__main__":
    main()
