from parser_lib import Parser

IS_DEBUG = True


p = Parser('./data/backup/')
a= p.mi_sleep_parser( number_of_files=0, isDebug=IS_DEBUG )
print(a)