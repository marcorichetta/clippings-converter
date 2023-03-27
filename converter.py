import re
from typing import Tuple
from markdown import markdown
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class Clipping:
    title: str
    author: str
    page: int
    date: datetime
    note: str

    @classmethod
    def parse_file(cls, clippings_file: str) -> list:
        """Parse Clippings file content and returns a list of Clippings

        Args:
            clippings_file (str): Path to clippings.txt file
        """

        clippings_list = []
        content = Path(clippings_file).read_text()

        # Split the clippings text into individual notes
        notes = content.split("==========")

        for index, note in enumerate(notes):
            print(f"Parsing note {index}")

            # Skip if we are in last line
            if note == "\n":
                continue

            lines = note.strip().split("\n")
            book_title, author = cls._parse_title_and_author(lines[0].strip())

            page, _, date_info = cls._parse_page_info(lines[1])

            page_num = cls._convert_page_number(page)

            # Convert to datetime
            parsed_date: datetime = datetime.strptime(
                date_info.strip(), "Added on %A, %B %d, %Y %I:%M:%S %p"
            )

            note_content = lines[3:]
            clippings_list.append(
                cls(book_title, author, page_num, parsed_date, *note_content)
            )

        return clippings_list

    @classmethod
    def _parse_title_and_author(cls, line: str) -> tuple[str, str]:
        """Parses the line with the title and author and returns the author

        Args:
            line (str): First line of the clipping

        Returns:
            tuple[str, str]: book title and author name
        """
        book_title = ""
        author_name = ""

        regex = re.compile(r"(?P<title>.+) (?P<author>\(.*\))")
        match = regex.search(line)

        if match:
            book_title = match.group("title")
            author_name = match.group("author").replace("(", "").replace(")", "")

        return book_title, author_name

    @classmethod
    def _convert_page_number(cls, page: str) -> int:
        match = re.search("\\d+", page)
        if match:
            # Capture first and only group
            page_num = int(match.group())
        else:
            page_num = 0
        return page_num

    @classmethod
    def _parse_page_info(cls, line: str) -> Tuple[str, ...]:
        """Parses a string with the following format:

        `- Your Highlight on page 1 | Location 1-10 | Added on Saturday, August 6, 2016 2:25:21 AM`

        Args:
            line (str): 2nd line of the clipping
        Returns:
            Tuple[str, ...]: Page, Location and Date information. Page may not be available so it returns 0 as default.
        """
        # Default page
        page = "Page 0"

        try:
            page, location, date_info = line.split("|")
            return (page, location, date_info)
        except ValueError:
            location, date_info = line.split("|")
            return (page, location, date_info)


def generate_markdown(clippings: str):
    # Retrieve the clippings text from the input field

    # TODO - Encontrar forma de pasar clippings.value desde el front
    # clippings = Element('clippings-input').value

    # Split the clippings text into individual notes
    notes = clippings.split("==========")

    # Initialize an empty dictionary to store the notes by book
    notes_by_book = {}

    # Iterate over the notes and group them by book title
    for note in notes:
        if note:
            # Extract the book title and note text from the note
            lines = note.strip().split("\n")
            book_title = lines[0].strip()
            page, _, date_info = lines[1].split("|")
            note_content: list[str] = lines[3:]

            # Add the note to the corresponding book
            if book_title not in notes_by_book:
                notes_by_book[book_title] = []
            notes_by_book[book_title].append(note_text)

    # Generate the Markdown output grouped by book title
    markdown = ""
    for book_title, notes in notes_by_book.items():
        markdown += f"## {book_title}\n\n"
        for note in notes:
            markdown += f"{note}\n"
        markdown += "\n"

    return markdown
