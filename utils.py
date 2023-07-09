def print_format(caption: tuple, data: list[tuple]):
    """Форматированный вывод данных"""
    print(', '.join(caption))
    [print(', '.join(str(e) for e in el)) for el in data]

