import torch
torch.cuda.is_available = lambda: False

from sentence_transformers import SentenceTransformer
from bertopic import BERTopic # pyright: ignore[reportMissingTypeStubs]
from sklearn.feature_extraction.text import CountVectorizer

from hdbscan import HDBSCAN # pyright: ignore[reportMissingTypeStubs]
import spacy
from scipy.cluster import hierarchy

from umap import UMAP # pyright: ignore[reportMissingTypeStubs]
from visualize import plot_topics

import joblib
import os
os.makedirs("bin", exist_ok=True)

MODEL_SENTENCE = "all-MiniLM-L6-v2"
def bert_get_topics(texts:list[str], num_topics:int=None, num_words:int=10):
    model_sentence = SentenceTransformer(MODEL_SENTENCE)

    try:
        embedding = joblib.load("bin/embeddings")
    except:
        print("\tFailed to load embeddings")
        embedding = model_sentence.encode(texts, show_progress_bar=True) # pyright: ignore[reportUnknownMemberType]
        try:
            joblib.dump(embedding, "bin/embeddings")
        except:
            print("\tFailed to save embeddings")

    nlp = spacy.load('en_core_web_sm')
    vectorizer_model = CountVectorizer(ngram_range=(1,2),
                                       stop_words=list(nlp.Defaults.stop_words))

    cluster_model = HDBSCAN(min_cluster_size=100, min_samples=25, metric='euclidean', prediction_data = True)
    
    topic_model = BERTopic(
        embedding_model=model_sentence,
        language='English',
        top_n_words=num_words,
        nr_topics="auto",
        verbose=True,
        calculate_probabilities=False,
        vectorizer_model = vectorizer_model,
        hdbscan_model=cluster_model
    )

    print("\nClustering topics...\n")
    topic, probs = topic_model.fit_transform(texts, embedding)
    topic = topic_model.reduce_outliers(texts, topic)
    print(topic_model.get_topic_info())

    linkage_function = lambda x: hierarchy.linkage(x, 'single', optimal_ordering=True)
    hier_topics = topic_model.hierarchical_topics(texts, linkage_function=linkage_function)

    fig_documents = topic_model.visualize_documents([x[:75] for x in texts], embeddings=embedding)
    fig_hierarchical = topic_model.visualize_hierarchy(hierarchical_topics=hier_topics)
    try:
        joblib.dump(fig_documents, "bin/fig_documents")
    except:
        print("failed to save fig_documents")

    try:
        joblib.dump(fig_hierarchical, "bin/fig_hierarchical")
    except:
        print("failed to save fig_hierarchical")
    fig_documents.show()
    fig_hierarchical.show()

    #plot_topics(texts, embedding, topic, "Topics predicted")
