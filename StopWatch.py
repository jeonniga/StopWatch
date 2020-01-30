'''
    스탑워치 프로그램 

    in ubuntu(sudo apt-get install python3-tk)
    but 윈도우 기반에서 python3.8을 설치할때 설치옵션에서 클릭함
    pip install beeply
    pip install auto-py-to-exe
'''
from tkinter import *
import tkinter.font
import time
from beeply import notes
import _thread

class StopWatch(Frame):  
    """ 스탑워치 구현. """                                                                
    def __init__(self, parent=None, **kw):        
        Frame.__init__(self, parent, kw)
        self._start = 0.0        
        self._elapsedtime = 0.0
        self._running = 0
        self.timestr = StringVar()
        self.e = 0
        self.m = 0
        self.makeWidgets()
        self.laps = []
        self.lapmod2 = 0

    
    def makeWidgets(self):                         
        """ 컴퍼넌트 위젯 생성. """
        l1 = Label(self, text='----File Name----')
        l1.pack(fill=X, expand=NO, pady=1, padx=2)

        v = StringVar()
        datestr = time.strftime("%Y%m%d", time.localtime())
        v.set("daily_" + datestr + ".txt")
        self.e = Entry(self, textvariable=v)
        self.e.pack(pady=2, padx=2)
    
        font = tkinter.font.Font(family="맑은 고딕", size=30, slant="italic")
        l = Label(self, textvariable=self.timestr, font=font)
        self._setTime(self._elapsedtime)
        l.pack(fill=X, expand=NO, pady=3, padx=2)

        l2 = Label(self, text='----Laps----')
        l2.pack(fill=X, expand=NO, pady=4, padx=2)

        scrollbar = Scrollbar(self, orient=VERTICAL)
        self.m = Listbox(self,selectmode=EXTENDED, height = 5,
                         yscrollcommand=scrollbar.set)
        self.m.pack(side=LEFT, fill=BOTH, expand=1, pady=5, padx=2)
        scrollbar.config(command=self.m.yview)
        scrollbar.pack(side=RIGHT, fill=Y)



    def beepsound(self):
        mybeep = notes.beeps()
        mybeep.hear('C',2000)


    def _update(self): 
        """ 경과시간 표시. """
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)
        

    def check(self):
        while True:
            if self._running==0:
                break

            tempo = self._elapsedtime - self.lapmod2

            if tempo >= 60 and tempo <= 70:
                self.beepsound()

            time.sleep(10)
    

    def _setTime(self, elap):
        """ 분:초:밀리초의 문자열 설정 """
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)    
        self.timestr.set('%02d:%02d:%02d' % (minutes, seconds, hseconds))


    def _setLapTime(self, elap):
        """ 구간시간 설정 분:초:밀리초 """
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)            
        return '%02d:%02d:%02d' % (minutes, seconds, hseconds)

        
    def Start(self):                                                     
        """ 시작. 이미 시작한 상태면 무시 """
        if not self._running:            
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1      
            _thread.start_new_thread(self.check, ())

  

    
    def Stop(self):                                    
        """ 정지, 이미 정지한 상태면 무시. """
        if self._running:
            self.after_cancel(self._timer)            
            self._elapsedtime = time.time() - self._start    
            self._setTime(self._elapsedtime)
            self._running = 0

    
    def Reset(self):                                  
        """ 스탑워치 시간 리셋. """
        self._start = time.time()         
        self._elapsedtime = 0.0
        self.laps = []   
        self._setTime(self._elapsedtime)


    def Lap(self):
        '''시작 상태에서만 구간시간 설정'''
        tempo = self._elapsedtime - self.lapmod2
        print(tempo)

        if self._running:
            
            self.laps.append(self._setLapTime(tempo))
            self.m.insert(END, self.laps[-1])
            self.m.yview_moveto(1)

            self.lapmod2 = 0.0
            self._start = time.time() 
            self._setTime(self._start)


       
    def GravaCSV(self):
        '''구간시간 정보를 저장'''
        arquivo = str(self.e.get())
        with open(arquivo, 'wb') as lapfile:
            for lap in self.laps:
                lapfile.write((bytes(str(lap) + '\n', 'utf-8')))




def main():
    root = Tk()
    root.title('Daily')
    # 항상 위로 나타나게 설정
    root.wm_attributes("-topmost", 1) 
    sw = StopWatch(root)
    sw.pack(side=TOP)

    Button(root, text='시작', command=sw.Start).pack(side=LEFT)
    Button(root, text='구간', command=sw.Lap).pack(side=LEFT)
    Button(root, text='정지', command=sw.Stop).pack(side=LEFT)
    Button(root, text='리셋', command=sw.Reset).pack(side=LEFT)
    Button(root, text='저장', command=sw.GravaCSV).pack(side=LEFT)
    Button(root, text='종료', command=root.quit).pack(side=LEFT)    
    
    root.mainloop()





if __name__ == '__main__':
    main()