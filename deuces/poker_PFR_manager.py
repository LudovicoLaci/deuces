#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 18:30:40 2020

@author: ludovicolaci
"""
### Imports ###
from subprocess import run
import random
import poker
import pandas as pd
import ast
from poker import Hand
#from poker import Suit

### position (key) : ranges 'str' form (value)'

BENCB789_OPEN_RANGES_DATABASE =     {
                                    
                                    '10BB': {
                                        
                                      'UTG' : { 'OPEN_SHOVE':'44+,A7s+,A5s-A4s,KTs+,QTs+,JTs,T9s,ATo+,KQo',
                                                'BORDER_RANGE':'33-22,A6s,A3s-A2s,K9s-K6s,Q9s-Q8s,J9s-J8s,T8s-T7s,97s+,86s+,75s+,65s,54s,43s,A9o-A7o,KJo-KTo,QTo+,JTo'
                                              },
                                      'UTG+1' : {'OPEN_SHOVE':'33+,A2s+,K9s+,Q9s+,J9s+,T9s,ATo+,KJo+',
                                                 'BORDER_RANGE':'22,K8s-K2s,Q8s-Q6s,J8s-J7s,T8s-T7s,97s+,87s,76s,65s,A9o-A5o,KTo-K9o,QTo+,JTo,T9o'
                                              },
                                      'UTG+2' : {'OPEN_SHOVE':'22+,A2s+,K9s+,Q9s+,J9s+,T9s,ATo+,KJo+,QJo',
                                                 'BORDER_RANGE':'K8s-K2s,Q8s,J8s,T8s,98s,87s,76s,65s,54s,A9o-A4o,KTo-K9o,QTo-Q9o,J9o+,T9o'
                                              },
                                      'MP' : {'OPEN_SHOVE':'22+,A2s+,K9s+,Q9s+,J9s+,T8s+,98s,A8o+,KTo+,QJo',
                                              'BORDER_RANGE':'K8s-K2s,Q8s-Q5s,J8s-J7s,T7s,97s,87s,76s,65s,54s,A7o-A2o,K9o-K8o,QTo-Q9o,J9o+,T9o'
                                              },
                                      'HJ' : {'OPEN_SHOVE':'22+,A2s+,K8s+,Q8s+,J8s+,T8s+,97s+,87s,A2o+,KTo+,QTo+,JTo',
                                              'BORDER_RANGE':'K7s-K2s,Q7s-Q2s,J7s-J6s,T7s-T6s,96s,86s,75s+,65s,54s,K9o-K7o,Q9o-Q8o,J9o,T9o,98o,87o'
                                              },
                                      'CO' : {'OPEN_SHOVE':'22+,A2s+,K5s+,Q8s+,J7s+,T8s+,97s+,87s,76s,A2o+,K9o+,QTo+,JTo',
                                              'BORDER_RANGE':'K4s-K2s,Q7s-Q2s,J6s,T7s-T6s,96s,86s-85s,75s,64s+,53s+,42s+,32s,K8o-K7o,Q9o-Q8o,J9o,T9o,98o,87o,76o'
                                              },
                                      'BU' : {'OPEN_SHOVE':'22+,A2s+,K2s+,Q4s+,J7s+,T7s+,97s+,87s,76s,65s,A2o+,K8o+,Q9o+,J9o+,T9o',
                                              'BORDER_RANGE':'Q3s-Q2s,J6s-J2s,T6s,96s-95s,86s-84s,75s-73s,64s-63s,52s+,42s+,32s,K7o-K2o,Q8o-Q5o,J8o-J6o,T8o-T7o,97o+,87o,76o,65o,54o'
                                              },
                                      'SB' : {'OPEN_SHOVE':'22+,A2s+,K2s+,Q2s+,J2s+,T3s+,95s+,85s+,74s+,64s+,53s+,A2o+,K2o+,Q4o+,J7o+,T7o+,97o+,87o',
                                              'BORDER_RANGE':'T2s,94s-93s,84s-83s,73s,63s,52s,42s+,32s,Q3o-Q2o,J6o-J3o,T6o,96o,86o,76o,65o,54o,43o,32o'
                                              }
                                      },
                                    
                                    '15BB':  {'UTG' : { 'OPEN_SHOVE':'77+,ATs+,KTs+,QJs,AJo+,KQo',
                                                'BORDER_RANGE':'44-22,A7s-A6s,A3s-A2s,K8s-K7s,Q9s-Q8s,J9s,T9s,98s,87s,ATo-A8o,KJo-KTo,QJo',
                                                 'TOTAL_MARGINAL_OSHOVE':'55+,A8s+,A5s-A4s,K9s+,QTs+,JTs,AJo+,KQo'
                                              },
                                      'UTG+1' : {'OPEN_SHOVE':'77+,ATs+,KTs+,QJs,AJo+,KQo',
                                                 'BORDER_RANGE':'44-22,A7s-A6s,A3s-A2s,K8s-K7s,Q9s-Q8s,J9s,T9s,98s,87s,ATo-A8o,KJo-KTo,QJo',
                                                 'TOTAL_MARGINAL_OSHOVE':'55+,A8s+,A5s-A4s,K9s+,QTs+,JTs,AJo+,KQo'
                                              },
                                      'UTG+2' : {'OPEN_SHOVE':'55+,A9s+,KTs+,QTs+,JTs,T9s,AJo+,KQo',
                                                 'BORDER_RANGE':'22,A7s-A6s,A3s-A2s,K8s-K6s,Q8s,J8s,T8s,98s,87s,76s,65s,ATo-A7o,KJo-K9o,QTo+,JTo',
                                                 'TOTAL_MARGINAL_OSHOVE':'33+,A8s+,A5s-A4s,K9s+,Q9s+,J9s+,T9s,AJo+,KQo'
                                              },
                                      'MP' : {'OPEN_SHOVE':'33+,A2s+,KTs+,QTs+,JTs,AJo+,KJo+',
                                              'BORDER_RANGE':'K8s-K4s,Q8s,J8s,T8s-T7s,97s+,86s+,76s,65s,54s,A9o-A6o,KTo-K9o,QTo,JTo,T9o,98o',
                                                 'TOTAL_MARGINAL_OSHOVE':'22+,A2s+,K9s+,Q9s+,J9s+,T9s,ATo+,KJo+,QJo'
                                              },
                                      'HJ' : {'OPEN_SHOVE':'22+,A2s+,K8s+,Q9s+,J9s+,T9s,98s,A9o+,KTo+,QJo',
                                              'BORDER_RANGE':'K7s-K2s,Q8s-Q6s,J8s-J7s,T7s,97s,87s,76s,65s,54s,A6o-A5o,K9o-K7o,QTo-Q9o,J9o+,T9o,98o,87o',
                                                 'TOTAL_MARGINAL_OSHOVE':'22+,A2s+,K8s+,Q9s+,J9s+,T8s+,98s,A7o+,KTo+,QJo'
                                              },
                                      'CO' : {'OPEN_SHOVE':'22+,A2s+,K8s+,Q9s+,J9s+,T8s+,98s,A7o+,KTo+,QTo+,JTo',
                                              'BORDER_RANGE':'K7s-K2s,Q8s-Q7s,J8s-J7s,T7s-T6s,97s-96s,86s+,75s+,65s,54s,43s,A3o-A2o,K9o-K7o,Q9o-Q8o,J9o-J8o,T8o+,98o,87o,76o',
                                                 'TOTAL_MARGINAL_OSHOVE':'22+,A2s+,K8s+,Q9s+,J9s+,T8s+,98s,54s,43s,32s,A4o+,KTo+,QTo+,JTo,65o'
                                              },
                                      'BU' : {'OPEN_SHOVE':'22+,A2s+,K5s+,Q8s+,J8s+,T7s+,97s+,87s,A2o+,KTo+,QTo+,JTo',
                                              'BORDER_RANGE':'Q6s-Q2s,J6s-J2s,T6s,96s,85s,75s-74s,64s,53s+,43s,32s,K8o-K2o,Q9o-Q6o,J9o-J7o,T8o,98o,87o,76o',
                                                 'TOTAL_MARGINAL_OSHOVE':'22+,A2s+,K2s+,Q7s+,J7s+,T7s+,97s+,86s+,76s,65s,A2o+,K9o+,QTo+,JTo,T9o'
                                              },
                                      'SB' : {'OPEN_SHOVE':'22+,A2s+,K2s+,Q4s+,J5s+,T6s+,96s+,86s+,75s+,65s,54s,A2o+,K5o+,Q9o+,J9o+,T9o',
                                              'BORDER_RANGE':'J3s-J2s,T3s,94s,84s,73s,63s,53s-52s,42s+,32s,Q4o-Q2o,J6o-J5o,T6o,96o,86o,76o,65o',
                                                 'TOTAL_MARGINAL_OSHOVE':'22+,A2s+,K2s+,Q2s+,J4s+,T4s+,95s+,85s+,74s+,64s+,54s,A2o+,K2o+,Q5o+,J7o+,T7o+,97o+,87o'
                                              }
                                        }
                                    }



'''
BENCB789_OPEN_RANGES_DATABASE_15BB = {
                                      'UTG' : { 'OPEN_SHOVE':'77+,ATs+,KTs+,QJs,AJo+,KQo',
                                                'BORDER_RANGE':'44-22,A7s-A6s,A3s-A2s,K8s-K7s,Q9s-Q8s,J9s,T9s,98s,87s,ATo-A8o,KJo-KTo,QJo',
                                                 'TOTAL_MARGINAL_OSHOVE':'55+,A8s+,A5s-A4s,K9s+,QTs+,JTs,AJo+,KQo'
                                              },
                                      'UTG+1' : {'OPEN_SHOVE':'77+,ATs+,KTs+,QJs,AJo+,KQo',
                                                 'BORDER_RANGE':'44-22,A7s-A6s,A3s-A2s,K8s-K7s,Q9s-Q8s,J9s,T9s,98s,87s,ATo-A8o,KJo-KTo,QJo',
                                                 'TOTAL_MARGINAL_OSHOVE':'55+,A8s+,A5s-A4s,K9s+,QTs+,JTs,AJo+,KQo'
                                              },
                                      'UTG+2' : {'OPEN_SHOVE':'55+,A9s+,KTs+,QTs+,JTs,T9s,AJo+,KQo',
                                                 'BORDER_RANGE':'22,A7s-A6s,A3s-A2s,K8s-K6s,Q8s,J8s,T8s,98s,87s,76s,65s,ATo-A7o,KJo-K9o,QTo+,JTo',
                                                 'TOTAL_MARGINAL_OSHOVE':'33+,A8s+,A5s-A4s,K9s+,Q9s+,J9s+,T9s,AJo+,KQo'
                                              },
                                      'MP' : {'OPEN_SHOVE':'33+,A2s+,KTs+,QTs+,JTs,AJo+,KJo+',
                                              'BORDER_RANGE':'K8s-K4s,Q8s,J8s,T8s-T7s,97s+,86s+,76s,65s,54s,A9o-A6o,KTo-K9o,QTo,JTo,T9o,98o',
                                                 'TOTAL_MARGINAL_OSHOVE':'22+,A2s+,K9s+,Q9s+,J9s+,T9s,ATo+,KJo+,QJo'
                                              },
                                      'HJ' : {'OPEN_SHOVE':'22+,A2s+,K8s+,Q9s+,J9s+,T9s,98s,A9o+,KTo+,QJo',
                                              'BORDER_RANGE':'K7s-K2s,Q8s-Q6s,J8s-J7s,T7s,97s,87s,76s,65s,54s,A6o-A5o,K9o-K7o,QTo-Q9o,J9o+,T9o,98o,87o',
                                                 'TOTAL_MARGINAL_OSHOVE':'22+,A2s+,K8s+,Q9s+,J9s+,T8s+,98s,A7o+,KTo+,QJo'
                                              },
                                      'CO' : {'OPEN_SHOVE':'22+,A2s+,K8s+,Q9s+,J9s+,T8s+,98s,A7o+,KTo+,QTo+,JTo',
                                              'BORDER_RANGE':'K7s-K2s,Q8s-Q7s,J8s-J7s,T7s-T6s,97s-96s,86s+,75s+,65s,54s,43s,A3o-A2o,K9o-K7o,Q9o-Q8o,J9o-J8o,T8o+,98o,87o,76o',
                                                 'TOTAL_MARGINAL_OSHOVE':'22+,A2s+,K8s+,Q9s+,J9s+,T8s+,98s,54s,43s,32s,A4o+,KTo+,QTo+,JTo,65o'
                                              },
                                      'BU' : {'OPEN_SHOVE':'22+,A2s+,K5s+,Q8s+,J8s+,T7s+,97s+,87s,A2o+,KTo+,QTo+,JTo',
                                              'BORDER_RANGE':'Q6s-Q2s,J6s-J2s,T6s,96s,85s,75s-74s,64s,53s+,43s,32s,K8o-K2o,Q9o-Q6o,J9o-J7o,T8o,98o,87o,76o',
                                                 'TOTAL_MARGINAL_OSHOVE':'22+,A2s+,K2s+,Q7s+,J7s+,T7s+,97s+,86s+,76s,65s,A2o+,K9o+,QTo+,JTo,T9o'
                                              },
                                      'SB' : {'OPEN_SHOVE':'22+,A2s+,K2s+,Q4s+,J5s+,T6s+,96s+,86s+,75s+,65s,54s,A2o+,K5o+,Q9o+,J9o+,T9o',
                                              'BORDER_RANGE':'J3s-J2s,T3s,94s,84s,73s,63s,53s-52s,42s+,32s,Q4o-Q2o,J6o-J5o,T6o,96o,86o,76o,65o',
                                                 'TOTAL_MARGINAL_OSHOVE':'22+,A2s+,K2s+,Q2s+,J4s+,T4s+,95s+,85s+,74s+,64s+,54s,A2o+,K2o+,Q5o+,J7o+,T7o+,97o+,87o'
                                              }
                                      }
'''
'''
BENCB789_OPEN_RANGES_DATABASE_15BB = {
                                      'UTG' : { 'OPEN_SHOVE':'',
                                                'BORDER_RANGE':'',
                                                 '':''
                                              },
                                      'UTG+1' : {'OPEN_SHOVE':'',
                                                 'BORDER_RANGE':'',
                                                 '':''
                                              },
                                      'UTG+2' : {'OPEN_SHOVE':'',
                                                 'BORDER_RANGE':'',
                                                 '':''
                                              },
                                      'MP' : {'OPEN_SHOVE':'',
                                              'BORDER_RANGE':'',
                                                 '':''
                                              },
                                      'HJ' : {'OPEN_SHOVE':'',
                                              'BORDER_RANGE':'',
                                                 '':''
                                              },
                                      'CO' : {'OPEN_SHOVE':'',
                                              'BORDER_RANGE':'',
                                                 '':''
                                              },
                                      'BU' : {'OPEN_SHOVE':'',
                                              'BORDER_RANGE':'',
                                                 '':''
                                              },
                                      'SB' : {'OPEN_SHOVE':'',
                                              'BORDER_RANGE':'',
                                                 '':''
                                              }
                                      }
'''
'''
BENCB789_OPEN_RANGES_DATABASE_15BB = {
                                      'UTG' : '55+,ATs+,KTs+,QJs,AJo+,KQo',
                                      'UTG+1' : '55+,ATs+,KTs+,QJs,AJo+,KQo',
                                      'UTG+2' : '55+,A9s+,KTs+,QTs+,JTs,T9s,AJo+,KQo',
                                      'MP' : '33+,A2s+,KTs+,QTs+,JTs,AJo+,KJo+',
                                      'HJ' : '22+,A2s+,K8s+,Q9s+,J9s+,T9s,98s,A9o+,KTo+,QJo',
                                      'CO' : '22+,A2s+,K8s+,Q9s+,J9s+,T8s+,98s,A7o+,KTo+,QTo+,JTo',
                                      'BU' : '22+,A2s+,K5s+,Q8s+,J8s+,T7s+,97s+,87s,A2o+,KTo+,QTo+,JTo',
                                      'SB' : '22+,A2s+,K2s+,Q4s+,J5s+,T6s+,96s+,86s+,75s+,65s,54s,A2o+,K5o+,Q9o+,J9o+,T9o'}
'''
'''
BENCB789_OPEN_RANGES_DATABASE_15BB_marginal_inc = {
                                      'UTG' : '',
                                      'UTG+1' : '',
                                      'UTG+2' : '',
                                      'MP' : '',
                                      'HJ' : '',
                                      'CO' : '',
                                      'BU' : '22+,A2s+,K2s+,Q7s+,J7s+,T7s+,97s+,86s+,76s,65s,A2o+,K9o+,QTo+,JTo,T9o',
                                      'SB' : '22+,A2s+,K2s+,Q2s+,J4s+,T4s+,95s+,85s+,74s+,64s+,54s,A2o+,K2o+,Q5o+,J7o+,T7o+,97o+,87o'}
'''


### Deck class


class Deck:
    def __init__(self):
        
        values = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
        suits = ['♣','♦','♥','♠']
        
        #cards_list = []
        self.cards = []
        
        for value in values:
            for suit in suits:
                self.cards.append(poker.Card("{}{}".format(value,suit)))
                #cards_list.append(str(value)+str(suit))

       # print(cards_list)
    def deck_shuffle(self):
        random.shuffle(self.cards)
        
    def draw_card(self):
        return self.cards.pop(0)
    
    def show_length(self):
        return len(self.cards)
    
    def deal_cards_from_deck_to_player(self,player):
        player.cards.append(self.draw_card())
        player.cards.append(self.draw_card())
        
    def drop_cards_back_in_deck(self,player):
        self.cards.append(player.drop_card())
        self.cards.append(player.drop_card())


### Class Player



class Player:
    POSITIONS = ['UTG','UTG+1','UTG+2','MP','HJ','CO','BU','SB']
    def __init__(self, position, stack):
        
        self.input_record = []
        self.record = []
        self.cards = []
        self.position = position
        self.stack = stack

        
    def add_card(self, card):
        self.cards.append(card)
    
    def show_cards(self):
        return print("{} {}{}".format('We have: ',self.cards[0],self.cards[1]))
    
    def show_position(self):
        return print( 'Position:' + ' ' + str(self.position) )
    
    def show_stack(self):
        return print( 'Stack:' + ' ' + str(self.stack) +' BB')
    
    def drop_card(self):
        return self.cards.pop(0)
    
    def make_random(self,x,y):
        positions = self.POSITIONS
        random.shuffle(positions)
        self.position = positions[0]
        self.stack = random.randint(x,y)

    def assign_position_to_player(self, position):
        self.position = position

    def assign_stack_to_player(self, stack):
        self.stack = stack

    def assign_cards_to_player(self, card_1, card_2):
        self.cards.append(card_1)
        self.cards.append(card_2)
    
    def display_situation(self):
        print('\n            ♣♣♣ Q'+ str(i+1) +' ♣♣♣\n')
        self.show_cards()
        self.show_position()
        self.show_stack()
        
    def display_question_to_player(self, i):
        self.display_situation()
        self.add_record()
        
    def add_record(self):
        answer = input('       ♣♣♣ True or False ? ♣♣♣\n')
        print('\n*****************************************\n')
        self.input_record.append(answer)
        self.record.append([str(poker.Combo.from_cards(self.cards[0],self.cards[1])), self.position, str(self.stack) + ' BB', answer])
        
    def get_range_from_record(self, stack_record, record, category='OPEN_SHOVE'):
        return poker.Range(BENCB789_OPEN_RANGES_DATABASE[stack_record][record[1]][category])
        
    def is_in_range(self, stack_record, record, category):
        if poker.Combo(record[0]) in self.get_range_from_record(stack_record, record, category).combos:
            return True
        if poker.Combo(record[0]) not in self.get_range_from_record(stack_record, record, category).combos:
            return False
        
    def answer_is_true(self, record):
         if record[3] == 'True' or 'T' or '1' or '':
             return True
         if record[3] == 'False' or 'f' or '0' or 'F':
             return False
         
    def display_review(self, review_count, card_record, position_record, stack_record, answer_record):
        print('                               ♣♣♣ Q'+ str(review_count+1) +' ♣♣♣')
        print('players cards were: ' + card_record , '      ***', poker.Combo.to_hand(poker.Combo(card_record)), '***')
        print('players position was: ' + position_record)
        print('players stack was: '+ stack_record)
        print('Your answer was: ' + answer_record)

        
    def stack_strip(self, record):
            return int(record[2].strip(' BB'))
        
    def print_range_from_record(self, stack_record, record, category='OPEN_SHOVE'):
        print('\n'+ 'The Correct Range is:')
        print(self.get_range_from_record(stack_record, record, category).to_ascii(border=True))
        print(self.get_range_from_record(stack_record, record, category).percent, ' %')
        
    def review_record(self):
        print('Reviewing Record...')
        print('Reviewing Record...')
        print('Reviewing Record...')

        review_count = 0
        TOTAL_CORRECT_ANSWERS = 0
        for records in self.record:
            print('                               Record number: '+str(review_count+1))
            print(records)
            if self.stack_strip(records) < 15:
                if self.is_in_range('10BB', records, 'OPEN_SHOVE') and self.answer_is_true(records):
                    self.display_review(review_count, records[0],records[1],records[2],records[3])
                    print('Your answer is Correct           11')
                    self.print_range_from_record('10BB', records)
                    records.append([self.is_in_range('10BB', records, 'OPEN_SHOVE'), self.answer_is_true(records), True])
                    TOTAL_CORRECT_ANSWERS +=1
                elif self.is_in_range('10BB', records, 'OPEN_SHOVE') or self.answer_is_true(records):
                    self.display_review(review_count, records[0],records[1],records[2],records[3])
                    print('Your answer is wrong             12')
                    self.print_range_from_record('10BB', records)
                    records.append([self.is_in_range('10BB', records, 'OPEN_SHOVE'), self.answer_is_true(records), False])
                elif not(self.is_in_range('10BB', records, 'OPEN_SHOVE') and self.answer_is_true(records)):
                    self.display_review(review_count, records[0],records[1],records[2],records[3])
                    print('Your answer is Correct           13')
                    self.print_range_from_record('10BB', records)
                    records.append([self.is_in_range('10BB', records, 'OPEN_SHOVE'), self.answer_is_true(records), True])
                    TOTAL_CORRECT_ANSWERS +=1
            elif 15 <= self.stack_strip(records) < 20:
                if self.is_in_range('10BB', records, 'OPEN_SHOVE') and self.answer_is_true(records):
                    self.display_review(review_count, records[0],records[1],records[2],records[3])
                    print('Your answer is Correct           21')
                    self.print_range_from_record('15BB', records)
                    records.append([self.is_in_range('10BB', records, 'OPEN_SHOVE'), self.answer_is_true(records), True])
                    TOTAL_CORRECT_ANSWERS +=1
                elif self.is_in_range('10BB', records, 'OPEN_SHOVE') or self.answer_is_true(records):
                    self.display_review(review_count, records[0],records[1],records[2],records[3])
                    print('Your answer is Wrong             22')
                    self.print_range_from_record('15BB', records)
                    records.append([self.is_in_range('10BB', records, 'OPEN_SHOVE'), self.answer_is_true(records), False])
                elif not(self.is_in_range('10BB', records, 'OPEN_SHOVE') and self.answer_is_true(records)):
                    self.display_review(review_count, records[0],records[1],records[2],records[3])
                    print('Your answer is Correct           23')
                    self.print_range_from_record('15BB', records)
                    records.append([self.is_in_range('10BB', records, 'OPEN_SHOVE'), self.answer_is_true(records), True])
                    TOTAL_CORRECT_ANSWERS +=1
            else:
                print('pppppppppppp')
            review_count+=1
        print(player.record)
        print('Total correct answers : ' +str(TOTAL_CORRECT_ANSWERS) +'/'+ str(review_count))


'''
###  PROGRAMME MAIN RUN ###
TOTAL_CARD_DEALT = 0
TOTAL_INR_CARD_DEALT = 0
TOTAL_OOFR_CARD_DEALT = 0

deck = Deck()
deck.deck_shuffle()
player = Player('UTG',10)

player.make_random(15,19)

deck.deal_cards_from_deck_to_player(player)
TOTAL_CARD_DEALT += 1

combo = poker.Combo.from_cards(player.cards[0],player.cards[1])
combo_to_hand = combo.to_hand()

for i in range(30):
    
    ### If 10BB Ranges : 
    if int(player.stack) <= 14:
        ### If Player Combo is INR or INBR :
        if combo in poker.Range(BENCB789_OPEN_RANGES_DATABASE['10BB'][player.position]['OPEN_SHOVE']).combos or combo in poker.Range(BENCB789_OPEN_RANGES_DATABASE['10BB'][player.position]['BORDER_RANGE']).combos :
            print('*****************************************')
            print('Combo in range: ' + str(combo))
            player.display_question_to_player(TOTAL_INR_CARD_DEALT)

            TOTAL_INR_CARD_DEALT += 1
        ### If Combo is not INR or INBR :
        else : 
            #print('Combo out of range: '+ str(combo))
            TOTAL_OOFR_CARD_DEALT +=1
    ### If 15BB <= Ranges < 20BB:
    elif (int(player.stack) >= 15) and (int(player.stack) <=19):
        ### If Player Combo is INR or INBR :
        if combo in poker.Range(BENCB789_OPEN_RANGES_DATABASE['15BB'][player.position]['OPEN_SHOVE']).combos or combo in poker.Range(BENCB789_OPEN_RANGES_DATABASE['15BB'][player.position]['BORDER_RANGE']).combos :
            print('*****************************************')
            print('Combo in range: ' + str(combo))
            player.display_question_to_player(TOTAL_INR_CARD_DEALT)
            
            TOTAL_INR_CARD_DEALT += 1
        ### If Player Combo is not INR or INBR:
        else:
            #print('Combo out of range: ' + str(combo))
            TOTAL_OOFR_CARD_DEALT +=1

    deck.drop_cards_back_in_deck(player)
    player.make_random(15,19)
    deck.deck_shuffle()
    deck.deal_cards_from_deck_to_player(player)
    TOTAL_CARD_DEALT += 1
    combo = poker.Combo.from_cards(player.cards[0],player.cards[1])
    combo_to_hand = combo.to_hand()

print('OOFR / CARD DEALT: ' + str(TOTAL_OOFR_CARD_DEALT) + '/' + str(i+1) )
print('INR / CARD DEALT: ' + str(TOTAL_INR_CARD_DEALT) + '/' + str(i+1) )

player.review_record()

output = run("pwd", capture_output=True).stdout

'''


### POKER MODULE TESTS ###

'''
c = poker.Suit('c')
print(c)
print('\n *** \n')

c = poker.Rank('J')
print(c)
print('\n *** \n')

print(list(poker.card.Suit))
print('\n *** \n')

print(list(poker.card.Rank))
print('\n *** \n')

c = poker.Card('Ac')
print(c)
print(type(c))
print(c.is_face)
print(c.is_broadway)
print(c.rank)
print(type(c.rank))
print(c.suit)
print(type(c.suit))
print('\n *** \n')

c = poker.Shape('o')
print(c)
c = poker.Shape
print(list(c))
print('\n *** \n')

c = poker.Hand('ATs')
print(c)
print(type(c))
print(c.first)
print(type(c.first))
print(c.second)
print(c.shape)
print(type(c.shape))
print(c.rank_difference)
print(type(c.rank_difference))
print(c.is_broadway)
print(c.is_connector)
print(c.is_offsuit)
print(c.is_one_gapper)
print(c.is_pair)
print(c.is_suited)
print(c.is_suited_connector)
print(c.is_two_gapper)
print(c.to_combos())
print(type(c.to_combos()))
print('\n *** \n')

c = poker.hand.PAIR_HANDS
print(c)
print(type(c))
print(type(c[0]))
print('\n *** \n')

c = poker.hand.OFFSUIT_HANDS
print(c)
print(type(c))
print(type(c[0]))
print('\n *** \n')

c = poker.hand.SUITED_HANDS
print(c)
print(type(c))
print(type(c[0]))
print('\n *** \n')

c = poker.Combo('AcKc')
#print(c.from_cards(poker.Card('Ac'),poker.Card('Js')))
print(c)
print(type(c))
print(c.first)
print(c.second)
print(c.shape)
print(c.is_broadway)
print(c.is_connector)
print(c.is_offsuit)
print(c.is_one_gapper)
print(c.is_pair)
print(c.is_suited)
print(c.is_suited_connector)
print(c.is_two_gapper)
print(c.rank_difference)
print(c.to_hand())
print(type(c.to_hand()))
print('\n *** \n')

c = poker.Range()
c = c.from_objects((Hand('A2s'), Hand('A3s'), Hand('A4s'), Hand('A5s'),
                    Hand('A6s'), Hand('A7s'), Hand('A8s'), Hand('A9s'),
                    Hand('ATs'), Hand('AJs'), Hand('AQs'), Hand('AKs'),
                    Hand('22'), Hand('33'), Hand('44'), Hand('55'),
                    Hand('66'), Hand('77'), Hand('88'), Hand('99'),
                    Hand('TT'), Hand('JJ'), Hand('QQ'), Hand('KK'),
                    Hand('AA')))
print(c)
print(type(c))
print('\n *** \n')

c = poker.Range('A2s+ 22+')
print(c)
print(type(c))
print('\n *** \n')

c = poker.Range('A2s+ 22+').hands
print(c)
print(type(c))
print(type(c[0]))
print('\n *** \n')


c = poker.Range('A2s+ 22+').combos
print(c)
print(type(c))
print(type(c[0]))
print('\n *** \n')

c = poker.Range('A2s+ 22+').percent
print(c)
print(type(c))
print('\n *** \n')

c = poker.Range('A2s+ 22+').rep_pieces
print(c)
print(type(c))
print(type(c[0]))
print('\n *** \n')

c = poker.Range('A2s+ 22+').to_ascii(border=True)
print(c)
print(type(c))
#classmethod from_objects(iterable)
'''






deck = Deck()
deck.deck_shuffle()
drawn_cards_storage = []
drawn_flops_storage = []

for i in range(10000):
    drawn_cards_storage.append(deck.draw_card())
    drawn_cards_storage.append(deck.draw_card())
    drawn_cards_storage.append(deck.draw_card())
    drawn_flops_storage.append(drawn_cards_storage)
    #print( 'FLOP ', i+1  , ': ',drawn_cards_storage) 
    for i in range(len(drawn_cards_storage)):
        deck.cards.append(drawn_cards_storage[i])
    drawn_cards_storage = []
    deck.deck_shuffle()

#print(drawn_flops_storage)
flop_storage_series = pd.Series(drawn_flops_storage, name = 'Flops')
print(flop_storage_series)
