

from enum import Enum

class Color(Enum):
    lSql = 1

    lChar = 2 #char
    lFloat = 3 #flaot
    lInteger = 3 #integer

    lReplace = 11
    lCreate = 12
    lAlter = 13
    lDrop = 14

    lIdentifier = 123

    lConstFloat = 301
    lConstInteger = 302
    lConstString = 303

    lEndOfFile = 965
    lError = 987
 
class Scanner:
    _maxLexemSize = 130
    _spaceChars = [' ', '\n', '\t', '\r']
    
    def __init__(self, sourceText):
        self.SourceText = sourceText
        self._position = 0

    def scan(self):
        _position = self._position;
        _codeText = self.SourceText;

        try:
            while (_codeText[_position] in self._spaceChars):
                _position += 1;

            currChar = _codeText[_position].upper()
            if ((currChar == '-') & (_codeText[_position + 1] == '-')):
                _position += 2;
                while (_codeText[_position] not in ['\n', '\r']):
                    _position += 1;

                self._position = _position;
                return self.scan();

            #Комментарий вида /* ... */
            if ((currChar == '/') & (_codeText[_position + 1] == '*')):
                _position += 2;
                while True:
                    _position += 1;
                    if ((_codeText[_position] != '/') | (_codeText[_position - 1] != '*')):
                        break;
                
                self._position = _position;
                return self.scan();
            
            if (currChar == '\0'):
                return (Lexem.lEndOfFile, "Конец исходного текста")

            if (currChar >= '0' & currChar <= '9'):
                _position += 1;
                currChar = _codeText[_position]
                
                while ((currChar >= '0') & (currChar <= '9')):
                    _position += 1;
                    currChar = _codeText[_position];
                                
                if (currChar == '.'):
                    _position += 1;
                    currChar = _codeText[_position];
                    while ((currChar >= '0') & (currChar <= '9')):
                        _position += 1;
                        currChar = _codeText[_position];

                    lexemKind = Lexem.lConstFloat;
                else:
                    lexemKind = Lexem.lConstInteger;

                lexemView = _codeText[self._position, _position]
                self._position = _position;
                return (lexemKind, lexemView);                    

                if (i > self._maxLexemSize):
                    return (Lexem.lError, u'Слишком длинная лексема')

            if (currChar == "'"):
                _position += 1;
                endChar = "'"
                while ((_codeText[_position] != endChar) | ((_codeText[_position] == endChar) & (_codeText[_position + 1] == endChar))):
                    _position += 1;

                lexemView = _codeText[self._position, _position]
                self._position = _position;
                return (Lexem.lConstString, lexemView);
                        
            if (currChar == '"'):
                _position += 1;
                endChar = '"'
                while ((_codeText[_position] != endChar) | ((_codeText[_position] == endChar) & (_codeText[_position + 1] == endChar))):
                    _position += 1;
                
                lexemView = _codeText[self._position, _position]
                self._position = _position;
                return (Lexem.lIdentifier, lexemView);

            if ((currChar >= 'a' and currChar <= 'z') or
                    (currChar >= 'A' & currChar <= 'Z') or
                    (currChar in ['_', '$', '#'])):
                
                _position += 1;
                currChar = _codeText[_position];
                while ((currChar >= '0' and currChar <= '9') or
                        (currChar >= 'a' and currChar <= 'z') or
                        (currChar >= 'A' and currChar <= 'Z') or
                        (currChar == '_')):
                    _position += 1;
                    currChar = _codeText[_position];
                
                _position -= 1;

                if (_position - self._position > self._maxLexemSize):                
                    return (Lexem.lError, "Слишком длинная лексема")
                
                
                
        except IndexError:
            return (Lexem.lEndOfFile, "Конец исходного текста")
        
sql = u'replace view prd3_db_dwh.v_oca as sel top 1 * from prd3_vd_djj.t_coa'
scanner = Scanner(sql)

scanner.scan();
