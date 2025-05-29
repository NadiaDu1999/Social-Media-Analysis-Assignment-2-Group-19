import re
from nltk.stem import PorterStemmer

class RedditProcess:
    """
    This class is used to pre-process Reddit posts. This class is based on the RedditProcessing class
    created by @author Jeffrey Chan, RMIT University, 2023.
    In this class, additional functions are added and listed below:
        1. Remove numbers (including decimals)
        2. Remove tokens containing any digits
        3. Remove empty tokens
        4. Apply the stemmer
    """

    def __init__(self, tokeniser, lStopwords, stemmer=None):
        """
        Initialise the tokeniser and set of stopwords to use.

        @param tokeniser: The tokenizer (e.g., TweetTokenizer)
        @param lStopwords: List of stopwords to be removed
        """
        self.tokeniser = tokeniser
        self.lStopwords = lStopwords
        self.stemmer = stemmer if stemmer is not None else PorterStemmer()

    def process(self, text): 
        """
        Perform the processing.
        
        @param text: the text (e.g., Reddit post) to process

        @returns: list of stemmed (valid) tokens in text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Tokenize
        tokens = self.tokeniser.tokenize(text)
        
        # Strip whitespace from each token
        tokensStripped = [tok.strip() for tok in tokens]
        
        # Regular expression pattern to filter out URLs
        regexHttp = re.compile("^http")
        
        # Filter tokens:
        filtered_tokens = [
            tok for tok in tokensStripped 
            if tok not in self.lStopwords              # Remove stopwords
            and not tok.replace('.', '', 1).isdigit()    # Remove numbers (including decimals)
            and not any(c.isdigit() for c in tok)         # Remove tokens containing any digits
            and not regexHttp.match(tok)                 # Remove URLs
            and tok                                     # Remove empty tokens
        ]
        
        # Apply the stemmer to the filtered tokens
        stemmed_tokens = [self.stemmer.stem(tok) for tok in filtered_tokens]
        
        return stemmed_tokens


