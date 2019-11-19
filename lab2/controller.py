from consolemenu import SelectionMenu

from model import Model
from view import View


TABLES_NAMES = ['task', 'worker', 'project', 'department', 'worker_task']
TABLES = {
    'task': ['id', 'deadline', 'name', 'description', 'project_id', 'isdone'],
    'worker': ['id', 'fullname', 'age', 'position', 'department_id'],
    'department': ['id', 'name', 'number_of_workers', 'manager'],
    'project': ['id', 'name', 'budget', 'deadline'],
    'worker_task': ['id', 'worker_id', 'task_id']
}


def getInput(msg, tableName=''):
    print(msg)
    if tableName:
        print(' | '.join(TABLES[tableName]), end='\n\n')
    return input()


def getInsertInput(msg, tableName):
    print(msg)
    print(' | '.join(TABLES[tableName]), end='\n\n')
    return input(), input()


def pressEnter():
    input()


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def show_init_menu(self, msg=''):
        selectionMenu = SelectionMenu(
            TABLES_NAMES + ['Find without word', 'Find whole phrase',
                            'Fill table  task by random data'], subtitle=msg)
        selectionMenu.show()

        index = selectionMenu.selected_option
        if index < len(TABLES_NAMES):
            tableName = TABLES_NAMES[index]
            self.show_entity_menu(tableName)
        elif index == 5:
            self.fts_without_word()
        elif index == 6:
            self.fts_phrase()
        elif index == 7:
            self.fillByRandom()
        else:
            print('Bye, have a beautiful day!')

    def show_entity_menu(self, tableName, msg=''):
        options = ['Get',  'Delete', 'Update', 'Insert']
        functions = [self.get, self.delete, self.update, self.insert]

        if tableName == 'task':
            options.append('Search task by worker positions')
            functions.append(self.search_task_by_worker_position)
        elif tableName == 'worker':
            options.append('Search worker by his task is done')
            functions.append(self.search_worker_by_task_is_done)

        selectionMenu = SelectionMenu(options, f'Name of table: {tableName}',
                                      exit_option_text='Back', subtitle=msg)
        selectionMenu.show()
        try:
            function = functions[selectionMenu.selected_option]
            function(tableName)
        except IndexError:
            self.show_init_menu()

    def get(self, tableName):
        try:
            condition = getInput(
                'Enter condition (SQL) or leave empty:', tableName)
            data = self.model.get(tableName, condition)
            self.view.print(data)
            pressEnter()
            self.show_entity_menu(tableName)
        except Exception as err:
            self.show_entity_menu(tableName, str(err))

    def insert(self, tableName):
        try:
            columns, values = getInsertInput(
                'Enter colums divided with commas, then do the same for values', tableName)
            self.model.insert(tableName, columns, values)
            self.show_entity_menu(tableName, 'Insert is successful!')
        except Exception as err:
            self.show_entity_menu(tableName, str(err))

    def delete(self, tableName):
        try:
            condition = getInput(
                'Enter condition (SQL):', tableName)
            self.model.delete(tableName, condition)
            self.show_entity_menu(tableName, 'Delete is successful')
        except Exception as err:
            self.show_entity_menu(tableName, str(err))

    def update(self, tableName):
        try:
            condition = getInput(
                'Enter condition (SQL):', tableName)
            statement = getInput(
                'Enter SQL statement where [<key>=<value>]', tableName)

            self.model.update(tableName, condition, statement)
            self.show_entity_menu(tableName, 'Update is successful')
        except Exception as err:
            self.show_entity_menu(tableName, str(err))

    def search_task_by_worker_position(self, tableName):
        try:
            positions = getInput(
                'Enter positions divided with commas:')
            data = self.model.search_task_by_worker_position(positions)
            self.view.print(data)
            pressEnter()
            self.show_entity_menu(tableName)
        except Exception as err:
            self.show_entity_menu(tableName, str(err))

    def search_worker_by_task_is_done(self, tableName):
        try:
            is_done = getInput('Is task done?:').lower() in [
                'true', 't', 'yes', 'y', '+']
            data = self.model.search_worker_by_task_is_done(is_done)
            self.view.print(data)
            pressEnter()
            self.show_entity_menu(tableName)
        except Exception as err:
            self.show_entity_menu(tableName, str(err))

    def fts_without_word(self):
        try:
            word = getInput('Enter word:')
            data = self.model.fts_without_word(word)
            self.view.print(data)
            pressEnter()
            self.show_init_menu()
        except Exception as err:
            self.show_init_menu(str(err))

    def fts_phrase(self):
        try:
            phrase = getInput('Enter phrase:')
            data = self.model.fts_phrase(phrase)
            self.view.print(data)
            pressEnter()
            self.show_init_menu()
        except Exception as err:
            self.show_init_menu(str(err))

    def fillByRandom(self):
        try:
            self.model.fillTaskByRandomData()
            self.show_init_menu('Generated successfully')

        except Exception as err:
            self.show_init_menu(str(err))
