import joblib
from sys import argv

if __name__=="__main__":
    documents = joblib.load("bin/fig_documents_" + str(argv[1]) + "_" + str(argv[2]))
    hierarchical = joblib.load("bin/fig_hierarchical_" + str(argv[1]) + "_" + str(argv[2]))
    documents.show()
    hierarchical.show()
