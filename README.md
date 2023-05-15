# buenzli-corpus
Creating a swiss german corpus from the subreddit /r/buenzli

## Libraries

We are using the pushshift.io database to get historical reddit data for swiss german subreddits. The data is then filtered and cleaned using various libraries (TBD)

## Currently provided data
We currently provide comments.json, which contains all comments from the subreddit /r/buenzli from 23.05.2013 to 31.12.2022. The data has been anonymized and currently contains 67112 comments, totaling up to 1260587 words. This data has only been rudimentarily cleaned by removing deleted and empty comments.

## Future Plans

### Goals
- Remove non swiss-german text
- identify swiss french

### Potential Expansion
- POS Tagging
- Seperating Dialects
