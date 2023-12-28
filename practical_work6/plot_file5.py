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


def first_plot(dataset: pd.DataFrame):
    # Построение графика количество полетов по дням недели
    plt.figure(figsize=(15, 10))
    plot = dataset.groupby(dataset["class"])["albedo"].sum().plot(kind="bar", title="Сумма albedo по классу")
    plt.semilogy()
    plot.get_figure().savefig(".\\file5_fig\\1.png")    
    plt.close()


def second_plot(dataset: pd.DataFrame):
    plt.figure(figsize=(10, 5))
    for col in dataset[[col for col in dataset.columns if "sigma" in col]]:
        plot = dataset[col].plot(bins=50, kind='hist', title="sigma", alpha=0.7, legend=True)
    plt.semilogy()
    plot.get_figure().savefig(".\\file5_fig\\2.png")
    plt.close()


def third_plot(dataset: pd.DataFrame):
    # Используемые классы в %    
    plt.figure(figsize=(20, 10))
    plot = dataset["class"].value_counts().plot(kind='barh',
                                                        fontsize=18)
    plt.title('Используемые классы в %', fontsize=20)
    plt.semilogx()
    plot.get_figure().savefig(".\\file5_fig\\3.png")
    
    plt.close()


def forth_plot(dataset: pd.DataFrame):
    df = dataset.select_dtypes(include=[np.uint8, np.uint32, float])
    plt.figure(figsize=(16,16))
    matplotlib.rc('font', size=18)
    sns.heatmap(df.corr(), annot=True, cmap="YlGnBu", cbar=False)
    plt.title("Корреляция", fontsize=24)
    plt.savefig(".\\file5_fig\\4.png")
    plt.close()


def fifth_plot(dataset : pd.DataFrame):
    sns.scatterplot(data=dataset, x='diameter', y='albedo')
    plt.savefig(".\\file5_fig\\5.png")


def main():
    need_dtypes = read_dtypes(".\\out5\\dtypes5.json")
    dataset = pd.read_csv(".\\out5\\df5.csv",
                          #usecols=lambda x: x in need_dtypes.keys(),
                          dtype=need_dtypes)    
    #dataset.info(memory_usage="deep")

    # first_plot(dataset)
    # second_plot(dataset)
    # third_plot(dataset)
    # forth_plot(dataset)
    fifth_plot(dataset)


if __name__ == "__main__":
    main()