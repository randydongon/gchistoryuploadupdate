import xlsxwriter 
import re

from progress.spinner import Spinner
#xlsxwriter
# workbook = xlsxwriter.Workbook('gcmsgs.xlsx')

def allgchistory(sk, gcid):
    filename = getfilename()
    workbook = getworkbook(filename) # workbook    
    
    ln = len(gcid)
    history = True
    
    for x in gcid:
        if ln <= 0:
            workbook.close()
            history = False
            print("Group chat history successfully extracted.")
            break
        else:
            ln-=1
        
        if re.findall('19', x):
            ch = sk.chats.chat(x)
            
            sheetname = cleanstring(gcid[x].topic) #remove special characters
            msg(sheetname)
            worksheet = workbook.add_worksheet(sheetname)

            getMsgs(ch, sk, worksheet, history)   
                    

    workbook.close()
    print(f'{filename} GC History successfully retrieved!')
    # uploadfile('./docs/', filename+'.xlsx')



def removeHtmlTag(raw_txt):
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', raw_txt)
    return cleantext.strip()


def singlegchistory(sk, gcid, id):
    filename = getfilename()
    workbook = getworkbook(filename) #generate workbook    
    ch = sk.chats.chat(id)    
    history = True    
    sheetname = cleanstring(gcid[id.strip()].topic)       
       
    worksheet = workbook.add_worksheet(sheetname)

    msg(sheetname)
    
    getMsgs(ch,sk, worksheet, history)               
    
    workbook.close()
    print(f'{filename} GC History successfully retrieved!')


def getworkbook(filename):
    doc = './docs/'
    
    workbook = xlsxwriter.Workbook(doc+filename + '.xlsx')
    return workbook


def getMsgs(ch,sk, worksheet, history):
    from animatecursor import CursorAnimation
    spin = CursorAnimation()
    spin.start()    

    col = 0
    row = 0
    outer = False    
    msglist = []
    while history:
        
        gcmsgs = ch.getMsgs()
        
        for ms in gcmsgs:

            if re.findall('HistoryDisclosedUpdate', ms.type): # 
                print(ms.type)
                print(ms.history)
                history = False                
                outer = ms.history
                
                break

            else:
                if sk.contacts[ms.userId]:
                    msglist.append(ms)
                                                                                
                   
        if outer:   
            spin.stop()        
            break

    msglist.reverse()                                
    for ms in msglist:    
        worksheet.write(row, col, str(ms.time))
        worksheet.write(row, col + 1, sk.contacts[ms.userId].name.first)
        worksheet.write(row, col + 2, removeHtmlTag(ms.content))
        row += 1  




def msg(cleanString):    
    print(f"Extracting: {cleanString} Chat History...")    


def cleanstring(strval):
    cleanString = re.sub('\W+', ' ', strval) 
    if len(cleanString) > 30:
        cleanString = cleanString[:30]
    
    content = cleanString.encode('utf-8').decode('utf8')
    return content


def getfilename():
    filename = input("Enter File name: ")
    return filename



