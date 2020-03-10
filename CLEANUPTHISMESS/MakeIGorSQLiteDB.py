#!/usr/bin/python3

# TODO: Script to change the indexed_seqs and the alignment files into a 
# a database to check and access the data
# So also I need to add a option to IGoR to get the data used for the alignment
# and inference in order to integrated with this new pygor3
# - check how to made the relational tables. How to set FOREIGN KEYS in sqlite

import sqlite3

#-- IgorIndexedSeq table
create_table_sql = '''
CREATE TABLE IF NOT EXISTS IgorIndexedSeq (
    seq_index integer PRIMARY KEY,
    sequence text NOT NULL
);
'''

#-- IgorVGeneTemplate table
'''
CREATE TABLE IF NOT EXISTS IgorVGeneTemplate (
    vgene_id integer PRIMARY KEY,
    gene_name text NOT NULL,
    sequence text NOT NULL,
);
'''


#-- IgorVAlignments table
'''
CREATE TABLE IF NOT EXISTS IgorVAlignments (
    id integer PRIMARY KEY,
    seq_index integer,
    vgene_id integer,
    score real,
    offset integer,
    insertions text NOT NULL,
    deletions  text NOT NULL,
    mismatches text NOT NULL,
    length integer,
    offset_5_p_align integer,
    offset_3_p_align integer,
    FOREIGN KEY (project_id) REFERENCES projects (id)
);
'''

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
 
    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def insert_IgorIndexedSeq_FromCSVline(conn, csvline):
    """
    Create a new task
    :param conn:
    :param csvline:
    :return:
    """
 
    sql = ''' INSERT INTO IgorIndexedSeq(seq_index,sequence)
              VALUES(?,?) '''
    
    data = tuple(csvline.split(";"))
    try:
        cur = conn.cursor()
        print(data)
        cur.execute(sql, data)
        conn.commit()
    except sqlite3.Error as e:
        print(e)
        pass

flnIndexedSeqCSV = "pytest/aligns/Barb02_indexed_sequences.csv"
flnIndexedSeqDB  = "test.db"#flnIndexedSeqCSV.split()

#db = sqlite3.connect(flnIndexedSeqDB)
#cursor = db.cursor()

# 1. Create database
conn = create_connection(flnIndexedSeqDB)
# 2. Create a Table 
create_table(conn, create_table_sql)

#csvline="seq_index;sequence"
#csvline="11;CGCACACAGCAGGAGGACTCCGCCGTGTATCTCTGTGCCAGCAGCTTACGAGGGGGAGGCAGCAATCAGCCCCAGCATTTTGGTGAT"
#csvline="7;CGCACACAGCAGGAGGACTCCGCCGTGTATCTCTGTGCCAGCAGCTTACGAGGGGGAGGCAGCAATCAGCCCCAGCATTTTGGTGAT"
# 3. Read csv file line by line and insert values on database.
with open(flnIndexedSeqCSV) as fp:
    csvline = fp.readline()
    while csvline:
#        try:
        print(csvline)
        insert_IgorIndexedSeq_FromCSVline(conn, csvline)
        csvline = fp.readline()
#        except sqlite3.Error as e:
#            print(e)
#            pass
            

conn.close()
#print("database closed")






#cursor.execute('''INSERT INTO Simulation(Directory, strF2B, strB2F, strB2B, strHrad, strBrad) VALUES(?, ?, ?, ?, ?, ?)''',