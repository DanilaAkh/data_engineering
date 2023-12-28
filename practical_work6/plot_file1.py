import pandas as pd
import matplotlib
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
def first_plot(dataset : pd.DataFrame):
    plt.figure(figsize=(10, 5))
    cats = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    df = dataset.copy()
    df["day_of_week"] = pd.Categorical(dataset['day_of_week'], categories=cats, ordered=True)    
    plot = dataset.groupby(df["day_of_week"], observed=True)["number_of_game"].sum().plot(kind="bar", title="Среднее количество игр в день")
    plot.get_figure().savefig(".\\file1_fig\\1.png")
    plt.close()


def second_plot(dataset : pd.DataFrame):
    #Построение графика Hits
    plt.figure(figsize=(10, 5))
    for col in dataset[[col for col in dataset.columns if "hits" in col]]:
        plot = dataset[col].plot(bins=100, kind='hist', title="Hits", alpha=0.7, legend=True)
    plot.get_figure().savefig(".\\file1_fig\\2.png")
    plt.close()


def third_plot(dataset : pd.DataFrame):
    # Количество игр в виде круговой диаграммы
    plt.figure(figsize=(10, 10))
    explode = (0.1, 0.15, 0.1, 0.15)
    plot = dataset["number_of_game"].value_counts().plot(kind='pie',  autopct="%1.1f%%", 
                                                         explode=explode, fontsize=18)
    plt.ylabel("")
    plt.title('Количество игр', fontsize=20)
    plot.get_figure().savefig(".\\file1_fig\\3.png")
    
    plt.close()


def fourth_plot(dataset : pd.DataFrame):
    # Корреляция    
    df = dataset.select_dtypes(include=[np.uint, float])
    plt.figure(figsize=(16,16))
    matplotlib.rc('font', size=18)
    sns.heatmap(df.corr(), annot=True, cmap="YlGnBu", cbar=False)
    plt.title("Корреляция", fontsize=20)
    plt.savefig(".\\file1_fig\\4.png")
    plt.close()
    return df


def fifth_plot(df : pd.DataFrame):
    #pairplot
    sns.pairplot(df)
    plt.savefig(".\\file1_fig\\5.png")


def main():
    need_dtypes = read_dtypes(".\\out1\\dtypes1.json")
    dataset = pd.read_csv(".\\out1\\df1.csv",
                          #usecols=lambda x: x in need_dtypes.keys(),
                          dtype=need_dtypes)    
    #dataset.info(memory_usage="deep")

    #print(dataset)
    
    first_plot(dataset)
    second_plot(dataset)
    third_plot(dataset)
    df = fourth_plot(dataset)
    fifth_plot(df)
    

if __name__ == "__main__":
    main()