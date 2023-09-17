from langdetect import detect
import regex

def isKorea(value):
    if regex.search(r'\p{IsHangul}', value):
        return True
    return False

def isThai(value):
    if regex.search(r'\p{IsThai}', value):
        return True
    return False

def isJapanChina(value):
    if regex.search(r'([\p{IsHan}\p{IsBopo}\p{IsHira}\p{IsKatakana}]+)', value):
        return True
    return False

def isRussia(value):
    if regex.search(r'\p{IsCyrillic}', value):
        return True
    return False

def isIsreal(value):
    if regex.search(r'\p{IsHebrew}', value):
        return True
    return False

def isLatin(value):
    if regex.search(r'\p{IsLatin}', value):
        return True
    return False

#def isIndia(value):
#    if regex.search(r'\p{isTamil}', value):
#        return True
#    return False
    
def isAscii(name):
    if name is None:
        return None
    try:
        retval = len(name) == len(name.encode())
    except:
        retval = None
    return retval




#####################################################################################################################
# Uses LangDetect
#####################################################################################################################
class stringInfo:
    def __init__(self, name, debug=False):
        self.name  = name
        self.debug = debug
        self.err   = None
        self.lang  = None
        
        self.isNone()        
        
        ##### General
        self.ascii   = self.isAscii()
        self.special = self.isSpecial()
        self.numeric = self.isNumeric()
        
        ##### Lang
        self.setLang()
        
        ##### Slavic
        self.slavic    = self.isSlavic()
        
        #####
        self.japanese  = self.isJapanese()
        self.korean    = self.isKorean()
        self.chinese   = self.isChinese()
        self.eastasia  = self.isEastAsia()
        
        #####
        self.greek     = self.isGreek()
        
        #####
        self.english   = self.isEnglish()
        self.french    = self.isFrench()
        self.italian   = self.isItalian()
        self.german    = self.isGerman()
        self.dutch     = self.isDutch()
        self.spanish   = self.isSpanish()
        self.portugese = self.isPortugese()
        self.iberian   = self.isIberian()
        self.european  = self.isEuropean()
        
        #####
        self.danish       = self.isDanish()
        self.swedish      = self.isSwedish()
        self.norwegian    = self.isNorwegian()
        self.icelandic    = self.isIcelandic()
        self.finnish      = self.isFinnish()
        self.scandinavian = self.isScandinavian()
        
        #####
        self.other = None
        if self.err is not None:
            if self.special | self.numeric:
                self.other = False
            else:
                try:
                    if (self.slavic | self.eastasia | self.greek | self.european | self.scandinavian):
                        self.other = True
                    else:
                        self.other = False
                except:
                    self.show()
        
        
    def show(self):
        print("{0: <15}: {1}".format("String",self.name))
        print("{0: <15}: {1}".format("  Language",self.lang))
        print("{0: <15}: {1}".format("  General",""))
        print("{0: <15}: {1}".format("    Ascii",self.ascii))
        print("{0: <15}: {1}".format("    Numeric",self.numeric))
        print("{0: <15}: {1}".format("    Special",self.special))
        print("{0: <15}: {1}".format("  Slavic", self.slavic))
        print("{0: <15}: {1}".format("  EastAsia", self.eastasia))
        print("{0: <15}: {1}".format("    Japanese", self.japanese))
        print("{0: <15}: {1}".format("    Korean", self.korean))
        print("{0: <15}: {1}".format("    Chinese", self.chinese))
        print("{0: <15}: {1}".format("  Greek",self.greek))
        print("{0: <15}: {1}".format("  European",self.european))        
        print("{0: <15}: {1}".format("    English",self.english))
        print("{0: <15}: {1}".format("    French",self.french))
        print("{0: <15}: {1}".format("    Italian",self.italian))
        print("{0: <15}: {1}".format("    German",self.german))
        print("{0: <15}: {1}".format("    Dutch",self.dutch))
        print("{0: <15}: {1}".format("    Iberian",self.iberian))
        print("{0: <15}: {1}".format("      Spanish",self.spanish))
        print("{0: <15}: {1}".format("      Portugese",self.portugese))
        print("{0: <15}: {1}".format("  Scandinavian",self.scandinavian))
        print("{0: <15}: {1}".format("    Danish",self.danish))
        print("{0: <15}: {1}".format("    Swedish",self.swedish))
        print("{0: <15}: {1}".format("    Norwegian",self.norwegian))
        print("{0: <15}: {1}".format("    Icelandic",self.icelandic))
        print("{0: <15}: {1}".format("    Finnish",self.finnish))
        print("{0: <15}: {1}".format("  Other",self.other))
        print("{0: <15}: {1}".format("  Err",self.err))

        
        
    def isNone(self):
        if self.name is None:
            self.err = "None"
            
    def setLang(self):
        if self.err is not None:
            return None
        try:
            self.lang = detect(self.name)
        except:
            self.err = "NoLang"
        
    
    def isAscii(self):
        if self.err is not None:
            return None
        return len(self.name) == len(self.name.encode())
    
    def isNumeric(self):
        try:
            int(self.name)
            self.err = "Numeric"
            return True
        except:
            return False
        
    def isSpecial(self):
        if self.err is not None:
            return None
        if sum([x in self.name for x in ['+', '[', ']', '(', ')', ":", '-', "'", '@', '°', '.', '-', '!', 'º']]) > 0:
            self.err = "Special"
            return True
        return False

    
    ########################################################################################################
    # Slavic
    ########################################################################################################
    def isSlavic(self):
        if self.err is not None:
            return None
        return self.lang in ['ru', 'uk', 'sr', 'ce', 'ab']

    
    ########################################################################################################
    # Scandinavian
    ########################################################################################################
    def isDanish(self):
        if self.err is not None:
            return None
        return self.lang in ['da']

    def isSwedish(self):
        if self.err is not None:
            return None
        return self.lang in ['sv']

    def isNorwegian(self):
        if self.err is not None:
            return None
        return self.lang in ['nb', 'nn', 'no']

    def isIcelandic(self):
        if self.err is not None:
            return None
        return self.lang in ['is']

    def isFinnish(self):
        if self.err is not None:
            return None
        return self.lang in ['fi']
    
    def isScandinavian(self):
        if self.err is not None:
            return None
        return (self.danish | self.swedish | self.norwegian | self.icelandic | self.finnish)

    
    ########################################################################################################
    # East Asia
    ########################################################################################################
    def isJapanese(self):
        if self.err is not None:
            return None
        return self.lang in ['ja']

    def isKorean(self):
        if self.err is not None:
            return None
        return self.lang in ['ko']

    def isChinese(self):
        if self.err is not None:
            return None
        return self.lang in ['zh', 'tw', 'zh-cn', 'zh-tw']
    
    def isEastAsia(self):
        if self.err is not None:
            return None
        return (self.japanese | self.korean | self.chinese)
    
    
    ########################################################################################################
    # East Asia
    ########################################################################################################
    def isGreek(self):
        if self.err is not None:
            return None
        return self.lang in ['he', 'el', 'ar', 'mk']
    
    
    ########################################################################################################
    # English
    ########################################################################################################    
    def isEnglish(self):
        if self.err is not None:
            return None
        return self.lang in ['en']
    
    def isDutch(self):
        if self.err is not None:
            return None
        return self.lang in ['nl']
    
    def isFrench(self):
        if self.err is not None:
            return None
        return self.lang in ['fr']
    
    def isGerman(self):
        if self.err is not None:
            return None
        return self.lang in ['de']

    def isItalian(self):
        if self.err is not None:
            return None
        return self.lang in ['it']

    def isSpanish(self):
        if self.err is not None:
            return None
        return self.lang in ['es']

    def isPortugese(self):
        if self.err is not None:
            return None
        return self.lang in ['pt']

    def isIberian(self):
        if self.err is not None:
            return None
        return (self.spanish | self.portugese)
    
    def isEuropean(self):
        if self.err is not None:
            return None
        return (self.english | self.french | self.german | self.italian | self.dutch | self.iberian)