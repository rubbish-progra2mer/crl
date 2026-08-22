import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel, AutoProcessor, Blip2Model
from PIL import Image
import torch


with open('/data3/wuzh/Karios_DPO/DPO_embedding.json', 'r') as f:
    all_data = json.load(f)


embeddings = np.array([item['embedding'][0] for item in all_data])
similarity_matrix = cosine_similarity(embeddings)

m = 0.95
k_values = [9,10]

for k in k_values:
    result_list = []
    
    for idx, item in enumerate(all_data):
        if item['DPO'] == False:
            # 获取相似度排序后的候选索引
            similarities = similarity_matrix[idx]
            candidates = [(sim, i) for i, sim in enumerate(similarities) if sim >= m]
            candidates.sort(reverse=True, key=lambda x: x[0])
            selected_indices = [i for (s, i) in candidates[:k]]
            
            for selected_idx in selected_indices:
                matched = all_data[selected_idx]
                new_item = {k: v for k, v in matched.items() if k != 'embedding'}
                
                if matched['DPO']:
                    new_item['DPO_action'] = matched['osatlas_action']
                    score = matched['score']
                    new_item['DPO_score'] = 1 if score in {4, 5} else 5
                
                result_list.append(new_item)
    
    # 保存结果
    output_path = f'/data3/wuzh/Karios_DPO/DPO_k={k}.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result_list, f, ensure_ascii=False)
