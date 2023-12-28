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
    plt.figure(figsize=(10, 5))
    cats = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    plot = dataset.groupby(dataset["DAY_OF_WEEK"], observed=True)["DAY_OF_WEEK"].count().plot(kind="bar", 
                        title="Количество полетов по дням недели",
                        xlabel="День недели",
                        ylabel="Количество",
                        fontsize=10
                        )

    plot.get_figure().savefig(".\\file3_fig\\1.png")
    plt.close()


def second_plot(dataset: pd.DataFrame):
    plt.figure(figsize=(10, 5))
    for col in dataset[[col for col in dataset.columns if "DELAY" in col]]:
        plot = dataset[col].plot(bins=50, kind='hist', title="DELAY", alpha=0.7, legend=True)
    plot.get_figure().savefig(".\\file3_fig\\2.png")
    plt.close()


def third_plot(dataset: pd.DataFrame):
    # Отношение отмененных к неотмененным рейсам
    labels = ["Не отменен", "Отменен"]
    plt.figure(figsize=(10, 10))
    plot = dataset["CANCELLED"].value_counts().plot(kind='pie', autopct="%1.1f%%", 
                                                        labels=labels, fontsize=18)
    plt.ylabel("")
    plt.title('Отношение отмененных к неотмененным рейсам', fontsize=20)
    plot.get_figure().savefig(".\\file3_fig\\3.png")
    
    plt.close()


def forth_plot(dataset: pd.DataFrame):
    df = dataset.select_dtypes(include=[np.uint8, np.uint32, float])
    plt.figure(figsize=(16,16))
    matplotlib.rc('font', size=18)
    sns.heatmap(df.corr(), annot=True, cmap="YlGnBu", cbar=False)
    plt.title("Корреляция", fontsize=24)
    plt.savefig(".\\file3_fig\\4.png")
    plt.close()


def fifth_plot(dataset : pd.DataFrame):
    # Отношение цены новых автомобилей к старым
    plt.figure(figsize=(28,10))
    data = dataset.groupby(["AIRLINE", "MONTH"], as_index=False, observed=False)["DAY_OF_WEEK"].count()    
    sns.barplot(data=data, x="DAY_OF_WEEK", y="AIRLINE", hue="MONTH")
    plt.title(label="Количество полетов airline распределенные по месяцу")
    plt.savefig(".\\file3_fig\\5.png")
    plt.close()


def main():
    need_dtypes = read_dtypes(".\\out3\\dtypes3.json")
    dataset = pd.read_csv(".\\out3\\df3.csv",
                          #usecols=lambda x: x in need_dtypes.keys(),
                          dtype=need_dtypes)    
    #dataset.info(memory_usage="deep")
    #print(dataset.info())
    
    #first_plot(dataset)
    #second_plot(dataset)
    #third_plot(dataset)
    forth_plot(dataset)
    fifth_plot(dataset)


if __name__ == "__main__":
    main()