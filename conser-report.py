from omnifocus import Visitor, build_model, traverse_folder
from datetime import date
import os

DAYS={'0':'Sun', '1':'Mon', '2':'Tue', '3':'Wed', '4':'Thu', '5':'Fri', '6':'Sat'}
MONTHS={'01':'Jan', '02':'Feb', '03':'Mar', '04':'Apr', '05':'May', '06':'Jun', '07':'Jul','08':'Aug', '09':'Sep', '10':'Oct', '11':'Nov', '12':'Dec'}

def format_date (thedate = date.today()):
        if thedate == None:
            return ''
        result = DAYS[thedate.strftime('%w')]
        result += ' ' + MONTHS[thedate.strftime('%m')]
        result += thedate.strftime(' %d %Y')
        return result
    
def format_timestamp (thedate = date.today()):
        return thedate.strftime('%Y-%m-%d')
    
class WeeklyReportVisitor(Visitor):

    def __init__ (self, out, proj_pfx='#', indent=4):
        self.tasks = []
        self.out = out
        self.proj_pfx = proj_pfx
        self.todo = False
    def end_project (self, project):
        if len(self.tasks) > 0 and self.todo and project.date_completed == None and project.name.startswith ('CONSER'):
            print >>self.out, self.proj_pfx + ' ' + str(project)
            #self.tasks.sort(key=lambda task:task.date_completed)
            for task in self.tasks:
                if task.date_completed != None:
                    print >>self.out, '- ' + str(task) + ' *[' + format_date(task.date_completed) + ']*'
                else:
                    print >>self.out, '- ' + str(task)
            if project.date_completed != None:
                print >>self.out, '- Finished *[' + format_date(project.date_completed) + ']*'
            print >>self.out
        self.tasks = []
        self.todo = False
    def begin_task (self, task):
        if task.date_completed == None:
            self.todo = True
        self.tasks.append (task)
    
folders, contexts = build_model ('/Users/psidnell/Library/Caches/com.omnigroup.OmniFocus/OmniFocusDatabase2')

file_name='/Users/psidnell/Documents/Reports/ConserReport.md'
out=open(file_name, 'w')
for folder in folders:
    if folder.name == 'Work':
        traverse_folder (WeeklyReportVisitor (out, proj_pfx='#'), folder)
out.close()
os.system("open '" + file_name + "'")
