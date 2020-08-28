import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import scatter_matrix

class Visualizer:

    # Pass one column or row id of a dataframe
    def box_plot(self, data_id):
        sns.boxplot(x=data_id)
        plt.show()

    #TODO: finish this method
    def scatter_plot(self, data, data_id):
        fig, ax = plt.subplots(figsize=(16,8))
        ax.scatter(data[data_id])

    #TODO: finish this method
    def scatter_matrix_plt(self, data):
        scatter_matrix(data, figsize=(16,8))
        plt.show()


    if __name__ == "__main__":
        pass