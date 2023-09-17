""" A simple utility class for measuring timing of processes """

__all__ = ["LangType"]

import regex

class LangType:
    def __init__(self):
        self.funcs = [x for x in dir(self) if x.startswith("get") and x not in ["get"]]

        
    def normRetval(self, x):
        if x is None:
            return False
        elif isinstance(x, bool):
            return x
        return True    
    
    def get(self, value):
        retval = {func[3:]: self.normRetval(getattr(self, func)(value)) for func in self.funcs} if isinstance(value, str) else {}
        return [k for k,v in retval.items() if v is True]
        

    def getLatin(self, value):
        return regex.compile(r"[\p{IsLatin}]+").search(value)
    def getKorean(self, value):
        return regex.compile(r"[\p{IsHangul}]+").search(value)
    def getThai(self, value):
        return regex.compile(r"[\p{IsThai}]+").search(value)
    def getHebrew(self, value):
        return regex.compile(r"[\p{IsHebrew}]+").search(value)
    def getRussian(self, value):
        return regex.compile(r"[\p{IsCyrillic}]+").search(value)
    def getGreek(self, value):
        return regex.compile(r"[α-ωΑ-Ω]+").search(value)
    def getArabic(self, value):
        return regex.compile(r"^[\u0621-\u064A\u0660-\u0669]+$").search(value)
    def getArmenian(self, value):
        return regex.compile(r"[ԱԲԳԴԵԶԷԸԹԺԻԼԽԾԿՀՁՂՃՄՅՆՇՈՉՊՋՌՍՎՏՐՑՒՓՔՕՖ]").search(value)
    def getGeorgian(self, value):
        return regex.compile(r"[აბგდევზჱთიკლმნჲოპჟრსტჳუფქღყშჩცძწჭხჴჯჰჵჶჷჸ]").search(value)
    def getChinese(self, value):
        return regex.compile(r"[\p{IsHan}]+").search(value)
    def getJapanese(self, value):
        return regex.compile(r"[\p{IsHira}\p{IsKatakana}]+").search(value)
    def getJCese(self, value):
        return regex.compile(r"[\p{IsHan}\p{IsBopo}\p{IsHira}\p{IsKatakana}]+").search(value)    
    def getKhmer(self, value):
        return regex.compile(r"[កខគឃងចឆជឈញដឋឌឍណតថទធនបផពភមសហយរលឡអវអ្កអ្ខអ្គអ្ឃអ្ងអ្ចអ្ឆអ្ឈអ្ញអ្ឌអ្ឋអ្ឌអ្ឃអ្ណអ្តអ្ថអ្ទអ្ធអ្នអ្បអ្ផអ្ពអ្ភអ្មអ្សអ្ហអ្យអ្រអ្យអ្លអ្អអ្វអក្សរខ្មែរ]+").search(value)
    def getVietnamese(self, value):
        return regex.compile(r"[ườầ]+").search(value)
    def getSlavic(self, value):
        return regex.compile(r"[ĆćĚěŠšČčŘřŽžÝýďŤťĎŇňŮů]+").search(value)
    def getGerman(self, value):
        return regex.compile(r"[ß]+").search(value)
    def getScandinavian(self, value):
        return regex.compile(r"[æøåÆØÅ]+").search(value)
    def getIcelandic(self, value):
        return regex.compile(r"[ðÐþÞ]+").search(value)
    def getPolish(self, value):
        return regex.compile(r"[ĄąĘęŁłŃńŚśŹźŻż]+").search(value)
    def getFrench(self, value):
        return regex.compile(r"[ÂâÊêËëÎîÏïÔôÛûŸÿçœ]+").search(value)
    def getPortuguese(self, value):
        return regex.compile(r"[ÃãÕõ]+").search(value)
    def getSpanish(self, value):
        return regex.compile(r"[¡ñ]+").search(value)
    def getSpecial(self, value):
        return regex.compile(r"[‒’„“‐ʻēū]+").search(value)
    def getRomanian(self, value):
        return regex.compile(r"[ĂăȘșȚț]+").search(value)
    def getHungarian(self, value):
        return regex.compile(r"[Őő]+").search(value)
    def getUmlaut(self, value):
        return regex.compile(r"[äöüÄÖÜ]+").search(value)
    def getAccentAcute(self, value):
        return regex.compile(r"[ÁáÉéÍíÓóÚú]+").search(value)
    def getAccentGrave(self, value):
        return regex.compile(r"[ÀàÈèÌìÒòÙù]+").search(value)

    def getDJMC(self, value):
        return sum([value.startswith(y) for y in ["DJ ", "Dj ", " DJ", " Dj", "Lil ", "Lil' ", "MC ", "D.J."]]) > 0
    def getClassical(self, value):
        return sum([value.find(y) != -1 for y in ["Theatre", "Theater", "Chorus", "Orchestra"]]) > 0
    def getAnd(self, value):
        return sum([value.find(y) != -1 for y in [" And ", " and ", " & "]]) > 0
    def getSlash(self, value):
        return sum([value.find(y) != -1 for y in ["+", "/", "*", "?", "'"]]) > 0
    def getDash(self, value):
        return sum([value.find(y) != -1 for y in ["-", ".", ","]]) > 0
    def getNumerical(self, value):
        return value.isdigit()
    def getSingleWord(self, value):
        return len(value.split()) == 1
    def getFourWords(self, value):
        return len(value.split()) >= 4