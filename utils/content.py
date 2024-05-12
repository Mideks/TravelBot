from typing import Iterator

from db.city_data import CityData


def content_text_cutter(city: str, content: CityData.Content, max_length: int) -> list[str]:
    caption = f"{city}"
    if content.title:
        caption += f' - {content.title}'

    length_limit = max_length - len(caption)

    new_line_symbols = 2
    if length_limit - new_line_symbols - len(content.text) > 0:
        return [f'{caption}\n\n{content.text}']

    symbols_for_page_numbers = 8  # (nn/kk)
    text_pieces = list(text_splitter(content.text, length_limit - symbols_for_page_numbers))

    pages = []

    for i, text_piece in enumerate(text_pieces, 1):
        caption = f'{caption} ({i}/{len(text_pieces)})'
        page = (
            f'{caption}\n\n'
            f'{text_piece}'
        )
        pages.append(page)

    return pages


def text_splitter(text: str, length_limit: int) -> Iterator[str]:
    words = text.split() # if there is many spaces it is become to one space, lol
    current_text_piece = ''
    for word in words:
        if len(current_text_piece) + len(word) + 1 >= length_limit:  # +1 for the space
            yield current_text_piece
            current_text_piece = word
        else:
            if current_text_piece:
                current_text_piece += ' ' + word
            else:
                current_text_piece = word

    if current_text_piece:
        yield current_text_piece
