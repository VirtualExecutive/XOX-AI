import random

class Board():
    ## Yeni Oyun Tahtası
    def __init__(self) -> None:
        self.boxs = [" "]*9
    
    # NO CHANGE!!
    oyuncu = "X"
    bot = "O"
    isPlayer=True

    ## Oyun Tahtasını yazdır
    def Display(self):
        for i in range(3):
            print("___"*4+"_")  
            print(f"| {self.boxs[i*3]} | {self.boxs[i*3+1]} | {self.boxs[i*3+2]} |")
        print("___"*4+"_")
    
    ## Oyunculardan biri kazandı mı?
    def isWinner(self):
        for i in range(3):
            
            ## Yatay olarak eşleşen var mı?
            if self.boxs[i*3] == self.boxs[i*3+1] == self.boxs[i*3+2] and not self.boxs[i*3] == " ":
                return self.boxs[i*3] # -> "X" or "O"
            
            ## Dikey olarak eşleşen var mı?
            if self.boxs[i] == self.boxs[i+3] == self.boxs[i+6] and not self.boxs[i] == " ":
                return self.boxs[i] # -> "X" or "O"
        
        ## Çapraz olarak eşleşen var mı?
        if (self.boxs[0] == self.boxs[4] == self.boxs[8] or self.boxs[6] == self.boxs[4] == self.boxs[2]) and not self.boxs[4] == " ":
            return self.boxs[4] # -> "X" or "O"
        
        ## Hala kazanan yok
        return False
    
    def isFinish(self):
        Winner = self.isWinner() ## -> "X" or "O" or False

        if Winner:
            return Winner
        else:
            ## Boşluk kontrolü
            for i in self.boxs:
                if i == " ":
                    ## Boş kutu varsa hala devam ediyor.
                    return False
                
        ## Boş kutu kalmadı berabere!
        return "B"

    def EndGame(self, won:str):
        ## Oyun sonucu
        if won =="B":
            print("Berabere!")
        elif won == self.oyuncu:
            print("Oyuncu kazandı!")
        elif won == self.bot:
            print("Bot kazandı!")
        
        result = self.BoardToStrLine()+won # -> Example: XO OOX OXXO


        ## Listede var mı kontrol et varsa pass geç
        with open("results.txt","r") as f :
            for line in f.readlines():
                line = line.rstrip("\n\r")
                if line == result:
                    return
        ## Listede yoksa ekle
        with open("results.txt","a") as f:
            f.write(f"{result}\n")

    ## Kutucuğu işaretler
    def SetBox(self, index):
        self.boxs[index] = self.oyuncu if self.isPlayer else self.bot

    ## Oyun tahtasını temizler
    def Clear(self):
        self.boxs = [" "]*9

    ## Boş kutuların indexklerini al
    def GetEmptyBoxes(self):
        emptyBoxs = []
        for i in range(9):
            if self.boxs[i] == " ":
                emptyBoxs.append(i)
        return emptyBoxs



    ## Oyun tahtasını tek satırlık data'ya çevir
    def BoardToStrLine(self):
        line = ""
        for i in self.boxs:
            line+=i
        return line


class Player():
    def __init__(self, board: Board) -> None:
        self.board = board

    ## Kullanıcıdan index iste
    def AskIndex(self):
        while True:
            try:
                index = int(input("İndex>>:"))
                break
            except:
                pass
        if 6<index:
            index-=6
        elif index<4:
            index+=6
        return index -1
    
    def Play(self):
        return self.AskIndex()

    def RandomPlay(self):
        emptyBoxs = self.board.GetEmptyBoxes()
        return int(random.choice(emptyBoxs))
    

class Bot():
    isLearning = False ## False -> AI | True -> Random Learning
    def __init__(self, board:Board) -> None:
        self.board = board

    def Play(self):
        if self.isLearning:
            emptyBoxs = self.board.GetEmptyBoxes()
            return int(random.choice(emptyBoxs))
        else:
            return self.Calculate()
    
    ## Yapay zeka kazanma olasılığı hesaplayıcısı
    def Calculate(self):
        boardLine = board.BoardToStrLine()
        stateLines = []
        
        with open("results.txt","r") as f:
            for line in f.readlines():
                line.rstrip("\n\r")
                state = True
                if len(line)!=11:
                    continue
                for i in range(9):
                    if boardLine[i] !=" ":
                        if line[i] != boardLine[i]:
                            state=False
                if state:
                    stateLines.append(line)

        emptyBoxes = self.board.GetEmptyBoxes()
        boardState = [0]*len(emptyBoxes)
        for line in stateLines:
            empty=0
            for c in line:
                if c==" ":
                    empty+=1
            for i in emptyBoxes:
                if line[i] == "O":
                    ind = emptyBoxes.index(i)
                    if line[9] == "O":
                        boardState[ind]+=1*empty
                    if line[9] == "B":
                        boardState[ind]+=0
                    if line[9] == "X":
                        boardState[ind]-=1*empty
                elif line[i] == "X":
                    ind = emptyBoxes.index(i)
                    if line[9] == "O":
                        boardState[ind]-=1*empty
                    if line[9] == "B":
                        boardState[ind]+=0
                    if line[9] == "X":
                        boardState[ind]+=1*empty

        # # Debugger Table
        # boxs = [" "]*9
        # for i in range(len(emptyBoxes)):
        #     boxs[emptyBoxes[i]]=boardState[i]

        # for i in range(3):
        #     print("___"*4+"_")  
        #     print(f"| {boxs[i*3]} | {boxs[i*3+1]} | {boxs[i*3+2]} |")
        # print("___"*4+"_")


        return emptyBoxes[boardState.index(max(boardState))]


board = Board()
bot = Bot(board)

print("Oynayacak mısınız? / Are you player?")
inp = input("(Y\\N): ")
if inp.lower()=="y":
    player = Player(board)
else:
    player = Bot(board)
    player.isLearning = True

from os.path import exists

if not exists("results.txt"):
    with open("results.txt","w"):
        pass


while True:
    board.Display()
    board.isPlayer = True
    index = player.Play()
    if index not in board.GetEmptyBoxes():
        continue
    board.SetBox(index)
    if board.isFinish():
        board.EndGame(board.isFinish())
        board.Display()
        board.Clear()
        continue

    board.isPlayer = False
    board.SetBox(bot.Play())
    if board.isFinish():
        board.EndGame(board.isFinish())
        board.Display()
        board.Clear()
    
    
