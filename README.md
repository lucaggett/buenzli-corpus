# buenzli-corpus
Creating a swiss german corpus from the subreddit /r/buenzli

## Libraries

We are using the pushshift.io database to get historical reddit data for swiss german subreddits. The data is then filtered and cleaned using various libraries (TBD)

## Currently provided data
We currently provide comments.json, which contains all comments from the subreddit /r/buenzli from 23.05.2013 to 31.12.2022. The data has been anonymized and currently contains 58951 comments, totaling up to 1246336 words. This data has been cleaned by removing all deleted and empty comments, as well as removing all comments containing no swiss-german words (swiss german word list generated from [NOAHs Corpus](https://github.com/noe-eva/NOAH-Corpus))

## Future Plans

### Goals
- Remove non swiss-german text
- identify swiss french

### Potential Expansion
- POS Tagging
- Seperating Dialects