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
    # Построение графика моделей по средней цене
    plt.figure(figsize=(10, 5))
    plot = dataset.groupby(dataset["modelName"], observed=True)["askPrice"].mean().plot(kind="bar", 
                     title="Средние цены на автомобили разных моделей",
                     xlabel="Модели машин",
                     ylabel="Средняя цена автомобиля",
                     fontsize=10
                    )
    
    plot.get_figure().savefig(".\\file2_fig\\1.png")
    plt.close()


def second_plot(dataset: pd.DataFrame):
    plt.figure(figsize=(10, 5))
    for col in dataset[[col for col in dataset.columns if "vf" in col and col != "vf_WheelBaseShort"]]:
        plot = dataset[col].plot(bins=5, kind='hist', title="vf", alpha=0.7, legend=True)
    plot.get_figure().savefig(".\\file2_fig\\2.png")
    plt.close()


def third_plot(dataset: pd.DataFrame):
    # Отношение новых к старым машинам
    labels = ["Новый", "Старый"]
    plt.figure(figsize=(10, 10))
    plot = dataset["isNew"].value_counts().plot(kind='pie', autopct="%1.1f%%", 
                                                        labels=labels, fontsize=18)
    plt.ylabel("")
    plt.title('Отношение новых к старым автомобилям', fontsize=20)
    plot.get_figure().savefig(".\\file2_fig\\3.png")
    
    plt.close()


def forth_plot(dataset: pd.DataFrame):
    df = dataset.select_dtypes(include=[np.uint8, np.uint32, float])
    plt.figure(figsize=(16,16))
    matplotlib.rc('font', size=18)
    sns.heatmap(df.corr(), annot=True, cmap="YlGnBu", cbar=False)
    plt.title("Корреляция", fontsize=20)
    plt.savefig(".\\file2_fig\\4.png")
    plt.close()


def fifth_plot(dataset : pd.DataFrame):
    # Отношение цены новых автомобилей к старым
    plt.figure(figsize=(28,10))
    data = dataset.groupby(["modelName", "isNew"], as_index=False, observed=False)["askPrice"].count()    
    sns.barplot(data=data, x="askPrice", y="modelName", hue="isNew")
    plt.title(label="Отношение цены новых автомобилей к старым")
    plt.savefig(".\\file2_fig\\5.png")
    plt.close()


def main():
    need_dtypes = read_dtypes(".\\out2\\dtypes2.json")
    dataset = pd.read_csv(".\\out2\\df2.csv",
                          #usecols=lambda x: x in need_dtypes.keys(),
                          dtype=need_dtypes)    
    #dataset.info(memory_usage="deep")
    #print(dataset.info())
    dataset = dataset.drop(dataset[dataset["askPrice"] < 1000].index)
    dataset = dataset.drop(dataset[dataset["askPrice"] > 100000].index)
    
    first_plot(dataset)
    second_plot(dataset)
    third_plot(dataset)
    forth_plot(dataset)
    fifth_plot(dataset)


if __name__ == "__main__":
    main()