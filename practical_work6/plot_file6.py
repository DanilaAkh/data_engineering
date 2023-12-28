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
    plot = dataset.groupby(dataset["CSA"], observed=False)["TRACTCE"].mean().plot(title="Зависимость TRACTCE от CSA")
    plt.semilogy()
    plot.get_figure().savefig(".\\file6_fig\\1.png")    
    plt.close()


def second_plot(dataset: pd.DataFrame):
    plt.figure(figsize=(10, 5))
    for col in dataset[[col for col in dataset.columns if "Ranked" in col]]:
        plot = dataset[col].plot(bins=50, kind='hist', title="Ranked", alpha=0.7, legend=True)
    #plt.semilogy()
    plot.get_figure().savefig(".\\file6_fig\\2.png")
    plt.close()


def third_plot(dataset: pd.DataFrame):
    # Используемые классы в %    
    plt.figure(figsize=(20, 10))
    plot = dataset["CSA"].value_counts(bins=8).plot(kind='barh',
                                                        fontsize=18)
    plt.title('Количество CSA', fontsize=20)
    plt.semilogx()
    plot.get_figure().savefig(".\\file6_fig\\3.png")
    
    plt.close()


def forth_plot(dataset: pd.DataFrame):
    df = dataset.select_dtypes(include=[np.uint8, np.uint32, float])
    plt.figure(figsize=(16,16))
    matplotlib.rc('font', size=18)
    sns.heatmap(df.corr(), annot=True, cmap="YlGnBu", cbar=False)
    plt.title("Корреляция", fontsize=24)
    plt.savefig(".\\file6_fig\\4.png")
    plt.close()


def fifth_plot(dataset : pd.DataFrame):
    plt.figure(figsize=(10,8))
    sns.scatterplot(data=dataset, x='TRACTCE', y='CSA')
    plt.savefig(".\\file6_fig\\5.png")


def main():
    need_dtypes = read_dtypes(".\\out6\\dtypes6.json")
    dataset = pd.read_csv(".\\out6\\df6.csv",
                          #usecols=lambda x: x in need_dtypes.keys(),
                          dtype=need_dtypes)    
    #dataset.info(memory_usage="deep")

    first_plot(dataset)
    second_plot(dataset)
    third_plot(dataset)
    forth_plot(dataset)
    fifth_plot(dataset)


if __name__ == "__main__":
    main()