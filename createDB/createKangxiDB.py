from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config


def insert_character(kangxis, what):
    if what == 'kangxi':
        query = "INSERT INTO kangxi(kangxi, structure, root, treeRoot, branchRoot, derivedFrom, english, russian)" \
                "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
    elif what == 'meanings':
        query = "INSERT INTO meanings(meaning) VALUES(%s)"
    elif what == 'radicals':
        query = "INSERT INTO radicals(radical) VALUES(%s)"

    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)

        cursor = conn.cursor()
        cursor.executemany(query, kangxis)

        conn.commit()

    except Error as error:
        print(error)

    finally:
        cursor.close()
        conn.close()


def main(kangxis):
    insert_character(kangxis, 'kangxi')


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


def findRoot(characterStructure):
    for i in range(len(characterStructure)):
        ###Check for radicals
        if characterStructure[i] in characters and characters[characterStructure[i]][1] == characterStructure[i]:
            if i == len(characterStructure) - 1:
                return characterStructure
            continue
        else:
            return characterStructure[:i+1]


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


def addRadicals():
    with open('radicals.txt', 'r', encoding="utf-8-sig") as f:
        rads = f.readlines()
    radicals = []
    for r in rads:
        radicals.append(r[0])        

    insert_character(radicals, 'radicals')


def processLine(character):
    v = characters[character]
    line = (character, v[1], findRoot(v[1]), splitMeanings(character, 5), splitMeanings(character, 6))
    return line, (splitMeanings(character, 5), splitMeanings(character, 6))


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
    
    characterList = []
 
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
    #print(meaningList)

    # for mean in meaningList:
    #     if '  ' not in mean[0]:
    #         if ' ' in mean[0]:
    #             print(mean[0])
    
    for k,v in trees.items():
        root = [char for char in kangxis if char[1] == k and char[1] == char[2]][0]
 #       print("ROOT:", root)
        if len(v) == 1:
            treeRoot = False
        elif len(v) > 1:
            treeRoot = True
        if root[0] not in [char[0] for char in characterList]:
            characterList.append([root[0], root[1], root[2], treeRoot, False, False, root[3], root[4]])

        branches, nonBranch = findBranches(v)
        #if len(nonBranch) != 0:
 #           print('    TRUNK:')
        for char in nonBranch:
 #           print('        ', str(char))
            branchRoot = False
            if char in branches:
                branchRoot = True
            characterList.append([char[0], char[1], char[2], False, branchRoot, False, char[3], char[4]])

        for branchRt, branch in branches.items():
 #           print('    BRANCH ROOT:', branchRt)
            for ch in branch:
 #               print('        ', str(ch))
                branchRoot = False
                if ch in branches:
                    branchRoot = True
                if ch[1] in [char[1] for char in characterList]:
                    [char for char in characterList if char[0] == ch[0]][0][4] += branchRt[0]
                else:
                    characterList.append([ch[0], ch[1], ch[2], False, branchRoot, branchRt[0], ch[3], ch[4]])
#        print('\n')
    main(characterList)
    insert_character(meaningList, 'meanings')
    addRadicals()


