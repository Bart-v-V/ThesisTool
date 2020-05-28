var fs = require('fs');
var esprima = require('esprima');
var estraverse = require('estraverse');
var walk = require('walk');

var output = "";
var scopeSchain = [];

options = {
	followLinks: false
};

var fileName = 'current.txt';


output = memberExpressionExpansion(fileName);
if (output != null) {
	fs.writeFile(fileName + '.exp', output, function(err) {
		if(err) {
			return console.log(err);
		}
	});
};


function memberExpressionExpansion(filepath) {
	output = "";
	try{
		var ast = esprima.parse(fs.readFileSync(filepath, 'utf-8'));
	} catch (err){
		console.log(err)
		return null;
	}

	scopeChain = [];
	estraverse.traverse(ast, {
		enter: enter,
		leave: leave
	});
	return output;
}


function getIdentifierOrName(node) {
	var name = undefined;
	
	if (node.type === "Identifier"){
		name = node.name;
	}
	else if (node.type === "MemberExpression") {
		name = getIdentifierOrName(node.object) + '.' + node.property.name;
	}
	return name;
}


function addToScope(node) {
	var currentScope = scopeChain[scopeChain.length - 1];

	if (node.id != null) {
		var identifier = node.id.name;
		var name = undefined;

		if (node.init != null) {
			name = getIdentifierOrName(node.init);
		}

		currentScope[identifier] = name
	}
	
	else if (node.left != null && node.right != null) {
		var identifier = node.left.name;
		var name = getIdentifierOrName(node.right);
		currentScope[identifier] = name;
	}
}


function enter(node) {
	if (createsNewScope(node)){
		scopeChain.push({});
	}

	if (node.type === 'VariableDeclarator') {
		addToScope(node);
	}
	else if (node.type === 'AssignmentExpression') {
		assignVarValue(node.left.name, getIdentifierOrName(node.right), node, scopeChain);
	}
	else if (node.type === 'MemberExpression') {
		output += isVarDefined(getIdentifierOrName(node.object), scopeChain, []) + '.' + node.property.name + '\n';
	}
}


function leave(node) { 
	if (createsNewScope(node)){
		scopeChain.pop();
	}
}


function isVarDefined(varname, scopeChain, previous) {
	var rest = '';
	if (varname == null) {
		return undefined;
	}
	
	if (varname.indexOf('.') >= 0){
		rest = '.' + varname.slice(varname.indexOf('.') + 1);
		varname = varname.split('.')[0];
	}

	for (var i = 0; i < scopeChain.length; i++){
		var scope = scopeChain[i];
		if (varname in scope){
			var returnValue = scope[varname];
			if (returnValue != undefined) {
				if (scope != null && scope[varname] != null && typeof(scope[varname]) == "string" && scope[varname].split('.')[0] != varname && !(previous.indexOf(scope[varname].split('.')[0]) > -1)){
					previous.push(scope[varname].split('.')[0]);
					
					var next = isVarDefined(scope[varname].split('.')[0], scopeChain, previous);
					if (next != undefined) {
						returnValue = scope[varname].replace(scope[varname].split('.')[0], next);
					}
				}
			return returnValue + rest;
			}
		}
	}
	return varname + rest;
}


function assignVarValue(varname, value, node, scopeChain) {
	var currentScope = scopeChain[scopeChain.length - 1];
	if (varname in currentScope){
		currentScope[varname] = value;
		return;
	}
	addToScope(node);
}


function createsNewScope(node) {
	return node.type === 'FunctionDeclaration' || node.type === 'FunctionExpression' || node.type === 'Program';
}
