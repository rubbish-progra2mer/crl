import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel, AutoProcessor, Blip2Model
from PIL import Image
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


BERT_tokenizer = BertTokenizer.from_pretrained('/data3/wuzh/Karios_DPO/BERT')
BERT_model = BertModel.from_pretrained('/data3/wuzh/Karios_DPO/BERT').to(device).eval()


blip_processor = AutoProcessor.from_pretrained("/data3/wuzh/Salesforce/blip2-opt-2.7b")
blip_model = Blip2Model.from_pretrained("/data3/wuzh/Salesforce/blip2-opt-2.7b").to(device).eval()

def get_text_embedding(text):
    inputs = BERT_tokenizer(text, return_tensors='pt', truncation=True, padding=True).to(device)
    with torch.no_grad():
        outputs = BERT_model(**inputs)
    embeddings = outputs.last_hidden_state
    sentence_embedding = embeddings.mean(dim=1)
    return sentence_embedding.cpu().numpy()

def get_image_embedding(image_path):
    with Image.open(image_path) as img:
        inputs = blip_processor(images=img, return_tensors="pt").to(device)
        features = blip_model.get_image_features(**inputs).pooler_output
    return features.detach().cpu().numpy()

with open('/data3/wuzh/kairosv2_eddpo/meta.json', 'r') as f:
    data = json.load(f)

for item in data:
    text_embed = get_text_embedding(item['goal'])

    image_embed = get_image_embedding(item['image_path'])

    print("text_embed dimension:", text_embed.shape) 
    print("image_embed dimension:", image_embed.shape) 
    combined_embed = np.concatenate([text_embed, image_embed], axis=1)
    item['embedding'] = combined_embed.tolist()

with open('/data3/wuzh/meta_embedding.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)