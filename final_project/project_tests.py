import unittest
from project_classes import Die, Game, Analyzer
import numpy as np
import pandas as pd


class TestDie(unittest.TestCase):

    def setUp(self):
        self.test_die=Die(np.array([1,2,3,4,5,6]))

    def test1_init_(self):
        
        self.assertIsInstance(self.test_die._die,pd.DataFrame)

    def test2_change_weight(self):
        self.test_die.change_weight(1,2)
        expected=2
        check=self.test_die._die.loc[1,'weights']
        self.assertEqual(check,expected)

    def test3_roll(self):
        check=self.test_die.roll(10)
        test=len(check)
        expected=10
        self.assertEqual(test,expected)


    def test4_show_die(self):
        check=list(self.test_die.show_die().index)
        expected=[1,2,3,4,5,6]
        self.assertEqual(check,expected)


class TestGame(unittest.TestCase):

    def setUp(self):
        self.test_die1 = Die(np.array([1,2,3,4,5,6]))
        self.test_die2 = Die(np.array([1,2,3,4,5,6]))
        self.test_die3 = Die(np.array([1,2,3,4,5,6]))
        self.test_unfair_die1 = Die(np.array([1,2,3,4,5,6]))
        self.test_unfair_die2 = Die(np.array([1,2,3,4,5,6]))
        self.test_game = Game([self.test_die1, self.test_die2, self.test_die3, self.test_unfair_die1, self.test_unfair_die2])


    def test5_init_(self):
        self.assertTrue(len(self.test_game.dice),5)

    def test6_play(self):
        self.test_game.play(1000)
        check=self.test_game._results
        shape=check.shape
        col_expected=5
        row_expected=1000
        self.assertEqual(shape[0],row_expected)
        self.assertEqual(shape[1],col_expected)

    def test7_results(self):
        self.test_game.play(1000)
        checkwide=self.test_game.results('wide')
        checknarrow=self.test_game.results('narrow')
        
        ##Check Wide
        wide_col_expected=5
        wide_row_expected=1000
        shape=checkwide.shape
        self.assertEqual(shape[0],wide_row_expected)
        self.assertEqual(shape[1],wide_col_expected)

        ##Check Narrow
        narrow_col_expected=1
        narrow_row_expected=5000
        shape=checknarrow.shape
        self.assertEqual(shape[0],narrow_row_expected)
        self.assertEqual(shape[1],narrow_col_expected)


class TestAnalyzer (unittest.TestCase):

    def setUp(self):
        self.alph_die=Die(np.array(['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S',
                       'T','U','V','W','X','Y','Z']))
        letter_prob=pd.read_table('english_letters.txt',names=['Count'],index_col=0,header=None,delimiter=' ')
        letter_prob['prob']=letter_prob.Count/sum(letter_prob.Count)
        for i in letter_prob.index:
            self.alph_die.change_weight(i,letter_prob.loc[i,'prob'])
        self.test_game=Game([self.alph_die,self.alph_die,self.alph_die,self.alph_die])
        self.test_game.play(1000)
        self.test_analyze=Analyzer(self.test_game)

    def test8__init__(self):
        self.assertEqual(len(self.test_analyze._results),1000)

    def test9_jackpot(self):
        self.assertGreaterEqual(self.test_analyze.jackpot(),0)

    def test10_face_counts(self):
        self.assertEqual(len(self.test_analyze.face_counts()),1000)
        self.assertIsInstance(self.test_analyze.face_counts(),pd.DataFrame)

    def test11_combocounts (self):
        test=self.test_analyze.combo_count()
        self.assertEqual(test['count'].sum(),1000)
        self.assertIsInstance(self.test_analyze.combo_count(),pd.DataFrame)

    def test12_permcounts (self):
        self.assertGreaterEqual(len(self.test_analyze.perm_count()),0)
        self.assertIsInstance(self.test_analyze.perm_count(),pd.DataFrame)

if __name__ == '__main__':
    unittest.main()
