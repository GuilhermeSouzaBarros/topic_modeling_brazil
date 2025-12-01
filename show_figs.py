import joblib

if __name__=="__main__":
    documents = joblib.load("bin/fig_documents")
    hierarchical = joblib.load("bin/fig_hierarchical")
    documents.show()
    hierarchical.show()
