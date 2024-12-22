import random
import string


def generate_message(filename: str, size_in_bytes: int):
    """
    Funkcija koja generiše nasumičan tekstualni sadržaj veličine prosleđenog broja bajtova.
    """
    
    text_content = ''.join(
        random.choices(
            string.ascii_letters + string.digits + string.punctuation, 
            k=size_in_bytes
        )
    )

    with open(f'messages/{filename}', 'w') as file:
        file.write(text_content)

generate_message('1kb_message.txt', 1_000)
generate_message('100kb_message.txt', 100_000)
generate_message('1mb_message.txt', 1_000_000)