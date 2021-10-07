from enum import Enum
import random
from typing import Union, List


class Suites(Enum):
    Club = '♣'
    Spade = '♠'
    Diamond = '♦'
    Heart = '♥'


class Card:
    """ @TODO: doc """

    def __init__(self, rank: int, suit: str) -> None:
        self.suit = suit
        self.rank = rank

    def __repr__(self) -> str:
        """ :returns cards in appropriate visual (...A♣, A♠, A♦, A♥) """
        return f'{self.rank}{self.suit}'


class CardSerializer:
    """ @TODO: doc """

    def __init__(self, rank: int) -> None:
        self.rank = rank

    def serialize(self) -> Union[int, str]:
        """
        Method that serializes cards in appropriate format (int to str)
        :returns - self.rank to str if rank in dict.keys (J, Q, K, A); Otherwise: self.rank
        """
        to_string = {
            11: 'J',
            12: 'Q',
            13: 'K',
            14: 'A',
        }.get(self.rank, self.rank)  # If rank not in dict it takes itself (11 - J; 9 - 9...)

        return to_string


class Deck:
    """ @TODO: doc """

    def __init__(self) -> None:
        self.deck = [str(Card((CardSerializer(rank).serialize()), suit.value)) for rank in range(6, 15) for suit in
                     Suites]
        random.shuffle(self.deck)


class CardDealing(Deck):
    """ @TODO: doc """

    def __init__(self) -> None:
        super().__init__()
        self.player1_hand = self.deck[-6:]
        self.player2_hand = self.deck[-12: -6]
        del self.deck[-12:]  # Deleting dealt cards from Deck
        self.trump_card = random.choice(self.deck)


class Game(CardDealing):
    """ @TODO: Doc """

    def __init__(self, player1_name, player2_name) -> None:
        super().__init__()
        self.player1_name = player1_name
        self.player2_name = player2_name

    def starts(self, player1: List[Card], player2: List[Card], trump: Card):
        """ @TODO: Doc """
        p1_trump_cards = [str(card) for card in player1 if card[-1] == trump[-1] if card[:-1] != 'A']
        p2_trump_cards = [str(card) for card in player2 if card[-1] == trump[-1] if card[:-1] != 'A']
        smallest_trump_card = None

        if p1_trump_cards and not p2_trump_cards:
            smallest_trump_card = min(p1_trump_cards)
        elif p2_trump_cards and not p1_trump_cards:
            smallest_trump_card = min(p2_trump_cards)
        elif p1_trump_cards and p2_trump_cards:
            smallest_trump_card = min(min(p2_trump_cards), min(p2_trump_cards))

        if smallest_trump_card in p1_trump_cards:
            return self.player1_name
        return self.player2_name

    @staticmethod
    def to_int(card_rank: str) -> int:
        """
        :param card_rank string (Q)
        :returns - Converted card rank to int (Input: str(A); Output: int(14)...)
        """
        r = {
            'J': 11,
            'Q': 12,
            'K': 13,
            'A': 14,
        }.get(card_rank)
        return r

    def _is_trump(self, player_card: str) -> bool:
        """ @TODO: doc """

        if player_card[-1] == self.trump_card[-1]:
            return True
        return False

    def is_stronger(self, p_card: str, table: list) -> bool:
        """ @TODO: doc """

        if self._is_trump(p_card) and not self._is_trump(table[-1]):
            return True
        elif not self._is_trump(p_card) and self._is_trump(table[-1]):
            return False
        elif self._is_trump(p_card) and self._is_trump(table[-1]):
            pass

        table_card_rank: str = table[-1][:-1]
        player_card_rank: str = p_card[:-1]

        if not player_card_rank.isdigit() and not table_card_rank.isdigit():
            if self.to_int(player_card_rank) > self.to_int(table_card_rank):
                return True
        elif player_card_rank.isdigit() and not table_card_rank.isdigit():
            if int(player_card_rank) > self.to_int(table_card_rank):
                return True
        elif not player_card_rank.isdigit() and table_card_rank.isdigit():
            if self.to_int(player_card_rank) > int(table_card_rank):
                return True
        elif player_card_rank.isdigit() and table_card_rank.isdigit():
            if int(player_card_rank) > int(table_card_rank):
                return True
        return False
