from nltk import TweetTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.svm import LinearSVC, SVC

from LexiconExtractor import LexiconExtractor
from POSExtractor import POSExtractor
from PictureCounterExtractor import PictureCounterExtractor
from Preprocessor import Preprocessor
from TwitterExtractor import TwitterExtractor
from baseline_model import read_corpus

message_train, label_train = read_corpus("datasets/train_dataset_30.csv")
message_test, label_test = read_corpus("datasets/test_dataset_30.csv")

preprocessor = Preprocessor(twitter_symbols='normalized', stemming=True).preprocess

pipeline = Pipeline([
    ('feats', FeatureUnion([
        ('vect', TfidfVectorizer(use_idf=False,
                                 preprocessor=preprocessor)),
        ('picture', PictureCounterExtractor()),
        #('pos', POSExtractor()),
        ('lexicon', LexiconExtractor()),
        ('abrev', TwitterExtractor())
    ])),
    ('clf', LinearSVC())
])


l = 99999999

pipeline.fit(message_train[:l], label_train[:l])

y_prediction = pipeline.predict( message_test[:l] )

report = classification_report( label_test[:l], y_prediction )

print(report)
print(accuracy_score(label_test[:l], y_prediction))