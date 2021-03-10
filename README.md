# PUM2
Kandidatprojekt.  
Detta document är skrivet i *markdown*.  
[Syntax docs](https://www.markdownguide.org/basic-syntax/).  
[Online editor](https://dillinger.io/)  

## TESTING instruktioner
### Python(windows):
(har inte fått det att fungera på mac)

##### Instalation: 
- Installera *pytest*
- Detta kan göras via *pip install -U pytest* (för att köra i terminalen) eller via inställningar i *pycharm* (för att köra i pycharm)

##### Det första testet:
- Skapa en *filnamn_test.py* testfil som importerar funtionerna som ska testas 
- **EX:** *sum_test.py*
- Denna fil ska impotera *pytest*
- Skapa funktioner som börjar med namn *filnamn_test*
- Testerna inuti en testfuntion skrivs: 
```py
assert sum(1, 2) == 3
```
- I terminalen (i pycharm's terminal om intalerat via pycharm) så skrivs: *pytest* för att starta testen

### Javascript (mac/windows):
	
##### Instalation:
- Behöver installera *npm*
- Detta kan göras med att intallera [Node js](https://nodejs.org/en/) då *npm* kommer med den

Efter installation så ska *npm* kunna köras i terminalen via comandot **npm**
	
##### Det första testet:
- Skapa en fil som ska testas: *filnamn.js*
- **EX:** *sum.js*
- Inkludera följande kod:
```js
module.exports = funktions_namn;
```
- **EX:** 
```js
module.exports = sum;
```
- Där *funktions_namn* är namnen på funktioner som ska testas
- Skapa en fil som ska inehålla testerna: *filnamn.test.js* 
- **EX:** *sum.test.js*
- I denna fil så ska det följande stå högst upp för att hämta functionerna
```js
const varnamn = require('./funktions_namn');
```
- **EX:**
```js
- const sum = require('./sum');
```
- För att köra testerna så skrivs:
```js
test('Beskriving', () => {
    expect(varnamn(indata)).toBe(utdata);
});
```
- **EX:**
```js
test('adds 1 + 2 to equal 3', () => {
    expect(sum(1, 2)).toBe(3);
});
```