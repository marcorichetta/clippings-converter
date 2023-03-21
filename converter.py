import re

from markdown import markdown
from pyscript import Element


def generate_markdown():
    # Retrieve the clippings text from the input field
    clippings = Element('clippings-input').value

    # Split the clippings text into individual notes
    notes = clippings.split('==========')

    # Initialize an empty dictionary to store the notes by book
    notes_by_book = {}

    # Iterate over the notes and group them by book title
    for note in notes:
        if note:
            # Extract the book title and note text from the note
            lines = note.strip().split('\n')
            book_title = lines[0].strip()
            note_text = '\n'.join(lines[1:]).strip()

            # Add the note to the corresponding book
            if book_title not in notes_by_book:
                notes_by_book[book_title] = []
            notes_by_book[book_title].append(note_text)

    # Generate the Markdown output grouped by book title
    markdown = ''
    for book_title, notes in notes_by_book.items():
        markdown += f'## {book_title}\n\n'
        for note in notes:
            markdown += f'- {note}\n'
        markdown += '\n'

    return markdown