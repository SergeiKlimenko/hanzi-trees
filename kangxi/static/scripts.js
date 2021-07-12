var enterCharacter = document.getElementById("enterCharacter");
var chooseCharacter = document.getElementById("chooseCharacter");
var chooseMeaning = document.getElementById("chooseMeaning");
var chooseSynChar = document.getElementById("chooseSynChar");
var listMeanings = document.getElementById("listMeanings");
var structure = document.getElementById("structure");
var chooseStructureElement = document.getElementById("chooseStructureElement");
var elementMeanings = document.getElementById("elementMeanings");
var treeTrunk = document.getElementById("treeTrunk");
var treeTrunkMeanings = document.getElementById("treeTrunkMeanings");
var branchRoots = document.getElementById("branchRoots");
var branchRootsMeanings = document.getElementById("branchRootsMeanings");
var branchCharacters = document.getElementById("branchCharacters");
var branchMeanings = document.getElementById("branchMeanings");

var enterStructure2 = document.getElementById("enterStructure2");
var chooseCharacter2 = document.getElementById("chooseCharacter2");
var chooseMeaning2 = document.getElementById("chooseMeaning2");
var structure2 = document.getElementById("structure2");
var chooseStructureElement2 = document.getElementById("chooseStructureElement2");
var elementMeanings2 = document.getElementById("elementMeanings2");
var chooseSynChar2 = document.getElementById("chooseSynChar2");
var listMeanings2 = document.getElementById("listMeanings2");
var treeTrunk2 = document.getElementById("treeTrunk2");
var treeTrunkMeanings2 = document.getElementById("treeTrunkMeanings2");
var branchRoots2 = document.getElementById("branchRoots2");
var branchRootsMeanings2 = document.getElementById("branchRootsMeanings2");
var branchCharacters2 = document.getElementById("branchCharacters2");
var branchMeanings2 = document.getElementById("branchMeanings2");

var enterStructure3 = document.getElementById("enterStructure3");
var chooseStructureElement3 = document.getElementById("chooseStructureElement3");
var elementMeanings3 = document.getElementById("elementMeanings3");
var rootList3 = document.getElementById("rootList3");
var listMeanings3 = document.getElementById("listMeanings3");
var tree3 = document.getElementById("tree3");
var treeCharMeanings3 = document.getElementById("treeCharMeanings3");

var enterMeaning4 = document.getElementById("enterMeaning4");
var wholeWord = document.getElementById("wholeWord");
var submit4 = document.getElementById("submit4");
var allMeanings4 = document.getElementById("allMeanings4");
var chooseSynChar4 = document.getElementById("chooseSynChar4");
var listMeanings4 = document.getElementById("listMeanings4");


if (document.getElementsByClassName('nav-link active')[0] !== undefined) {
	document.getElementsByClassName('nav-link active')[0].classList.remove('active');
};


function getListOptions(field1, field2, wholeWord=null) {  
    
    var what;
    if (field1.value.trim() === '') {
        what = null
    } else {
        what = field1.value
    };

    var route;
    if (wholeWord !== null) {
        route = `/list/${field2.id}/${what}/${wholeWord}`
    } else {
        route = `/list/${field2.id}/${what}`
    };

    fetch(route).then(function(response) {
        response.json().then(function(data) {
	    
	    var optionHTML = '';
	    for (var item of data.items) {
	        optionHTML += '<option value="' + item.id + '">' + item.item + '</option>';
	    }
	    
	    field2.innerHTML = optionHTML;

	    if (field1.id === 'enterCharacter') {
            getListOptions(chooseCharacter, chooseMeaning);
	    } else if (field2.id === 'chooseMeaning') {
		getListOptions(chooseMeaning, chooseSynChar); 
		getValue(chooseCharacter, structure);
		getListOptions(chooseCharacter, treeTrunk);
		getListOptions(chooseCharacter, branchRoots);
	    } else if (field2.id === 'treeTrunk') {
		getValue(treeTrunk, treeTrunkMeanings);
	    } else if (field2.id === 'branchRoots') {
		getListOptions(branchRoots, branchCharacters); 
	    } else if (field1.id === 'branchRoots') {
		getValue(branchRoots, branchRootsMeanings);
		getValue(branchCharacters, branchMeanings);
	    };
		
	    if (field1.id === 'chooseMeaning') {
	        removeOption(chooseCharacter, chooseSynChar);
		getValue(chooseSynChar, listMeanings);
	    };
	
	    if (field2.id === 'chooseStructureElement') {
	        getValue(chooseStructureElement, elementMeanings);
	    };

	
	    if (field1.id === 'enterStructure2') {
                getListOptions(chooseCharacter2, chooseMeaning2);
	    } else if (field2.id === 'chooseMeaning2') {
		getListOptions(chooseMeaning2, chooseSynChar2); 
		getValue(chooseCharacter2, structure2);
		getListOptions(chooseCharacter2, treeTrunk2);
		getListOptions(chooseCharacter2, branchRoots2);
	    } else if (field2.id === 'treeTrunk2') {
		getValue(treeTrunk2, treeTrunkMeanings2);
	    } else if (field2.id === 'branchRoots2') {
		getListOptions(branchRoots2, branchCharacters2); 
	    } else if (field1.id === 'branchRoots2') {
		getValue(branchRoots2, branchRootsMeanings2);
		getValue(branchCharacters2, branchMeanings2);
	    };
		
	    if (field1.id === 'chooseMeaning2') {
	        removeOption(chooseCharacter2, chooseSynChar2);
		getValue(chooseSynChar2, listMeanings2);
	    };
	
	    if (field2.id === 'chooseStructureElement2') {
	        getValue(chooseStructureElement2, elementMeanings2);
	    };

		
	    if (field2.id === 'chooseStructureElement3') {
		getValue(chooseStructureElement3, elementMeanings3);
		getListOptions(enterStructure3, rootList3);
	    } else if (field2.id === 'rootList3') {
		getValue(rootList3, listMeanings3);
		getListOptions(rootList3, tree3);
	    } else if (field2.id === 'tree3') {
		getValue(tree3, treeCharMeanings3);
	    };
	
	
	    if (field1.id === 'enterMeaning4') {
		getListOptions(allMeanings4, chooseSynChar4);
	    } else if (field2.id === 'chooseSynChar4') {
		getValue(chooseSynChar4, listMeanings4);
	    };
	});
    });
};


function getValue(field1, field2) {
  
    var what;
    if (field1.value.trim() === '') {
        what = null
    } else {
	what = field1.value
    };

    fetch(`/value/${field2.id}/${what}`).then(function(response) {
        response.json().then(function(data) {
            
	    field2.value = data.items;

	    var textAreas = ['elementMeanings', 'listMeanings', 'treeTrunkMeanings', 'branchRootsMeanings', 'branchMeanings', 'treeCharMeanings'];

	    if (field2.id === 'structure') {
		getListOptions(structure, chooseStructureElement);
	    };

	    
	    if (field2.id === 'structure2') {
		getListOptions(structure2, chooseStructureElement2);
	    };


	    var field2Id = field2.id;

	    if (!(isNaN(field2Id[field2Id.length - 1]))) {
	        field2Id = field2Id.substring(0, field2Id.length - 1);
	    };

	    if (textAreas.includes(field2Id)) {
		adjustTextArea(field2);
	    };


	});
    });
};


function removeOption(field1, field2) {
    for (var i = 0; i < field2.options.length; i++) {
	if (field2.options[i].value === field1.value) {
            field2.remove(i);
	};
    };
};
	

function adjustTextArea(textArea) {
    textArea.style.height = "1px";
    textArea.style.height = (25+textArea.scrollHeight)+"px";
};


function input(field, value) {
    field.value = field.value + value;
    var fieldIdNumber = field.id[field.id.length - 1];
    if (fieldIdNumber === '2') {
	getListOptions(enterStructure2, chooseCharacter2);
    } else if (fieldIdNumber === '3') {
	getListOptions(enterStructure3, chooseStructureElement3); 
    };
};


