# PUM2
Kandidatprojekt

# TESTING instruktioner
# Python(windows):
(har inte fått det att fungera på mac)
Instalation: 
	Installera pytest
	Detta kan göras via pip (för att köra i terminalen) eller pycharm (för att köra i pycharm)


Det första testet:
	Skapa en test_filnamn.py testfil som importerar funtionerna som ska testas 
		EX: test_shell.py
	Denna fil ska impotera pytest
	Skapa funktioner som börjar med namn test_
	Testerna inuti en testfuntion skrivs: 
		EX: assert 1 == 1
	I terminalen (i pycharm's terminal om intalerat via pycharm) så skrivs: pytest

# Javascript (mac/windows):
	
Instalation:
	Behöver installera npm
	Detta kan göras med att intallera Node js då npm kommer med den

Efter installation så ska npm kunna köras i terminalen via comandot npm
	
Det första testet:
	Skapa en fil som ska testas: filnamn.js EX: sum.js
	Inkludera följande kod: module.exports = funktions_namn; 
		EX: module.exports = sum;
 	Där funktions_namn är namnen på funktioner som ska testas
 	Skapa en fil som ska inehålla testerna: filnamn.test.js 
 		EX: sum.test.js
 	I denna fil så ska det stå högst upp const varnamn = require('./funktions_namn'); för att hämta functionerna
 		EX: const sum = require('./sum');
 	För att köra testerna så skrivs test('<Beskriving>', () => {expect(varnamn(indata)).toBe(utdata);});
 		EX: test('adds 1 + 2 to equal 3', () => {expect(sum(1, 2)).toBe(3);});
 	I terminalen skriv npm test för att köra testerna
