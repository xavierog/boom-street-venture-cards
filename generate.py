#!/usr/bin/env python3

# MIT License
# 
# Copyright (c) 2024 Xavier G.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import re
import sys

DEFAULT_DATA_FILEPATH = os.environ.get('BOOM_STREET_DATA') or 'data'
DEFAULT_GRID_FILEPATH = os.environ.get('BOOM_STREET_GRID') or '-'

def load_cards(filepath: str = DEFAULT_DATA_FILEPATH) -> list[dict]:
	cards = [{'number': 0}]
	current_card = None
	with open(filepath, 'r') as data_filedesc:
		while line := data_filedesc.readline():
			if rem := re.match(r'\[CARD_0*(?P<card_number>\d+)\] "(?P<card_text>.*?)"', line):
				current_card = {'number': int(rem.group('card_number')), 'text': rem.group('card_text'), 'symbol': ''}
				cards.append(current_card)
			elif rem := re.match(r'Card Type: (?P<card_type>\S+)', line):
				current_card['type'] = rem.group('card_type').lower()
			elif rem := re.match(r'Rating: (?P<card_rating>\d+)/10', line):
				current_card['rating'] = int(rem.group('card_rating'))
			elif rem := re.match('Info/Comments: (?P<card_comment>.+)', line):
				current_card['comment'] = rem.group('card_comment')
			elif rem := re.match('Symbol: (?P<symbol>.+)', line):
				current_card['symbol'] = rem.group('symbol')
	return cards

def load_grid(filepath: str = DEFAULT_GRID_FILEPATH) -> list[list[int]]:
	grid = []
	with (sys.stdin if filepath == '-' else filepath):
		for i in range(8):
			grid.append([int(x) for x in sys.stdin.readline().split()[:8]])
	return grid

def indent(text, level=1):
	return '\n'.join(['\t'*level + line for line in text.split('\n')])

def prindent(text, level=1):
	print(indent(text, level))

HEAD = """<!DOCTYPE html>
<html>
	<head>
		<style>
			body { background-color: #1e1e1e; }
			table { border: 1px solid black; }
			td { text-align: center; border: 5px solid gray; }
			td > span.number { font-size: 4em; }
			td.rating-0, td.rating-1 { background-color: black; color: white; }
			td.rating-2, td.rating-3 { background-color: red; color: white; }
			td.rating-4, td.rating-5 { background-color: orange; }
			td.rating-6, td.rating-7 { background-color: green; color: white; }
			td.rating-8, td.rating-9 { background-color: lightgreen; }
			td.rating-10 { background-color: yellow; }
			td:before { font-size: 3em; }
			td > span.symbol { font-size: 3em; }
			td.type-bonus:before { content: "➕"; }
			td.type-cameo:before { content: "🐙"; }
			td.type-expansion:before { content: "📈"; }
			td.type-investment:before { content: "💲➡️🏠"; }
			td.type-minigame:before { content: "🎪"; }
			td.type-misadventure:before { content: "☹️"; }
			td.type-moneymaking:before { content: "💰"; }
			td.type-movement:before { content: "➡️"; }
			td.type-property:before { content: "🏠"; }
			td.type-stock:before { content: "🗠"; }
			td.type-suit:before { content: "🂡"; }
			td.type-warping:before { content: "🚀"; }
		</style>
	</head>"""

def card_td(card):
	html = """<td class="card rating-{rating} type-{type}">
	<span class="number">{number}</span>
	<span class="symbol">{symbol}</span>
	<br>
	<span class="text">{text}</span>
</td>"""
	return html.format(**card)

def main() -> None:
	cards = load_cards()
	grid = load_grid()
	print(HEAD)
	prindent('<body>', 1)
	prindent('<table>', 2)
	for row in range(8):
		prindent('<tr>', 3)
		for column in range(8):
			card_number = grid[row][column]
			card = cards[card_number]
			prindent(card_td(card), 4)
		prindent('</tr>', 3)
	prindent('</table>', 2)
	prindent('</body>', 1)
	print('</html>')

if __name__ == '__main__':
	main()
