follow={
  'Program': [ '\x00' ],
  'Declaration-list': [
    '$',      '{',
    ';',      'break',
    'if',     'repeat',
    'return', 'ID',
    '(',      'NUM',
    '}'
  ],
  'Declaration': [
    'int',    'void',
    '$',      '{',
    ';',      'break',
    'if',     'repeat',
    'return', 'ID',
    '(',      'NUM',
    '}'
  ],
  'Declaration-initial': [ '(', ';', '[' ],
  'Declaration-prime': [
    'int',    'void',
    '$',      '{',
    ';',      'break',
    'if',     'repeat',
    'return', 'ID',
    '(',      'NUM',
    '}'
  ],
  'Var-declaration-prime': [
    'int',    'void',
    '$',      '{',
    ';',      'break',
    'if',     'repeat',
    'return', 'ID',
    '(',      'NUM',
    '}'
  ],
  'Fun-declaration-prime': [
    'int',    'void',
    '$',      '{',
    ';',      'break',
    'if',     'repeat',
    'return', 'ID',
    '(',      'NUM',
    '}'
  ],
  'Type-specifier': [ 'ID' ],
  'Params': [ ')' ],
  'Para': [ ')' ],
  'Param': [],
  'Param-prime': [ ',', ')' ],
  'Compound-stmt': [
    'int',   'void',   '$',
    '{',     ';',      'break',
    'if',    'repeat', 'return',
    'ID',    '(',      'NUM',
    '}',     'endif',  'else',
    'until'
  ],
  'Statement-list': [ '}' ],
  'Statement': [
    '{',      ';',
    'break',  'if',
    'repeat', 'return',
    'ID',     '(',
    'NUM',    '}',
    'endif',  'else',
    'until'
  ],
  'Expression-stmt': [
    '{',      ';',
    'break',  'if',
    'repeat', 'return',
    'ID',     '(',
    'NUM',    '}',
    'endif',  'else',
    'until'
  ],
  'Selection-stmt': [
    '{',      ';',
    'break',  'if',
    'repeat', 'return',
    'ID',     '(',
    'NUM',    '}',
    'endif',  'else',
    'until'
  ],
  'Else-stmt': [
    '{',      ';',
    'break',  'if',
    'repeat', 'return',
    'ID',     '(',
    'NUM',    '}',
    'endif',  'else',
    'until'
  ],
  'Iteration-stmt': [
    '{',      ';',
    'break',  'if',
    'repeat', 'return',
    'ID',     '(',
    'NUM',    '}',
    'endif',  'else',
    'until'
  ],
  'Return-stmt': [
    '{',      ';',
    'break',  'if',
    'repeat', 'return',
    'ID',     '(',
    'NUM',    '}',
    'endif',  'else',
    'until'
  ],
  'Return-stmt-prime': [
    '{',      ';',
    'break',  'if',
    'repeat', 'return',
    'ID',     '(',
    'NUM',    '}',
    'endif',  'else',
    'until'
  ],
  'Expression': [ ';', ')', ']', ',' ],
  'B': [ ';', ')', ']', ',' ],
  'H': [ ';', ')', ']', ',' ],
  'Simple-expression-zegond': [ ';', ')', ']', ',' ],
  'Simple-expression-prime': [ ';', ')', ']', ',' ],
  'C': [ ';', ')', ']', ',' ],
  'Relop': [ '( ', 'ID', 'NUM' ],
  'Additive-expression': [ ';', ')', ']', ',' ],
  'Additive-expression-prime': [ '<', '==', ';', ')', ']', ',' ],
  'Additive-expression-zegond': [ '<', '==', ';', ')', ']', ',' ],
  'D': [ '<', '==', ';', ')', ']', ',' ],
  'Addop': [],
  'Term': [ 'Addop ', ';', ')', '<', '==', ']', ',' ],
  'Term-prime': [ 'Addop ', '<', "TODO", ';', ')', ']', ',' ],
  'Term-zegond': [ 'Addop ', '<', '==', ';', ')', ']', ',' ],
  'G': [ 'Addop ', '<', '==', ';', ')', ']', ',' ],
  'Factor': [ '*', 'Addop ', ';', ')', '<', '==', ']', ',' ],
  'Var-call-prime': [ '*', 'Addop ', ';', ')', '<', '==', ']', ',' ],
  'Var-prime': [ '*', 'Addop ', ';', ')', '<', '==', ']', ',' ],
  'Factor-prime': [ '*', 'Addop ', '<', '==', ';', ')', ']', ',' ],
  'Factor-zegond': [ '*', 'Addop ', '<', '==', ';', ')', ']', ',' ],
  'Args': [ ')' ],
  'Arg-list': [ ')' ],
  'Arg-list-prime': [ ')' ]
}
