import pickle
import json
import spacy
import random
from spacy.util import minibatch, compounding 
from pathlib import Path
import os

#LABEL = ['Email Address', 'Links', 'Skills', 'Graduation Year', 'College Name', 'Degree', 'Companies worked at', 'Location', 'Name', 'Designation', 'projects', 'Years of Experience', 'Can Relocate to', 'UNKNOWN', 'Rewards and Achievements', 'Address', 'University', 'Relocate to', 'Certifications', 'state', 'links', 'College', 'training', 'des', 'abc']

def custom_nlp_train(filename):
    with open(filename, 'rb') as fp:
        doc = pickle.load(fp)
    
    ## Creating a blank spacy model
    nlp = spacy.blank('en')
    print("Created a blank en model")

    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner)
        print("Added ner pipe")
    else:
        ner.get_pipe('ner')

    # for i in LABEL:
    #     ner.add_label(i)


    # add labels
    for _, annotations in doc:
        for ent in annotations.get('entities'):
            ner.add_label(ent[2])
        
    optimizer = nlp.begin_training()
    
    for itn in range(30):
                random.shuffle(doc)
                losses = {}
                # batch up the examples using spaCy's minibatch
                batches = minibatch(doc, size=compounding(4.0, 32.0, 1.001))
                for batch in batches:
                    texts, annotations = zip(*batch)
                    nlp.update(
                        texts,  # batch of texts
                        annotations,  # batch of annotations
                        drop=0.3,  # dropout - make it harder to memorise data
                        losses=losses,
                    )
                print("Losses", losses)

    output_dir = os.path.dirname(os.path.realpath(__file__)) + "/training_data"
    new_model_name="customspacy"
    output_dir = Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir()

    nlp.meta["name"] = new_model_name  # rename model
    nlp.to_disk(output_dir)
    print("Saved model to", output_dir)           
            

    


if __name__ == "__main__":
    custom_nlp_train('model/forTraining')   