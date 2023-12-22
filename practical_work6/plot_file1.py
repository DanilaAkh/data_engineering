import pandas as pd
import matplotlib.pyplot as plt
import json
import numpy as np
import seaborn as sns



def read_dtypes(file_name):
    dtypes = {}
    with open(file_name, "r") as f:
        dtypes = json.load(f)

        for key, value in dtypes.items():
            if value == "category":
                dtypes[key] = pd.CategoricalDtype()
            else:
                dtypes[key] = np.dtype(value)
    return dtypes


# Построение графика количества игр по дням недели
def first_plot(dataset):
    plt.figure(figsize=(10, 5))
    cats = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    df = dataset.copy()
    df["day_of_week"] = pd.Categorical(dataset['day_of_week'], categories=cats, ordered=True)    
    plot = dataset.groupby(df["day_of_week"], observed=True)["number_of_game"].mean().plot(title="Среднее количество игр по дням недели")
    plot.get_figure().savefig(".\\file1_fig\\1.png")
    plt.close()




def main():
    need_dtypes = read_dtypes("dtypes.json")
    dataset = pd.read_csv("df.csv",
                          #usecols=lambda x: x in need_dtypes.keys(),
                          dtype=need_dtypes)    
    #dataset.info(memory_usage="deep")

    #print(dataset)
    
    
    
    
    # Построение графика Hits
    plt.figure(figsize=(10, 5))
    for col in dataset[[col for col in dataset.columns if "hits" in col]]:
        plot = dataset[col].plot(bins=100, kind='hist', title="Hits", alpha=0.7, legend=True)
    plot.get_figure().savefig(".\\file1_fig\\2.png")
    plt.close()

    # Количество игр в виде круговой диаграммы
    plt.figure(figsize=(10, 5))    
    plot = dataset["number_of_game"].value_counts().plot(kind='pie', title='Количество игр')
    plot.get_figure().savefig(".\\file1_fig\\3.png")
    plt.close()

    # Корреляция
    df = dataset.select_dtypes(include=[int, float])
    plt.figure(figsize=(16,16))
    sns.heatmap(df.corr(), annot=True, cmap="YlGnBu", cbar=False)
    plt.savefig(".\\file1_fig\\4.png")
    plt.close()

    # pairplot
    sns.pairplot(df)
    plt.savefig(".\\file1_fig\\5.png")


    plt.show()


if __name__ == "__main__":
    main()