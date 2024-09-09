import unittest

class TestFunctions(unittest.TestCase):
    
    # testing to make sure the add function is adding hands correctly
    def test_add(self):
        from functions import add
        from classes import Card

        # testing basic addition
        hand_1: list[Card] = [Card(7,'Spade'), Card(8,'Heart')]

        for card in hand_1:
            print(card)
        
        hand_total_1 = add(hand_1)
        print(f'{hand_total_1}\n')


        # testing soft ace addition
        hand_2: list[Card] = [Card(1,'Spade'), Card(8,'Heart')]

        for card in hand_2:
            print(card)
        
        hand_total_2 = add(hand_2)
        print(f'{hand_total_2}\n')


        # testing if a single hard ace is added correctly
        hand_3: list[Card] = [Card(1,'Spade'), Card(6,'Heart'), Card(7, 'Diamond')]

        for card in hand_3:
            print(card)
        
        hand_total_3 = add(hand_3)
        print(f'{hand_total_3}\n')


        # testing if 2 aces are added correctly, one needing to be hard, the other needing to be soft
        hand_4: list[Card] = [Card(1,'Spade'), Card(2, 'Club'), Card(1,'Heart'), Card(6, 'Diamond')]

        for card in hand_4:
            print(card)
        
        hand_total_4 = add(hand_4)
        print(f'{hand_total_4}\n')


        # testing if 3 aces are added correctly, two needing to be hard, the other two needing to be soft
        hand_5: list[Card] = [Card(1,'Spade'), Card(8, 'Club'), Card(1,'Heart'), Card(1, 'Diamond')]

        for card in hand_5:
            print(card)
        
        hand_total_5 = add(hand_5)
        print(f'{hand_total_5}\n')


        # testing if 4 aces are added correctly, with all 4 aces needing to be soft
        hand_6: list[Card] = [Card(1,'Spade'), Card(1,'Heart'), Card(1, 'Diamond'), Card(1, 'Club'), Card(10, 'Spade')]

        for card in hand_6:
            print(card)
        
        hand_total_6 = add(hand_6)
        print(f'{hand_total_6}\n')


        # the asserts
        self.assertEqual(hand_total_1,15)
        self.assertEqual(hand_total_2,19)
        self.assertEqual(hand_total_3,14)
        self.assertEqual(hand_total_4,20)
        self.assertEqual(hand_total_5,21)
        self.assertEqual(hand_total_6,14)


if __name__ == '__main__':
    unittest.main()