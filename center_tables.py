from tabulate import tabulate

def center_table(df, width):
    table = tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False, numalign='center', stralign='center')
    table_lines = table.split('\n')
    table_width = len(table_lines[0])
    centered_table = [line.center(width) for line in table_lines]
    return '\n'.join(centered_table)