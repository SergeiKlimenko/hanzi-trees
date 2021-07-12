from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField, BooleanField, SubmitField


class characterSearchForm(FlaskForm):

    enterCharacter = StringField('Enter a character/characters')
    enterCharStructure = StringField('Enter a character structure')
    chooseCharacter = SelectField('Choose a character', choices=[])
    chooseMeaning = SelectField('Choose a meaning', choices=[])
    structure = StringField('Character structure')
    chooseStructureElement = SelectField('Choose a structure element', choices=[])
    elementMeanings = TextAreaField('Element meanings')


class synonymousCharactersForm(FlaskForm):

    chooseSynChar = SelectField('Characters with the same meaning', choices=[])
    listMeanings = TextAreaField('All meanings of the character')


class treeForm(FlaskForm):

    treeTrunk = SelectField('Tree trunk', choices=[])
    treeTrunkMeanings = TextAreaField('Meanings')
    branchRoots = SelectField('Branch roots', choices=[])
    branchRootsMeanings = TextAreaField('Meanings')
    branchCharacters = SelectField('Characters in the branch', choices=[])
    branchMeanings = TextAreaField('Meanings')
    

class treeSearchForm(FlaskForm):

    enterStructure = StringField('Enter root elements')
    chooseStructureElement = SelectField('Choose root element', choices=[])
    elementMeanings = TextAreaField('Root element meanings')
    rootList = SelectField('Choose a root', choices=[])
    rootListMeanings = TextAreaField('Root meanings')
    treeList = SelectField('Select a tree/branch member', choices=[])
    treeCharMeanings = TextAreaField('Character meanings')


class meaningSearchForm(FlaskForm):

    enterMeaning = StringField('Enter a meaning')
    wholeWord = BooleanField('Search a whole word')
    submit = SubmitField('Search')
    allMeanings = SelectField('Choose a meaning', choices=[])
    chooseCharacter = SelectField('Choose a character', choices=[])
    listMeanings = TextAreaField('Character meanings')
