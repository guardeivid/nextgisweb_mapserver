# -*- coding: utf-8 -*-

'''Лексический анализатор
'''

import re
import ply.lex as lex


class CharNotRecognizedError(Exception):
    pass


tokens = (
    'NUMBER',
    'IDENTIFIER',
    'LOGIC_OPERATOR',
    'OPERATOR',
    'STRING_OPERATOR',
    #'QUOTE',
    #'DOUBLEQUOTE',
    'LBRAC',
    'RBRAC',
    'STRING'
)


t_NUMBER = ur'[+-]?(\d+)?\.\d+([Ee][+-]?\d+)?|[+-]?\d+?\.([Ee][+-]?\d+)?|[+-]?\d+'
t_IDENTIFIER = ur'\[[A-Z_]+[A-Z0-9_:-]*\]'
t_LOGIC_OPERATOR = ur'(and)|(or)|(&&)|(\|)'
t_OPERATOR = ur'(!=)|(>=)|(<=)|(<)|(>)|(=\*)|(=)|(lt)|(gt)|(ge)|(le)|(eq)|(ne)'
t_STRING_OPERATOR = ur'(~\*)|(~)'
# t_QUOTE = ur"'"
# t_DOUBLEQUOTE = ur'"'
t_LBRAC = ur'\('
t_RBRAC = ur'\)'
t_STRING = ur"('[^\']*')|(\"[^\"]*\")"


# Символы, которые будут игнорироваться
t_ignore = u' \t'


# Правило для обработки ошибок
def t_error(t):
    # err_char = t.value[0].decode('utf-8', 'replace')
    msg = u"Illegal character"
    raise CharNotRecognizedError(msg)


# Лексический анализатор
lexer = lex.lex(reflags=re.IGNORECASE+re.UNICODE)


if __name__ == "__main__":
    # Тестирование

    ##########################
    # Вспомогательные функции
    ##########################
    def _tuple_to_token(t):
        assert len(t) == 3

        token = lex.LexToken()
        token.type = t[0]
        token.value = t[1]
        token.lexpos = t[2]
        token.lineno = 1

        return token

    def get_tokens(token):
        tokens = []
        lexer.input(token)

        # Tokenize
        while True:
            tok = lexer.token()
            # print tok
            if not tok:
                return tokens
            tokens.append(tok)

    def check_token_eq(token_list, expected_token_list):
        # print 'list:', token_list
        # print 'expd:', expected_token_list
        assert (len(token_list) == len(expected_token_list))

        expected_token_list = [
            _tuple_to_token(t) for t in expected_token_list
        ]
        for i in range(len(token_list)):
            token = token_list[i]
            expected = expected_token_list[i]
            # print 'recived ', token
            # print 'expected', expected
            assert (token.type == expected.type)
            assert (token.value == expected.value)
            assert (token.lexpos == expected.lexpos)

    #######################
    # Тесты
    #######################

    # data = {'входная строка': список ожидаемых токенов}
    data = {
		# Число:
		u"-23 34.4 24 -4.5 +2.3E-1 -2. +.4E+3 .4E3":
		#u"-23 34.4":
			[
				('NUMBER', u'-23', 0),
				('NUMBER', u'34.4', 4),
				('NUMBER', u'24', 9),
				('NUMBER', u'-4.5', 12),
				('NUMBER', u'+2.3E-1', 17),
				('NUMBER', u'-2.', 25),
				('NUMBER', u'+.4E+3', 29),
				('NUMBER', u'.4E3', 36),
			],
        # Много разных токенов в одной строке
        u"([POPULATION] > 50000 AND '[LANGUAGE9]' eq 'FRENCH')":
            [
                ('LBRAC', u'(', 0),
                ('IDENTIFIER', u'[POPULATION]', 1),
                ('OPERATOR', u'>', 14),
                ('NUMBER', u'50000', 16),
                ('LOGIC_OPERATOR', u'AND', 22),
                ('STRING', u"'[LANGUAGE9]'", 26),
                ('OPERATOR', u'eq', 40),
                ('STRING', u"'FRENCH'", 43),
                ('RBRAC', u')', 51)
            ],
        # Кавычки
        u"('[LANGUAGE]' eq 'FRENCH2')":
            [
                ('LBRAC', u'(', 0),
                ('STRING', u"'[LANGUAGE]'", 1),
                ('OPERATOR', u'eq', 14),
                ('STRING', u"'FRENCH2'", 17),
                ('RBRAC', u')', 26)
            ],
        # Двойные кавычки
        u'("[LANGUAGE]" eq "FRENCH2")':
            [
                ('LBRAC', u'(', 0),
                ('STRING', u'"[LANGUAGE]"', 1),
                ('OPERATOR', u'eq', 14),
                ('STRING', u'"FRENCH2"', 17),
                ('RBRAC', u')', 26)
            ],
        # Кавычки внутри строки
        u'''("[LANGUAGE]" eq "FR 'w'2")''':
            [
                ('LBRAC', u'(', 0),
                ('STRING', u'"[LANGUAGE]"', 1),
                ('OPERATOR', u'eq', 14),
                ('STRING', u'"FR \'w\'2"', 17),
                ('RBRAC', u')', 26)
            ],
        # Строковый оператор
        u"('[attr]' =* 'aa=(a)')":
            [
                ('LBRAC', u'(', 0),
                ('STRING', u"'[attr]'", 1),
                ('OPERATOR', u'=*', 10),
                ('STRING', u"'aa=(a)'", 13),
                ('RBRAC', u')', 21)
            ],
        # Просто строка с пробелами
        u"'   '":
            [
                ('STRING', "'   '", 0)
            ]
    }

    # Give the lexer some input
    for line, expected in data.iteritems():
        print
        print 'line:', line
        lexer.input(line)

        recived_tokens = get_tokens(line)
        # print 'Tokens', recived_tokens
        check_token_eq(recived_tokens, expected)



