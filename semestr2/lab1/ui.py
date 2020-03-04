import os
from pprint import pprint

from consolemenu import SelectionMenu

from lab1.spiders import ISportSpider, PortativSpider


def show_start_menu():
    """Entrance point in menu"""
    menu = SelectionMenu([
        'Crawl isport.ua',
        'Print all links crawled from isport.ua',
        'Crawl portativ.ua',
        'Create XHTML table with headphones from portativ.ua'
    ], title="Select a task to do")
    menu.show()

    if menu.is_selected_item_exit():
        print('Bye!')
    else:
        index = menu.selected_option
        (crawl_isport, print_all_links_from_isport,
         crawl_portativ, create_xhtml_table)[index]()


def press_enter(msg=''):
    return input(f'{msg}\nPress ENTER to continue...')


def crawl_isport():
    ISportSpider.run()
    press_enter('isport.ua was crawled, results are saved to'
                f'{ISportSpider.get_data_filename()}')
    show_start_menu()


def print_all_links_from_isport():
    urls = ISportSpider.get_all_urls()
    pprint(urls)
    press_enter()
    show_start_menu()


def crawl_portativ():
    PortativSpider.run()
    press_enter('portativ.ua was crawled, results are saved to'
                f'{PortativSpider.get_data_filename()}')
    show_start_menu()


def create_xhtml_table():
    PortativSpider.create_xhtml_table()
    press_enter('XHTML table was created, results are saved to output/table.xhtml')
    show_start_menu()


if __name__ == '__main__':
    show_start_menu()
