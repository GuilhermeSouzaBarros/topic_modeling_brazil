import pandas as pd
import matplotlib.pyplot as plot
import seaborn
import umap

def plot_topics(documents, embeddings, topics, title):
    reducer = umap.UMAP(n_components=2)  # or TSNE(n_components=2)
    reduced_embeddings = reducer.fit_transform(embeddings)

    df = pd.DataFrame(reduced_embeddings, columns=["x", "y"])
    df['topic'] = topics

    # Plotting
    plot.figure(figsize=(8, 6))
    seaborn.scatterplot(data=df, x="x", y="y", hue="topic", palette="Set1", s=100, alpha=0.7)
    plot.title(title)
    plot.show()
    