import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
import switchboard as switchboard

def prepare_db():
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

if __name__ == '__main__':
    switchboard.DB_init()
    prepare_db()