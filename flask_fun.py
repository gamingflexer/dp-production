import pandas as pd
from fastai.text.all import noop, DataBlock,ColReader,RandomSplitter,Learner,ranger,CrossEntropyLossFlat,partial
from transformers import BartForConditionalGeneration
from blurr.data.all import HF_Seq2SeqBlock,HF_Seq2SeqBeforeBatchTransform
from blurr.modeling.all import HF_BaseModelWrapper,HF_BaseModelCallback,HF_Seq2SeqMetricsCallback,BLURR,seq2seq_splitter
from config import summary_db

from fileconversion import fileconversion1
from preprocessing import*
from linkedIn import*
from model import*
from db import *
from flask_fun import * 


df = pd.read_csv(summary_db)
df = df[['Text','Summary']]

def Summary_run():
    df = pd.read_csv(summary_db)
    #Select part of data we want to keep
    df = df[['Text','Summary']]

    #Clean text
    df['Text'] = df['Text'].apply(lambda x: x.replace('\n',' '))
    df['Summary'] = df['Summary'].apply(lambda x: x.replace('\n',' '))


    pretrained_model_name = "facebook/bart-large-cnn"
    hf_arch, hf_config, hf_tokenizer, hf_model = BLURR.get_hf_objects(pretrained_model_name, 
                                                                    model_cls=BartForConditionalGeneration)

    #Create mini-batch and define parameters
    hf_batch_tfm = HF_Seq2SeqBeforeBatchTransform(hf_arch, hf_config, hf_tokenizer, hf_model, 
        task='summarization',
        text_gen_kwargs=
    {'max_length': 248,'min_length': 56,'do_sample': False, 'early_stopping': True, 'num_beams': 4, 'temperature': 1.0, 
    'top_k': 50, 'top_p': 1.0, 'repetition_penalty': 1.0, 'bad_words_ids': None, 'bos_token_id': 0, 'pad_token_id': 1,
    'eos_token_id': 2, 'length_penalty': 2.0, 'no_repeat_ngram_size': 3, 'encoder_no_repeat_ngram_size': 0,
    'num_return_sequences': 1, 'decoder_start_token_id': 2, 'use_cache': True, 'num_beam_groups': 1,
    'diversity_penalty': 0.0, 'output_attentions': False, 'output_hidden_states': False, 'output_scores': False,
    'return_dict_in_generate': False, 'forced_bos_token_id': 0, 'forced_eos_token_id': 2, 'remove_invalid_values': False})

    articles = df.head(100)

    #Prepare data for training
    blocks = (HF_Seq2SeqBlock(before_batch_tfm=hf_batch_tfm), noop)
    dblock = DataBlock(blocks=blocks, get_x=ColReader('Text'), get_y=ColReader('Summary'), splitter=RandomSplitter())
    dls = dblock.dataloaders(articles, batch_size = 1 )


    seq2seq_metrics = {
            'rouge': {
                'compute_kwargs': { 'rouge_types': ["rouge1", "rouge2", "rougeL"], 'use_stemmer': True },
                'returns': ["rouge1", "rouge2", "rougeL"]
            },
            'bertscore': {
                'compute_kwargs': { 'lang': 'fr' },
                'returns': ["precision", "recall", "f1"]}}

    #Model
    model = HF_BaseModelWrapper(hf_model)
    learn_cbs = [HF_BaseModelCallback]
    fit_cbs = [HF_Seq2SeqMetricsCallback(custom_metrics=seq2seq_metrics)]

    #Specify training
    global learn
    learn = Learner(dls, model,
                    opt_func=ranger,loss_func=CrossEntropyLossFlat(),
                    cbs=learn_cbs,splitter=partial(seq2seq_splitter, arch=hf_arch)).to_fp16()
    
    return "Model Loadded - Extractive summarization"


# functions
def convertToBinary(filename):
    with open(filename, 'rb') as file:
        binarydata = file.read()
    return binarydata


def convertBinaryToFile(binarydata, filename):
    with open(filename, 'wb') as file:
        file.write(binarydata)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#BERT
def process_resume2(text, tokenizer, max_len):
    tok = tokenizer.encode_plus(
        text, max_length=max_len, return_offsets_mapping=True)

    curr_sent = dict()

    padding_length = max_len - len(tok['input_ids'])

    curr_sent['input_ids'] = tok['input_ids'] + ([0] * padding_length)
    curr_sent['token_type_ids'] = tok['token_type_ids'] + \
        ([0] * padding_length)
    curr_sent['attention_mask'] = tok['attention_mask'] + \
        ([0] * padding_length)

    final_data = {
        'input_ids': torch.tensor(curr_sent['input_ids'], dtype=torch.long),
        'token_type_ids': torch.tensor(curr_sent['token_type_ids'], dtype=torch.long),
        'attention_mask': torch.tensor(curr_sent['attention_mask'], dtype=torch.long),
        'offset_mapping': tok['offset_mapping']
    }

    return final_data


def predict(model, tokenizer, idx2tag, tag2idx, device, test_resume):
    MAX_LEN = 512
    model.eval()
    data = process_resume2(test_resume, tokenizer, MAX_LEN)
    input_ids, input_mask = data['input_ids'].unsqueeze(
        0), data['attention_mask'].unsqueeze(0)
    labels = torch.tensor([1] * input_ids.size(0),
                          dtype=torch.long).unsqueeze(0)
    with torch.no_grad():
        outputs = model(
            input_ids,
            token_type_ids=None,
            attention_mask=input_mask,
            labels=labels,
        )
        tmp_eval_loss, logits = outputs[:2]

    logits = logits.cpu().detach().numpy()
    label_ids = np.argmax(logits, axis=2)

    entities = []
    for label_id, offset in zip(label_ids[0], data['offset_mapping']):
        curr_id = idx2tag[label_id]
        curr_start = offset[0]
        curr_end = offset[1]
        if curr_id != 'O':
            if len(entities) > 0 and entities[-1]['entity'] == curr_id and curr_start - entities[-1]['end'] in [0, 1]:
                entities[-1]['end'] = curr_end
            else:
                entities.append(
                    {'entity': curr_id, 'start': curr_start, 'end': curr_end})
    for ent in entities:
        ent['text'] = test_resume[ent['start']:ent['end']]
    return entities
