from webapp import app

from os import system
import unittest


from tests.test_CustomTrends import CustomTrendManagementTestCase
from tests.test_Trends import TrendsManagementTestCase

def CLImenu():
    while True:
        print('####################')
        print('Anteo AI         ')
        print('CLI test launcher')
        print('####################')
        print('')
        print(' 1 --> Test CustomTrend Management')
        print(' 2 --> Test Trends Management')
        print(' q --> Quit tests')
        print('')

        option = input('Select an option: ')

        if option == '1':
            print('WARNING!')
            print('For this test case you need a demo Custom Trend with ID 1')
            print('on the fileserver.')
            print('')
            unittest.main(CustomTrendManagementTestCase(), exit = False)
        elif option == '2':
            unittest.main(TrendsManagementTestCase(), exit = False)
        elif option == 'q':
            break
        else:
            system('clear')
            print('Wrong option!\n\n')


if  __name__ == '__main__':
    system('clear')
    with app.app_context():
        CLImenu()
