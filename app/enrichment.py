from settings import *

from csv import DictWriter

from gensim.models import Phrases
from gensim.models.phrases import Phraser
from gensim.corpora import Dictionary

start_time = start_process('Enrichment')

# Train Phrases model
posts_stream = read_posts(clean_posts_csv, attribute='content', split=True)
bigram_model = Phrases(posts_stream, min_count=1)

# Create CSV
with open(data_folder+enriched_posts_csv, 'w', errors='surrogatepass') as result_file:
    writer = DictWriter(result_file, fieldnames=posts_header) 
    writer.writeheader()

# Make bi-grams
posts_stream = read_posts(clean_posts_csv)
for post in posts_stream:
    # Concatenate bi-grams
    post['content'] = post['content'].split()
    bigrams = [ bigram for bigram in bigram_model[post['content']] if '_' in bigram ]
    post['content'] += bigrams
    # Write in CSV
    post['content'] = ' '.join(post['content'])
    with open(data_folder+enriched_posts_csv, 'a', errors='surrogatepass') as result_file:
        writer = DictWriter(result_file, fieldnames=posts_header) 
        writer.writerow(post)

end_process(start_time)