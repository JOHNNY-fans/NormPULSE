import torch
import json
import faiss
from faiss import normalize_L2
from sentence_transformers import SentenceTransformer
from transformers import AutoConfig, AutoTokenizer

class StdLevelTree:
    def __init__(self, tree):
        self.tree = tree if isinstance(tree, dict) else json.load(
            open(tree, 'r', encoding='utf-8'))
        self.tree = dict(sorted(self.tree.items(),key=lambda x:-len(x[0]),reverse=True))
        self.depth = 0
        self.std_2_code = {}
        for k, v in self.tree.items():
            # self.std_2_code[v['term_name'].replace("（" + k + "）", '')] = k
            self.std_2_code[v['term_name']] = k
            self.std_2_code[v['term_name'].replace("（","(").replace("）",")")] = k
            self.depth = v['level'] if v['level'] > self.depth else self.depth

    def loacate_position(self, query):
        query = query.replace("（","(").replace("）",")")
        if query in self.tree.keys():
            return self.tree[query]
        else:
            return self.tree[self.std_2_code[query]]

    def get_depth(self):
        return max([self.tree[i]['level'] for i in self.tree])
    
    def get_father(self, query):
        return self.tree[self.loacate_position(query)['father']] if self.loacate_position(query)['father'] != None else None

    def get_children(self, query):
        if self.loacate_position(query)['child'] == None:
            return None
        if self.loacate_position(query)['child'] != None and self.loacate_position(query)['child'] != []:
            return [self.tree[code] for code in self.loacate_position(query)['child']]

    def get_father_code(self, query):
        return self.loacate_position(query)['father']

    def get_children_codes(self, query):
        self.loacate_position(query)['child']

    def generate_path(self, query):
        index = 0
        node = self.loacate_position(query)
        code = node['code']
        path = [node['term_name']]
        father_code = self.get_father_code(code)
        while father_code != None:
            path.append(self.tree[father_code]['term_name'])
            father_code = self.get_father_code(father_code)
            index += 1
            if index > self.depth:
                # print(std_code,std,code_tree[father_code]['father'])
                raise ValueError(
                    "The tree isn't a DAG! It may be cyclic in " + "---".join(path.reverse()))
        path.reverse()
        return path

    def detect_DAG(self):
        for k, v in self.tree.items():
            if v['level'] == self.depth:
                self.generate_path(k)
        return True

class Vec_Search_Controller:
    def __init__(self, model_name_or_path="moka-ai/m3e-base", init_kb=None):
        self.embedding_model = SentenceTransformer(model_name_or_path)
        self.embedding_model_tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
        self.embedding_model_config = AutoConfig.from_pretrained(model_name_or_path)
        if torch.cuda.is_available():
            self.embedding_model = self.embedding_model.cuda()
        if init_kb is not None:
            self.update_kb(init_kb)
        
    def update_kb(self, kb):
        if isinstance(kb,list):
            self.kb = list(set(kb))
            self.kb_dict = {}
            self.kb_vec = self.embedding_model.encode(self.kb)

        else:
            raise NotImplementedError('KB input should be a card dict or list')
        

    
    def vec_search(self, query, topN=20, index_list=None):
        # print(index_list.any())
        if index_list is not None:
            target_vecs = self.kb_vec[index_list]
            target_kb = np.array(self.kb)[index_list].tolist()
        else:
            target_vecs = self.kb_vec
            target_kb = self.kb
        if query == '':
            raise NotImplementedError('search input should be a query or query list')
        
        if isinstance(query,str):
            query = [query]
        if isinstance(query,list) and query!=[]:
            q = self.embedding_model.encode(query)
            index_l,_ = self.faiss_cosine_sim(q_vectors=q, training_vectors=target_vecs, topN=topN, d=self.embedding_model_config.hidden_size)
            return [[target_kb[i] for i in j] for j in index_l]
            
        else:
            raise NotImplementedError('search input should be a query or query list')
    
    def faiss_cosine_sim(self, q_vectors, training_vectors, topN, d):
        normalize_L2(training_vectors)
        normalize_L2(q_vectors)
        index=faiss.IndexFlatIP(d)        # the other index，需要以其他index作为基础
        index.train(training_vectors) 
        index.add(training_vectors)
        D, I =index.search(q_vectors, topN)
        score_list = D.tolist()
        index_list = I.tolist()
        return index_list,score_list