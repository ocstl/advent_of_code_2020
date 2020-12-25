#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import deque


class CardCombat:
    def __init__(self, deck1, deck2):
        self.deck1 = deque(deck1)
        self.deck2 = deque(deck2)
        self.winner = None

    def __iter__(self):
        return self

    def __next__(self):
        if not self.deck1:
            self.winner = 2
            raise StopIteration
        elif not self.deck2:
            self.winner = 1
            raise StopIteration

        card1 = self.deck1.popleft()
        card2 = self.deck2.popleft()
        if card1 > card2:
            self.deck1.append(card1)
            self.deck1.append(card2)
        else:
            self.deck2.append(card2)
            self.deck2.append(card1)

    def score(self):
        cards = reversed(self.deck1) if self.winner == 1 else reversed(self.deck2)
        return sum(idx * card for idx, card in enumerate(cards, 1))


class CardRecursiveCombat(CardCombat):
    def __init__(self, deck1, deck2):
        super(CardRecursiveCombat, self).__init__(deck1, deck2)
        self.former_rounds = set()

    def __next__(self):
        # If one of the decks is empty, declare a winner.
        if not self.deck1:
            self.winner = 2
            raise StopIteration
        elif not self.deck2:
            self.winner = 1
            raise StopIteration

        # If this round has happened before, player 1 wins the game.
        current_round = (tuple(self.deck1), tuple(self.deck2))
        if current_round in self.former_rounds:
            self.winner = 1
            raise StopIteration
        else:
            self.former_rounds.add(current_round)

        card1 = self.deck1.popleft()
        card2 = self.deck2.popleft()

        # If both players have at least as many cards as the card they have just
        # drawn, we decide the round with a new game. But we only want as many
        # cards as indicated by the recently drawn cards.
        if len(self.deck1) >= card1 and len(self.deck2) >= card2:
            game = CardRecursiveCombat(list(self.deck1)[:card1], list(self.deck2)[:card2])
            for _ in game:
                pass

            winner = game.winner
        elif card1 > card2:
            winner = 1
        else:
            winner = 2

        if winner == 1:
            self.deck1.append(card1)
            self.deck1.append(card2)
        else:
            self.deck2.append(card2)
            self.deck2.append(card1)


def main(_args):
    decks = [[int(card) for card in deck.splitlines() if not card.startswith("Player")]
             for deck in open("input.txt", "r").read().split("\n\n")]

    # Play the small crab in a game of Combat using the two decks you just
    # dealt. What is the winning player's score?
    game = CardCombat(*decks)
    for _ in game:
        pass

    first_answer = game.score()
    print("The first answer is: " + str(first_answer))

    # Defend your honor as Raft Captain by playing the small crab in a game of
    # Recursive Combat using the same two decks as before. What is the winning
    # player's score?
    game = CardRecursiveCombat(*decks)
    for _ in game:
        pass

    second_answer = game.score()
    print("The second answer is: " + str(second_answer))


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
