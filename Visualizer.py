import matplotlib.pyplot as plt
import seaborn as sns

class Visualizer:

    # Pass one column or row id of a dataframe
    def box_plot(self, data_id):
        sns.boxplot(x=data_id)
        plt.show()

    def scatterplot(self, data):
        pass

    if __name__ == "__main__":
        pass