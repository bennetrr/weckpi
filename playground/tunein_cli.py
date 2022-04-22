from tunein import TuneIn
from rich import print as rich_print
from rich.table import Table
from rich.prompt import Prompt

search_term = Prompt.ask('Search TuneIn: ')

search_results = TuneIn.search(search_term)

table = Table(title='TuneIn Search Results')
table.add_column('Stream Name', justify='left')
table.add_column('Stream URL')
table.add_column('Description')
table.add_column('Now Playing', justify='right')

for result in search_results:
    table.add_row(result.raw['stream'],
                  result.raw['url'],
                  result.raw['description'],
                  f'{result.raw["artist"]} - {result.raw["title"]}')

rich_print(table)
