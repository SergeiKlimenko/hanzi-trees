with open('iRR.csv', 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

###Make characters dictionary
characters = {}
for line in lines:
    if line == '\n':
        continue
    line = line.split(';')
    characters[line[0]] = line[1:]


def findRoot(characterStructure):
    for i in range(len(characterStructure)):
        ###Check for radicals
        if characterStructure[i] in characters and characters[characterStructure[i]][1] == characterStructure[i]:
            if i == len(characterStructure) - 1:
                return characterStructure
            continue
        else:
            return characterStructure[:i]


def buildTree(character):
    with open('tree.txt', 'w') as f:
        for k, v in characters.items():
            if findRoot(characters[character][1]) == findRoot(v[1]):
                f.write(k + ' ' + str(v) + '\n')


def splitMeanings(k, language):
    v = characters[k]
    meanings = v[language].replace('\n', '')
    if '...' in meanings:
        meanings.replace('...', '')

    if '_' in meanings:
        meanings = [meaning.replace('_', ' ').strip() for meaning in meanings.split()]
    elif ',' in meanings:
        if 'междометие, чтобы' in meanings:
            return meanings
        meanings = [meaning.strip() for meaning in meanings.split(',')]
    elif '.' in meanings:
        if 'Cant.' in meanings or 'etc.' in meanings:
            return meanings
        meanings = [meaning.strip() for meaning in meanings.split('.')]
    elif '  ' in meanings:
        meanings = [meaning.strip() for meaning in meanings.split('  ')]
    if type(meanings) == list:
        meanings = ';'.join(meanings)
    return meanings
        

def processLine(character): 
    v = characters[character]
    line = [character, v[1], findRoot(v[1]), splitMeanings(character, 5), splitMeanings(character, 6)]
    return line

        
if __name__ == "__main__":
    for k in sorted(characters.keys()):
        processLine(k)
    
    
