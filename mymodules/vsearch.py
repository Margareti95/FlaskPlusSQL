def search4vowels(phrase:str) -> set: # Аннотация программистам
    """Возвращает гласные, найденные в указанном слове."""
    vowels = set('aeiou')
    return vowels.intersection(set(phrase)) # Заменяем три строки на одну'''


def search4letters(phrase:str, letters:str='aeiou') -> set: # установка значения по умолчанию. Теперь функция vowels нам не нужна!
    """Возвращает множество букв из `letters`, найденных в
    указанной фразе."""
    return set(letters).intersection(set(phrase))

