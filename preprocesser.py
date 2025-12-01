from pathlib import Path
import re

import os
os.makedirs("preprocessed", exist_ok=True)

if __name__ == "__main__":
    dir_str_articles = "brazil_wikipedia_articles"
    dir_path_articles = Path(dir_str_articles)
    if not dir_path_articles.is_dir():
        print("Articles directory not found: ", dir_path_articles)
        exit()

    dir_str_preprocessed = "preprocessed"
    dir_path_preprocessed = Path(dir_str_preprocessed)

    for file_path_article in dir_path_articles.iterdir():
        with open(file_path_article, "r") as article:
            article_preprocessed = str.join(" ", article.readlines())
            article_preprocessed = re.sub(r'==.*==', '\n', article_preprocessed, flags=re.M)
            article_preprocessed = re.sub(r'\s\s+', ' ', article_preprocessed, flags=re.M)
        
        file_str_preprocessed = str(file_path_article).replace(dir_str_articles, dir_str_preprocessed)
        file_path_preprocessed = Path(file_str_preprocessed)

        with open(file_path_preprocessed, "w") as preprocessed:
            preprocessed.writelines(article_preprocessed)
        
    