# coding: utf8
from flask import render_template, request, Blueprint, jsonify
from kangxi import db
from .forms import characterSearchForm, synonymousCharactersForm, treeForm, treeSearchForm, meaningSearchForm
import sqlalchemy as sa
import urllib


functions = Blueprint('functions', __name__)


kangxi = db.Table('kangxi', db.metadata, autoload=True, autoload_with=db.engine)
meanings = db.Table('meanings', db.metadata, autoload=True, autoload_with=db.engine)
radicals = db.Table('radicals', db.metadata, autoload=True, autoload_with=db.engine)


@functions.route('/characterSearch', methods=['GET', 'POST'])
def characterSearch():
    
    charSearchForm = characterSearchForm()
    synCharForm = synonymousCharactersForm()
    trForm = treeForm()
    trSearchForm = treeSearchForm()
    meanSearchForm = meaningSearchForm()
    rads = db.session.query(radicals).all()
    
    return render_template('characterSearch.html',
                            charSearchForm=charSearchForm,
                            synCharForm=synCharForm,
                            trForm=trForm,
                            trSearchForm=trSearchForm,
                            meanSearchForm=meanSearchForm,
                            rads=rads)


@functions.route('/list/<what>/<value>')
@functions.route('/list/<what>/<value>/<wholeWord>')
def getList(what, value=None, wholeWord=None):

    value = urllib.parse.unquote(value)

    if value == 'null':
        return jsonify({'items': []})

    listArray = []

    if what.startswith('chooseMeaning'):
        meanings = db.session.query(kangxi).filter_by(id=value).with_entities(sa.text('english'), sa.text('russian')).first()
        value = meanings[0].split(';') + meanings[1].split(';')

    elif what.startswith('chooseSynChar'):
        query = sa.text(f"SELECT id, kangxi FROM kangxi WHERE english LIKE '%;{value};%' OR russian LIKE '%;{value};%' OR LEFT(TRIM(BOTH FROM english), {len(value)+1}) = '{value};' OR LEFT(TRIM(BOTH FROM russian), {len(value)+1}) = '{value};' OR RIGHT(TRIM(BOTH FROM english), {len(value)+1}) = ';{value}' OR RIGHT(TRIM(BOTH FROM russian), {len(value)+1}) = ';{value}' OR TRIM(BOTH FROM english) = '{value}' OR TRIM(BOTH FROM russian) = '{value}'")
        value = list(db.engine.execute(query))

    elif what.startswith('treeTrunk') or what.startswith('branchRoots'):
        root = db.session.query(kangxi).filter_by(id=value).with_entities(sa.text('root')).first()[0]
        if what.startswith('treeTrunk'):
            value = db.session.query(kangxi).filter_by(root=root).filter_by(derivedFrom=0).with_entities(sa.text('id'), sa.text('kangxi')).all()
        elif what.startswith('branchRoots'):
            value = db.session.query(kangxi).filter_by(root=root).filter_by(branchRoot=1).with_entities(sa.text('id'), sa.text('kangxi')).all()

    elif what.startswith('branchCharacters'):
        valueChar = db.session.query(kangxi).filter_by(id=value).with_entities(sa.text('kangxi')).first()[0]
        query = sa.text(f"SELECT id, kangxi FROM kangxi WHERE derivedFrom LIKE '%{valueChar}%'")
        value = list(db.engine.execute(query))

    elif what == 'chooseCharacter2':
        queryLike = ' AND '.join([f"structure LIKE '%{radical}%'" for radical in value])
        query = sa.text(f"SELECT id, kangxi FROM kangxi WHERE {queryLike} AND CHAR_LENGTH(structure) >= {len(value)}")
        value = list(db.engine.execute(query))

    elif what == 'rootList3':
        queryLike = ' AND '.join([f"structure LIKE '%{radical}%'" for radical in value])
        query = sa.text(f"SELECT id, kangxi FROM kangxi WHERE {queryLike} AND CHAR_LENGTH(structure) >= {len(value)} AND (branchRoot = 1 OR structure = root)")
        value = list(db.engine.execute(query))

    elif what == 'tree3':
        rootQuery = db.session.query(kangxi).filter_by(id=value).with_entities(sa.text('kangxi'), sa.text('branchRoot'), sa.text('structure'), sa.text('root')).first()
        if rootQuery[1] == 1:
            queryLike = f"derivedFrom LIKE '%{rootQuery[0]}'"
            query = sa.text(f"SELECT id, kangxi FROM kangxi WHERE {queryLike}")
            value = list(db.engine.execute(query))
        elif rootQuery[1] == 0 and rootQuery[2] == rootQuery[3]:
            value = db.session.query(kangxi).filter_by(root=rootQuery[3]).with_entities(sa.text('id'), sa.text('kangxi')).all()

    elif what == 'allMeanings4':
        if wholeWord == 'n':
            query = sa.text(f"SELECT meaning, meaning FROM meanings WHERE meaning = '{value}' OR meaning LIKE '% {value} %' OR LEFT(TRIM(BOTH FROM meaning), {len(value)+1}) = '{value} ' OR RIGHT(TRIM(BOTH FROM meaning), {len(value)+1}) = ' {value}'")
        elif wholeWord == 'y':
            query = sa.text(f"SELECT meaning, meaning FROM meanings WHERE meaning LIKE '%{value}%'")
        value = list(db.engine.execute(query))

    if what.startswith('chooseStructureElement') and not what.endswith('3'):
        value = value[:-1]

    for char in value:

        charObj = {}
        if what == 'chooseCharacter' or what.startswith('chooseStructureElement'):
            try:
                characterInDB = db.session.query(kangxi).filter_by(kangxi=char).with_entities(sa.text('id')).first()[0]
            except:
                continue
            charObj['id'] = characterInDB 
            charObj['item'] = char
        elif what.startswith('chooseMeaning'):
            charObj['id'] = char
            charObj['item'] = char
        else:
            charObj['id'] = char[0]
            charObj['item'] = char[1]
        listArray.append(charObj)

    return jsonify({'items': listArray})


@functions.route('/value/<what>/<characterID>')
def getValue(what, characterID):

    characterID = urllib.parse.unquote(characterID)

    if characterID == 'null':
        return jsonify({'items': []})

    if what.startswith('structure'):
        value = db.session.query(kangxi).filter_by(id=characterID).with_entities(sa.text('structure')).first()[0]
        with open('shit.txt', 'a', encoding="utf-8-sig") as f:
            f.write(value)

    elif 'Meanings' in what:
        if what.startswith('rootMeanings'):
            meaning = db.session.query(kangxi).filter_by(kangxi=characterID).with_entities(sa.text('english'), sa.text('russian')).first()
        else:
            meaning = db.session.query(kangxi).filter_by(id=characterID).with_entities(sa.text('english'), sa.text('russian')).first()
        value = meaning[0].split(';') + meaning[1].split(';')
        value = ', '.join(value)
        
    return jsonify({'items': value})
