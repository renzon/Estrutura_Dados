# -*- coding: utf-8 -*-

# Exercício de avaliação de expressão aritmética.
# Só podem ser usadas as estruturas Pilha e Fila implementadas em aulas anteriores.
# Deve ter análise de tempo e espaço para função avaliação

import unittest
from aula5.fila import Fila
from aula4.pilha import Pilha


class ErroLexico(Exception):
    pass


class ErroSintatico(Exception):
    pass


def analise_lexica(expressao):
    """
    Executa análise lexica transformando a expressao em fila de objetos:
    Transforma inteiros em ints
    Flutuantes em floats
    e verificar se demais caracteres são validos: +-*/(){}[]
    :param expressao: string com expressao a ser analisada
    :return: fila com tokens
    Complexidade: o(n) em tempo de execução e memória
    """
    fila = Fila()

    #numeros e tokens
    dig = R"0123456789.-+*/{}[]()"

    if expressao:
        aux = ''
        for i in expressao:
            if i in dig:
                if i in '.-+*/{}[]()':
                    if aux:
                        fila.enfileirar(aux)
                        aux = ''
                    fila.enfileirar(i)
                else:
                    aux = aux + i
            else:
                raise ErroLexico()
        if aux:
            fila.enfileirar(aux)
    return fila


def analise_sintatica(fila):
    """
    Função que realiza analise sintática de tokens produzidos por analise léxica.
    Executa validações sintáticas e se não houver erro retorn fila_sintatica para avaliacao
    :param fila: fila proveniente de análise lexica
    :return: fila_sintatica com elementos tokens de numeros
    Complexidade: o(n) em tempo de execução e memória
    """
    if fila.__len__():

     op = '+-*/(){}[]'
    _fila = Fila()
    characteres = ''
    if fila.vazia():
        raise ErroSintatico('')
    while not fila.vazia():
        current = fila.desenfileirar()
        if current in op:
            if len(characteres):
                if '.' not in characteres:
                    _fila.enfileirar(int(characteres))
                else: _fila.enfileirar(float(characteres))
                characteres = ''
            _fila.enfileirar(current)
        else: characteres += current
    if len(characteres):
        if '.' not in characteres: characteres = int(characteres)
        else: characteres = float(characteres)
        _fila.enfileirar(characteres)
    return _fila

def avaliar(expressao):
    """
    Função que avalia expressão aritmetica retornando se valor se não houver nenhum erro
    :param expressao: string com expressão aritmética
    :return: valor númerico com resultado
    Complexidade: o(n) em tempo de execução e memória
    """
    if expressao:
        fila = analise_sintatica(analise_lexica(expressao))
        tamanho = len(fila)
        if tamanho == 1:
            return fila.primeiro()
        pilha = Pilha()
        for n in range(tamanho):
            pilha.empilhar(fila._deque[n])
            if pilha.__len__() > 2 and str(pilha.topo()) not in '-+*/(){}[]':
                valor = pilha.topo()
                pilha.desempilhar()
                if pilha.topo() == '+':
                    pilha.desempilhar()
                    valor = pilha.desempilhar() + valor
                elif pilha.topo() == '-':
                    pilha.desempilhar()
                    valor = pilha.desempilhar() - valor
                elif pilha.topo() == '*':
                    pilha.desempilhar()
                    valor = pilha.desempilhar() * valor
                elif pilha.topo() == '/':
                    pilha.desempilhar()
                    valor = pilha.desempilhar() / valor
                pilha.empilhar(valor)
            elif str(pilha.topo()) in ')}]' and n == tamanho - 1:
                pilha.desempilhar()
                while len(pilha) > 1:
                    if str(pilha.topo()) not in '-+*/(){}[]':
                        valor = pilha.topo()
                        pilha.desempilhar()
                        if pilha.topo() == '+':
                            pilha.desempilhar()
                            valor = pilha.desempilhar() + valor
                        elif pilha.topo() == '-':
                            pilha.desempilhar()
                            valor = pilha.desempilhar() - valor
                        elif pilha.topo() == '*':
                            pilha.desempilhar()
                            valor = pilha.desempilhar() * valor
                        elif pilha.topo() == '/':
                            pilha.desempilhar()
                            valor = pilha.desempilhar() / valor
                        elif str(pilha.topo()) in '(){}[]':
                            pilha.desempilhar()
                        pilha.empilhar(valor)
                    else:
                        pilha.desempilhar()
        return pilha.topo()
    raise ErroSintatico()

class AnaliseLexicaTestes(unittest.TestCase):
    def test_expressao_vazia(self):
        fila = analise_lexica('')
        self.assertTrue(fila.vazia())

    def test_caracter_estranho(self):
        self.assertRaises(ErroLexico, analise_lexica, 'a')
        self.assertRaises(ErroLexico, analise_lexica, 'ab')

    def test_inteiro_com_um_algarismo(self):
        fila = analise_lexica('1')
        self.assertEqual('1', fila.desenfileirar())
        self.assertTrue(fila.vazia())

    def test_inteiro_com_vários_algarismos(self):
        fila = analise_lexica('1234567890')
        self.assertEqual('1234567890', fila.desenfileirar())
        self.assertTrue(fila.vazia())

    def test_float(self):
        fila = analise_lexica('1234567890.34')
        self.assertEqual('1234567890', fila.desenfileirar())
        self.assertEqual('.', fila.desenfileirar())
        self.assertEqual('34', fila.desenfileirar())
        self.assertTrue(fila.vazia())

    def test_parenteses(self):
        fila = analise_lexica('(1)')
        self.assertEqual('(', fila.desenfileirar())
        self.assertEqual('1', fila.desenfileirar())
        self.assertEqual(')', fila.desenfileirar())
        self.assertTrue(fila.vazia())

    def test_chaves(self):
        fila = analise_lexica('{(1)}')
        self.assertEqual('{', fila.desenfileirar())
        self.assertEqual('(', fila.desenfileirar())
        self.assertEqual('1', fila.desenfileirar())
        self.assertEqual(')', fila.desenfileirar())
        self.assertEqual('}', fila.desenfileirar())
        self.assertTrue(fila.vazia())

    def test_colchetes(self):
        fila = analise_lexica('[{(1.0)}]')
        self.assertEqual('[', fila.desenfileirar())
        self.assertEqual('{', fila.desenfileirar())
        self.assertEqual('(', fila.desenfileirar())
        self.assertEqual('1', fila.desenfileirar())
        self.assertEqual('.', fila.desenfileirar())
        self.assertEqual('0', fila.desenfileirar())
        self.assertEqual(')', fila.desenfileirar())
        self.assertEqual('}', fila.desenfileirar())
        self.assertEqual(']', fila.desenfileirar())
        self.assertTrue(fila.vazia())

    def test_adicao(self):
        fila = analise_lexica('1+2.0')
        self.assertEqual('1', fila.desenfileirar())
        self.assertEqual('+', fila.desenfileirar())
        self.assertEqual('2', fila.desenfileirar())
        self.assertEqual('.', fila.desenfileirar())
        self.assertEqual('0', fila.desenfileirar())
        self.assertTrue(fila.vazia())

    def test_subtracao(self):
        fila = analise_lexica('1-2.0')
        self.assertEqual('1', fila.desenfileirar())
        self.assertEqual('-', fila.desenfileirar())
        self.assertEqual('2', fila.desenfileirar())
        self.assertEqual('.', fila.desenfileirar())
        self.assertEqual('0', fila.desenfileirar())
        self.assertTrue(fila.vazia())

    def test_multiplicacao(self):
        fila = analise_lexica('1*2.0')
        self.assertEqual('1', fila.desenfileirar())
        self.assertEqual('*', fila.desenfileirar())
        self.assertEqual('2', fila.desenfileirar())
        self.assertEqual('.', fila.desenfileirar())
        self.assertEqual('0', fila.desenfileirar())
        self.assertTrue(fila.vazia())

    def test_divisao(self):
        fila = analise_lexica('1/2.0')
        self.assertEqual('1', fila.desenfileirar())
        self.assertEqual('/', fila.desenfileirar())
        self.assertEqual('2', fila.desenfileirar())
        self.assertEqual('.', fila.desenfileirar())
        self.assertEqual('0', fila.desenfileirar())
        self.assertTrue(fila.vazia())

    def test_expresao_com_todos_simbolos(self):
        expressao = '1/{2.0+3*[7-(5-3)]}'
        fila = analise_lexica(expressao)
        self.assertListEqual(list(expressao), [e for e in fila])
        self.assertTrue(fila.vazia())


class AnaliseSintaticaTestes(unittest.TestCase):
    def test_fila_vazia(self):
        fila = Fila()
        self.assertRaises(ErroSintatico, analise_sintatica, fila)

    def test_int(self):
        fila = Fila()
        fila.enfileirar('1234567890')
        fila_sintatica = analise_sintatica(fila)
        self.assertEqual(1234567890, fila_sintatica.desenfileirar())
        self.assertTrue(fila_sintatica.vazia())

    def test_float(self):
        fila = Fila()
        fila.enfileirar('1234567890')
        fila.enfileirar('.')
        fila.enfileirar('4')
        fila_sintatica = analise_sintatica(fila)
        self.assertEqual(1234567890.4, fila_sintatica.desenfileirar())
        self.assertTrue(fila_sintatica.vazia())

    def test_expressao_com_todos_elementos(self):
        fila = analise_lexica('1000/{222.125+3*[7-(5-3)]}')
        fila_sintatica = analise_sintatica(fila)
        self.assertListEqual([1000, '/', '{', 222.125, '+', 3, '*', '[', 7, '-', '(', 5, '-', 3, ')', ']', '}'],[e for e in fila_sintatica])


class AvaliacaoTestes(unittest.TestCase):
    def test_expressao_vazia(self):
        self.assertRaises(ErroSintatico, avaliar, '')

    def test_inteiro(self):
        self.assert_avaliacao('1')

    def test_float(self):
        self.assert_avaliacao('2.1')

    def test_soma(self):
        self.assert_avaliacao('2+1')

    def test_subtracao_e_parenteses(self):
        self.assert_avaliacao('(2-1)')

    def test_expressao_com_todos_elementos(self):
        self.assertEqual(1.0, avaliar('2.0/[4*3+1-{15-(1+3)}]'))

    def assert_avaliacao(self, expressao):
        self.assertEqual(eval(expressao), avaliar(expressao))


if __name__ == '__main__':
    unittest.main()
