import os
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt
from collections import Counter
from typing import List, Set
from nltk.corpus import stopwords


def lemmatize_text(
    text: str, lemmatizer: WordNetLemmatizer, stop_words: Set[str]
) -> List[str]:
    """
    Лемматизирует текст, удаляет стоп-слова и возвращает список лемматизированных слов.

    Параметры:
    text: Входной текст для лемматизации.
    lemmatizer: Экземпляр лемматизатора.
    stop_words: Множество стоп-слов.
    Возвращает:
    Список лемматизированных слов.
    """
    words = word_tokenize(text)
    lemmatized_words = [
        lemmatizer.lemmatize(word.lower())
        for word in words
        if word.isalnum() and word.lower() not in stop_words
    ]
    return lemmatized_words


def filter_dataframe_by_word_count(
    input_df: pd.DataFrame, word_count: int
) -> pd.DataFrame:
    """
    Фильтрует DataFrame по заданному количеству слов.

    Параметры:
    input_df: Входной DataFrame.
    word_count: Количество слов для фильтрации.
    Возвращает:
    Отфильтрованный DataFrame.
    """
    return input_df[input_df["Word Count"] == word_count]


def filter_dataframe_by_star_rating(
    input_df: pd.DataFrame, star_rating: int
) -> pd.DataFrame:
    """
    Фильтрует DataFrame по заданному рейтингу.

    Параметры:
    input_df: Входной DataFrame.
    star_rating: Рейтинг для фильтрации.
    Возвращает:
    Отфильтрованный DataFrame.
    """
    return input_df[input_df["Star Rating"] == str(star_rating)]


def plot_word_histogram(
    df: pd.DataFrame,
    class_label: str,
    lemmatizer: WordNetLemmatizer,
    stop_words: Set[str],
) -> None:
    """
    Строит гистограмму слов для заданного класса в DataFrame.

    Параметры:
    df: Входной DataFrame.
    class_label: Метка класса для построения гистограммы.
    lemmatizer: Экземпляр лемматизатора.
    stop_words: Множество стоп-слов.
    """
    class_texts = df[df["Star Rating"] == class_label]["Review Text"].values
    all_words = [
        word
        for text in class_texts
        for word in lemmatize_text(text, lemmatizer, stop_words)
    ]
    word_counter = Counter(all_words)
    common_words = word_counter.most_common(20)

    words, counts = zip(*common_words)

    plt.figure(figsize=(10, 6))
    bars = plt.bar(words, counts, color="red")
    plt.title(f"Word Histogram for Class Label {class_label}")
    plt.xlabel("Words")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45, ha="right")

    for bar, count in zip(bars, counts):
        plt.text(
            bar.get_x() + bar.get_width() / 2 - 0.15,
            bar.get_height() + 0.1,
            str(count),
            ha="center",
            va="bottom",
        )

    plt.show()


data_folder_path: str = r"D:\PPLabs\lab4\dataset"
stop_words: Set[str] = set(stopwords.words("russian"))
lemmatizer: WordNetLemmatizer = WordNetLemmatizer()
max_word_count_filter: int = 5
star_rating_filter: str = "4"

data: dict = {"Star Rating": [], "Review Text": []}
for root, dirs, files in os.walk(data_folder_path):
    for filename in files:
        file_path = os.path.join(root, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                folder_number = os.path.basename(root)
                data["Star Rating"].append(folder_number)
                data["Review Text"].append(content)

df: pd.DataFrame = pd.DataFrame(data)

df["Review Text"].fillna("Комментарий отсутствует", inplace=True)

df["Word Count"] = df["Review Text"].apply(lambda x: len(str(x).split()))

csv_filename: str = "data.csv"
df.to_csv(csv_filename, index=False)

filtered_dataframe_by_word_count: pd.DataFrame = filter_dataframe_by_word_count(
    df, max_word_count_filter
)
filtered_csv_filename_word_count: str = "filtered_data_word_count.csv"
filtered_dataframe_by_word_count.to_csv(filtered_csv_filename_word_count, index=False)

filtered_dataframe_by_star_rating: pd.DataFrame = filter_dataframe_by_star_rating(
    df, star_rating_filter
)

filtered_csv_filename_star_rating: str = (
    f"filtered_data_star_rating_{star_rating_filter}.csv"
)
filtered_dataframe_by_star_rating.to_csv(filtered_csv_filename_star_rating, index=False)

numeric_info_word_count: pd.DataFrame = df[["Word Count"]].describe()
print("\nStatistical Information on Word Count:")
print(numeric_info_word_count)

grouped_by_star: pd.DataFrame = df.groupby("Star Rating")["Word Count"].agg(
    ["max", "min", "mean"]
)
print("\nGrouped DataFrame by Star Rating with Maximum, Minimum, and Mean Word Count:")
print(grouped_by_star)

class_label_to_plot: str = "1"
plot_word_histogram(df, class_label_to_plot, lemmatizer, stop_words)
