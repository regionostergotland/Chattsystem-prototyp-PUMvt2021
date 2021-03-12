# PUM2
Kandidatprojekt.  
Detta document är skrivet i *markdown*.  
[Syntax docs](https://www.markdownguide.org/basic-syntax/).  
[Online editor](https://dillinger.io/)  

## TESTING instruktioner
### Test python kod
#### Python(i github):
I github så finns det möligheten att testa kod som är pushad.  
##### Metod 1 (automatiskt):
- Pusha en pyton fil till github
- När en ny fill skapen eller uppdateras i github så kommer testerna att köras
- Resultaten av testerna hittas under (Det tar 1 min innan testet är över):
    - Actions
    - Här ska du se en litsta av *workflows* på höger sida av skärmen
    - Den som är högs upp i listan, altså den senaste ska vara ditt test
    - Tryck på namnet av testet *(Troligen heter den **pytest**)*
    - Tryck på *buld*
    - Resultaten ska finnas under de följande:
        - Lint with flake8
        - Test with pytest-cov

##### Metod 2 (manuellt):
- Gå till Actions
- Här ska du se en litsta av *workflows* på vänster sida av skärmen
- Tryck på pytest
- Tryck sendan på *run wokflow* på höger sida av skärmen
- Välj vilken branch som testet ska kötas på och tryck senad på *run wokflow*
- Resultaten av testerna hittas under (Det tar 1 min innan testet är över):
    - Actions
    - Här ska du se en litsta av *workflows* på höger sida av skärmen
    - Den som är högs upp i listan, altså den senaste ska vara ditt test
    - Tryck på namnet av testet *(Troligen heter den **pytest**)*
    - Tryck på *buld*
    - Resultaten ska finnas under de följande:
        - Lint with flake8
        - Test with pytest-cov

#### Python(windows/mac):
Waring pytest i pycharm fungerar inte helt på en mac dator

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

### Testa javascript kod
#### Javascript (i github):
I github så finns det möligheten att testa kod som är pushad.  
##### Metod 1 (automatiskt):
- Pusha en javascript fil till github
- När en ny fill skapen eller uppdateras i github så kommer testerna att köras
- Resultaten av testerna hittas under (Det tar 1 min innan testet är över):
    - Actions
    - Här ska du se en litsta av *workflows* på höger sida av skärmen
    - Den som är högs upp i listan, altså den senaste ska vara ditt test
    - Tryck på namnet av testet *(Troligen heter den samma som din commit)*
    - Tryck på *buld*
    - Resultaten ska finnas under de följande:
        - Test with jest

##### Metod 2 (manuellt):
- Gå till Actions
- Här ska du se en litsta av *workflows* på vänster sida av skärmen
- Tryck på jest
- Tryck sendan på *run wokflow* på höger sida av skärmen
- Välj vilken branch som testet ska kötas på och tryck senad på *run wokflow*
- Resultaten av testerna hittas under (Det tar 1 min innan testet är över):
    - Actions
    - Här ska du se en litsta av *workflows* på höger sida av skärmen
    - Den som är högs upp i listan, altså den senaste ska vara ditt test
    - Tryck på namnet av testet *(Troligen heter den **jest**)*
    - Tryck på *buld*
    - Resultaten ska finnas under de följande:
        - Test with jest

### Javascript (mac/windows) WARING: DETTA fungera inte för tillfälet:
	
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
const sum = require('./sum');
```
- För att skriva testerna så skrivs:
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
- Sendan så behöver du bara köra följande i terminalen så ska testerna köras:
- *npm run test*
