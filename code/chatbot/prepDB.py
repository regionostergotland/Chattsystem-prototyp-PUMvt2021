import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
import switchboard as switchboard

def prepare_db():
    switchboard.DB_init()
    switchboard.DB_addQ('vad är diabetes', 'Diabetes är en sjukdom som innebär att din kropp inte kan producera insulin som reglerar ditt blodsockervärde. ')
    switchboard.DB_addQ('hur är diabetes', 'Diabetes kan innebära trötthet på grund av lågt blodsocker.')
    switchboard.DB_addQ('varför är diabetes farligt', 'Då diabetes påverkar din förmåga att reglera blodsockret så kan ej reglerat blodsocker innebära trötthet, näringsbrist och potentiellt död.')
    switchboard.DB_addQ('kan diabetes vara farligt', 'Ja det kan det. ')
    switchboard.DB_addQ('vad betyder hola', 'Det betyder hej.')
    switchboard.DB_addQ('hus', 'Kåk.')
    switchboard.DB_addQ('vilka är sympotmen av diabetes', 'Trötthet och man behöver kissa ofta och mycket.')
    switchboard.DB_addQ('vad kan man göra om man har diabetes', 'Kontakta sjukvården. ')
    switchboard.DB_addQ('vad är insulin', 'Insulin är ett ämne som produceras i bukspottskörteln och det reglerar blodsockervärdet.')
    switchboard.DB_addQ('vad är blodsocker', 'Blodsocker är mängden fruktos/socker i blodet.')
    switchboard.DB_addQ('vad är fetma', 'Det är en sjukdom som personer som är kraftig överviktiga lider av.')
    switchboard.DB_addQ('vad orsakar fetma', 'Levandsvanor, stress, sömnbrist, psykisk ohälsa, är ett flertal potentiella orsaker till fetma.')
    switchboard.DB_addQ('vad är corona', 'Det är ett virus, se mer på https://www.1177.se/Ostergotland/sjukdomar--besvar/lungor-och-luftvagar/inflammation-och-infektion-ilungor-och-luftror/om-covid-19--coronavirus/covid-19-coronavirus/')
    switchboard.DB_addQ('hur smittar corona', 'Corona smittar via droppsmitta och kontaktsmitta. Dsv så smittar corona via hostningar, nysningar och fysisk kontakt.')
    switchboard.DB_addQ('hur testar jag mig för corona', 'Gå in på 1177 och anmäl dig för testning där')
    switchboard.DB_addQ('vad är hiv', 'HIV är en könssjukdom som sprids via samlag eller blodtransfusion. Det är ett virus som bryter ner imunförsvaret och som utvecklar AIDS.')
    switchboard.DB_addQ('kan man dö av hiv', 'Ja men risken är mindre om det behandlas i tid. Det finns mycket forskning och bromsmedecin finns tillgänglig. Misstänker du att du kan ha smittats av HIV kontakta 1177 omedelbart.')
    switchboard.DB_addQ('hur får man hiv', 'HIV sprids via blodtransfusion och samlag.')
    switchboard.DB_addQ('jag har haft huvudvärk', 'Har det varat i två veckor?')
    switchboard.DB_addQ('ja', 'En sjuksköterska kommer att gå med i konversationen.')
    switchboard.DB_addQ('nej', 'En sjuksköterska kommer att gå med i konversationen.')
    switchboard.DB_addQ('jag har ont i halsen', 'Har det varat i mer än 1 vecka?')
    switchboard.DB_addQ('jag har ont i ryggen', 'Har det varat i mer än 3 veckor?')
    switchboard.DB_addQ('jag har hög feber', 'Har det varat i mer än 5 dagar?')
    switchboard.DB_addQ('ur mom gay', ' ur mom gayer')
    switchboard.DB_addQ('jag har svullna halsmandlar', 'Har det varat i mer än 1 vecka?')
    
    #switchboard.DB_addQ('', '')
  
if __name__ == '__main__':
    prepare_db()

