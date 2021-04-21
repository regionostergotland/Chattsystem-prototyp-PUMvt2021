import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
import switchboard as switchboard

def prepare_db():
    switchboard.DB_init()
    switchboard.DB_addQ('vad är diabetes', 'dålig')
    switchboard.DB_addQ('hur är diabetes', 'inte bra')
    switchboard.DB_addQ('varför är diabetes farligt', 'kan dö')
    switchboard.DB_addQ('kan diabetes vara farligt', 'ja')
    switchboard.DB_addQ('vad betyder hola', 'det betyder hej')
    switchboard.DB_addQ('hus', 'kåk')
    switchboard.DB_addQ('vilka är sympotmen av diabetes', 'lågt blodtryck, osv...')
    switchboard.DB_addQ('vad kan man göra om man har diabetes', 'börja använda insulin')
    switchboard.DB_addQ('vad är insulin', 'insulin sänker/höjer blodsockervärde')
    switchboard.DB_addQ('vad är blodsocker', 'blodsocker är mängden fruktos/socker i blodet')
    switchboard.DB_addQ('vad är fetma', 'det är när en person är kraftig överviktig')
    switchboard.DB_addQ('vad orsakar fetma', 'levandsvanor, stress, sömnbrist, psykisk ohälsa')
    switchboard.DB_addQ('vad är corona', 'det är ett virus')
    switchboard.DB_addQ('hur smittar corona', 'genom att inte vara i karantän')
    switchboard.DB_addQ('hur testar jag mig för corona', 'kontakta din vårdcentral')
    switchboard.DB_addQ('vad är hiv', 'det är en könssjukdom')
    switchboard.DB_addQ('kan man dö av hiv', 'ja men risken är mindre om det behandlas i tid')
    switchboard.DB_addQ('hur får man hiv', 'via blod och samlag')
    switchboard.DB_addQ('jag har haft huvudvärk', 'har det varat i två veckor?')
    switchboard.DB_addQ('ja', 'en sjuksköterska kommer att gå med i konversationen.')
    switchboard.DB_addQ('nej', 'en sjuksköterska kommer att gå med i konversationen.')
    #switchboard.DB_addQ('', '')
"""  
if __name__ == '__main__':
    switchboard.DB_init()
    prepare_db()
"""
