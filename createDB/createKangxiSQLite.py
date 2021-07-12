import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
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
    except Error as e:
        print(e)


def create_my_tables():
    database = r"F:\RaspberryPi\Characters\createDB\kangxiNew.db"

    sql_create_kangxi_table = """CREATE TABLE IF NOT EXISTS kangxi (
                                    id integer PRIMARY KEY,
                                    kangxi text NOT NULL,
                                    structure text NOT NULL,
                                    root text NOT NULL,
                                    treeRoot text NOT NULL,
                                    branchRoot text NOT NULL,
                                    derivedFrom text NOT NULL,
                                    english text,
                                    russian text
                                    );"""

    sql_create_meanings_table = """CREATE TABLE IF NOT EXISTS meanings (
                                    id integer PRIMARY KEY,
                                    meaning text NOT NULL
                                    );"""

    sql_create_radicals_table = """CREATE TABLE IF NOT EXISTS radicals (
                                    id integer PRIMARY KEY,
                                    radical text
                                    );"""

    # create a database connection
    conn = create_connection(database)

    if conn is not None:
        # create kangxi table
        create_table(conn, sql_create_kangxi_table)

        # create meanings table 
        create_table(conn, sql_create_meanings_table)

        # create radicals table
        create_table(conn, sql_create_radicals_table)

    else:
        print("Error! Cannot create the database connection.")


def insert_kangxi(conn, character):
    sql = """INSERT INTO kangxi(kangxi, structure, root, treeRoot, branchRoot, derivedFrom, english, russian)
             VALUES(?,?,?,?,?,?,?,?)"""
    cur = conn.cursor()
    cur.execute(sql, character)
    conn.commit()


def insert_meaning(conn, meaning):
    sql = """INSERT INTO meanings(meaning)
             VALUES(?)"""
    cur = conn.cursor()
    cur.execute(sql, meaning)
    conn.commit()


def insert_radical(conn, radical):
    sql = """INSERT INTO radicals(radical)
             VALUES(?)"""
    cur = conn.cursor()
    cur.execute(sql, radical)
    conn.commit()


def addRows(table, item_list):
    database = "kangxiNew.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        # create a new character
        for item in item_list:
            if table == 'kangxi':
                insert_kangxi(conn, item)
            elif table == 'meanings':
                insert_meaning(conn, item)
            elif table == 'radicals':
                insert_radical(conn, item)


def readFile():
    with open('iRR.txt', 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()

    characters = {}
    for line in lines:
        if line == '\n':
            continue
        line = line.split(';')
        characters[line[0]] = line[1:]

    return characters


def processLine(character):
    v = characters[character]
    line = (character, v[1], findRoot(v[1]), splitMeanings(character, 5), splitMeanings(character, 6))
    return line, (splitMeanings(character, 5), splitMeanings(character, 6))


def findRoot(characterStructure):
    for i in range(len(characterStructure)):
        ###Check for radicals
        if characterStructure[i] in characters and characters[characterStructure[i]][1] == characterStructure[i]:
            if i == len(characterStructure) - 1:
                return characterStructure
            continue
        else:
            return characterStructure[:i+1]


def splitMeanings(k, language):
    v = characters[k]
    meanings = v[language].replace('\n', '')
    if '...' in meanings:
        meanings.replace('...', '')

    if '_' in meanings:
        meanings = [meaning.replace('_', ' ').strip() for meaning in meanings.split()]
    elif '  ' in meanings:
        meanings = [meaning.strip() for meaning in meanings.split('  ')]
    elif ',' in meanings:
        if 'междометие, чтобы' in meanings:
            return meanings
        meanings = [meaning.strip() for meaning in meanings.split(',')]
    elif '.' in meanings:
        if 'Cant.' in meanings or 'etc.' in meanings:
            return meanings
        meanings = [meaning.strip() for meaning in meanings.split('.')]
    if type(meanings) == list:
        meanings = ';'.join(meanings)
    return meanings


def findTrees(kangxis): 
    trees = {}
    for char in kangxis:
        trees.setdefault(char[2], []).append(char)    
    return trees


def findBranches(tree):
    
    branches = {}
    nonBranch = []

    root = None
    for i in range(len(tree)):
        if tree[i][2] == tree[i][1]:
            root = tree[i]
            continue
        for n in range(len(tree)):
            if i != n and tree[i][1] in tree[n][1]:
                if tree[i] not in nonBranch:
                    nonBranch.append(tree[i])
                branches.setdefault(tree[i], []).append(tree[n])

    for char in tree:
        if char not in [ch for v in branches.values() for ch in v] and char not in branches.keys() and char != root:
            nonBranch.append(char)

    trunk = []

    for i in range(len(nonBranch)):
        for n in range(len(nonBranch)):
            if i != n and nonBranch[n][1] in nonBranch[i][1]:
                break
            if n == len(nonBranch) - 1 and nonBranch[i] not in trunk:
                trunk.append(nonBranch[i])

    trunk.sort(key=lambda tup: tup[1])
    list(branches.items()).sort(key=lambda tup: tup[0][1])

    return branches, trunk


if __name__ == "__main__":
    characters = readFile()
    kangxis = []
    charactersList = list(characters.items())
    charactersList.sort(key=lambda tup: tup[1][1])
    meanings = []
    for tup in charactersList:
        processedLine, meaning = processLine(tup[0])
        kangxis.append(processedLine)
        meanings.append(meaning)

    trees = findTrees(kangxis) 

    meaningList = {}
    for mean in meanings:
        english = mean[0].strip().split(';')
        russian = mean[1].strip().split(';')
        for eng in english:
            if eng.strip() != '':
                if eng.strip() not in meaningList:
                    meaningList[eng.strip()] = True
        for rus in russian:
            if rus.strip() != '':
                if rus.strip() not in meaningList:
                    meaningList[rus.strip()] = True
    meaningList = list(meaningList.keys())
    meaningList.sort()
    meaningList = [(mean,) for mean in meaningList]

    characterList = []
    for k,v in trees.items():
        root = [char for char in kangxis if char[1] == k and char[1] == char[2]][0]
        if len(v) == 1:
            treeRoot = False
        elif len(v) > 1:
            treeRoot = True
        if root[0] not in [char[0] for char in characterList]:
            characterList.append([root[0], root[1], root[2], treeRoot, False, False, root[3], root[4]])

        branches, nonBranch = findBranches(v)
        for char in nonBranch:
            branchRoot = False
            if char in branches:
                branchRoot = True
            characterList.append([char[0], char[1], char[2], False, branchRoot, False, char[3], char[4]])

        for branchRt, branch in branches.items():
            for ch in branch:
                branchRoot = False
                if ch in branches:
                    branchRoot = True
                if ch[1] in [char[1] for char in characterList]:
                    [char for char in characterList if char[0] == ch[0]][0][5] += branchRt[0]
                else:
                    characterList.append([ch[0], ch[1], ch[2], False, branchRoot, branchRt[0], ch[3], ch[4]])


    # make radical list
    with open('radicals.txt', 'r', encoding="utf-8-sig") as f:
        rads = f.readlines()
    radicals = []
    for r in rads:
        radicals.append(r[0])        

    create_my_tables()
    addRows('kangxi', characterList)
    addRows('meanings', meaningList)
    addRows('radicals', radicals)

