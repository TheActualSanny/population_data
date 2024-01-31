import logging

parsing = logging.getLogger('exception')
parsing.setLevel(logging.DEBUG) # CHANGE THE LEVEL HERE
format1 = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file1 = logging.FileHandler('parsing.log')
file1.setFormatter(format1)
parsing.addHandler(file1)