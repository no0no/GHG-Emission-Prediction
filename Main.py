from Cleaner import Cleaner
from Modeler import Modeler
from Preparer import Preparer
from Visualizer import Visualizer
import pandas as pd

def main():

    data = pd.read_excel('Data/Merged.xlsx')
    mdlr = Modeler(data, 42)

if __name__ == '__main__':
    main()