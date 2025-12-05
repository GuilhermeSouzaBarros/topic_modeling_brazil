from modeling_bert import bert_get_topics
from pathlib import Path

from sys import argv

def main():
    num_topics = None
    num_words = 5
    if len(argv) > 1: num_topics = None if argv[1] == 'None' else int(argv[1])
    if len(argv) > 2: min_documents = int(argv[2])

    dir_path_preprocessed = Path("preprocessed")
    if not dir_path_preprocessed.is_dir():
        print("Could not find preprocessed folder:", dir_path_preprocessed)
        exit()

    print("Loading articles...", end=" ", flush=True)
    titles = []
    data = []
    for file_path_preprocessed in dir_path_preprocessed.iterdir():
        with open(file_path_preprocessed, "r") as preprocessed:
            titles.append(
                str(file_path_preprocessed) \
                            .replace(".txt", "") \
                            .replace("preprocessed/", "")
                        )
            data.append(preprocessed.readline())

    print(f" Finished (loaded {len(data)})\n\n")

    print(f"Topic modeling with BERTopic (n_topics: {num_topics})\n")
    bert_get_topics(titles, data, num_topics, min_documents)
    
if __name__ == "__main__":
    main()
