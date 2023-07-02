from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoTokenizer, AutoModelForCausalLM
import uvicorn, json, datetime
import torch
from utils import Vec_Search_Controller, StdLevelTree

DEVICE = "cuda"
DEVICE_ID = "0"
CUDA_DEVICE = f"{DEVICE}:{DEVICE_ID}" if DEVICE_ID else DEVICE


def torch_gc():
    if torch.cuda.is_available():
        with torch.cuda.device(CUDA_DEVICE):
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()


app = FastAPI(
	title='normpulse_server',
	version='1.0.0'
)
app.add_middleware(
    CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=False,
	allow_methods=["*"],
	allow_headers=["*"],
)



@app.post("/retrival")
async def cand_retrival(request: Request):
    global dis_vec_engine, dis_level_tree, op_vec_engine, op_level_tree, dis_name2code, op_name2code
    json_post_raw = await request.json()
    json_post = json.dumps(json_post_raw)
    json_post_list = json.loads(json_post)
    term_type = json_post_list.get('term_type')
    topN = json_post_list.get('topN')
    mention = json_post_list.get('mention')
    level = json_post_list.get('level')
    history = json_post_list.get('history')
    
    search_input = [mention]
    
    if term_type == 'disease':
        search_result = dis_vec_engine.vec_search(query=search_input,topN=topN)
        search_tree_result = [dis_level_tree.generate_path(i) for i in search_result[0]]
        max_depth = dis_level_tree.depth
        search_tree_result = [i+[[]]*(max_depth-len(i)) for i in search_tree_result]
        
    elif term_type == 'operation':
        search_result = op_vec_engine.vec_search(query=search_input,topN=topN)
        search_tree_result = [op_level_tree.generate_path(i) for i in search_result[0]]
        max_depth = op_level_tree.depth
        search_tree_result = [i+['pad']*(max_depth-len(i)) for i in search_tree_result]
        
    else:
        raise(NotImplementedError('term_type should be within the limits of disease and operation'))
    
    cand_list = []
    
    if history==[]:
        for item in search_tree_result:
            if term_type == 'disease':
                cand_item = dis_code[dis_name2code[level-1][item[level-1]]]
                if cand_item not in cand_list:
                    cand_list.append(cand_item) 
                
            elif term_type == 'operation':
                cand_item = op_code[op_name2code[level-1][item[level-1]]]
                if cand_item not in cand_list:
                    cand_list.append(cand_item)
                
            else:
                raise(NotImplementedError('term_type should be within the limits of disease and operation'))

    else:
        last_level_answer = history[-1][-1].split('推荐可能对应的标准词为：')[-1].split('##')
        if term_type == 'disease':
            last_level_answer_code = [dis_name2code[level-2][i] for i in last_level_answer]
            for item in search_tree_result:
                if item[level-1] == 'pad':
                    continue
                cand_item = dis_code[dis_name2code[level-1][item[level-1]]]
                if cand_item not in cand_list and dis_code[dis_name2code[level-1][item[level-1]]]['father'] in last_level_answer_code:
                    cand_list.append(cand_item)
            for add_c in dis_code[dis_code[dis_name2code[level-1][item[level-1]]]['father']]['child']:
                if dis_code[add_c] not in cand_list:
                    cand_list.append(dis_code[add_c])
                    
        elif term_type == 'operation':
            last_level_answer_code = [op_name2code[level-2][i] for i in last_level_answer]
            for item in search_tree_result:
                if item[level-1] == 'pad':
                    continue
                cand_item = op_code[op_name2code[level-1][item[level-1]]]
                
                if cand_item not in cand_list and op_code[op_name2code[level-1][item[level-1]]]['father'] in last_level_answer_code:
                    cand_list.append(cand_item)
            for add_c in op_code[op_code[op_name2code[level-1][item[level-1]]]['father']]['child']:
                if op_code[add_c] not in cand_list:
                    cand_list.append(op_code[add_c])
                    
    return {'mention':mention,'cand':cand_list,'level':level,'term_type':term_type,'max_depth':max_depth}


@app.post("/generate")
async def model_gen(request: Request):
    global model, tokenizer, dis_level_tree, op_level_tree, dis_name2code, op_name2code
    
    # all_dis_name = sum([list(i) for i in dis_name2code],[])
    # all_op_name = sum([list(i) for i in op_name2code],[])
    
    json_post_raw = await request.json()
    json_post = json.dumps(json_post_raw)
    json_post_list = json.loads(json_post)
    prompt = json_post_list.get('prompt')
    term_type = json_post_list.get('term_type')
    task_type = json_post_list.get('task_type')
    
    input_max_length = 256
    top_p = 0.7
    temperature = 1.0
    
    if task_type=='kc':
        do_sample = True
        gen_max_length = 512
    elif task_type=='norm':
        do_sample=False
        gen_max_length = 128

    first_instruction = "Instructions: You are Helper, a large language model full of intelligence. Respond conversationally."
    
    prompt = prompt.strip() 

    input_ids = tokenizer(
        first_instruction,
        add_special_tokens=False
    ).input_ids + [tokenizer.convert_tokens_to_ids("</s>")]
    
    
    input_ids += tokenizer("User: " + prompt, add_special_tokens=False).input_ids
    input_ids += [tokenizer.convert_tokens_to_ids("</s>")]  

    model_inputs = tokenizer.pad(
        {"input_ids": [input_ids + tokenizer("Helper: ", add_special_tokens=False).input_ids[:1]]}, 
        return_tensors="pt",
    )

    inputs = model_inputs.input_ids[:,-input_max_length:]
    attention_mask = model_inputs.attention_mask[:,-input_max_length:]

    max_length = inputs.shape[1] + gen_max_length
    min_length = inputs.shape[1] + 1 # add eos

    outputs = model.generate(
        inputs=inputs.cuda(),
        attention_mask=attention_mask.cuda(),
        max_length=max_length,
        min_length=min_length,
        do_sample=do_sample,
        top_p=top_p,
        temperature=temperature,
        num_return_sequences=1,
        eos_token_id=tokenizer.convert_tokens_to_ids("</s>"),
    )

    outputs_token = outputs[0].tolist()

    new_start_pos = inputs.shape[1]
    new_end_pos = new_start_pos

    while new_end_pos < len(outputs_token) and outputs_token[new_end_pos] != tokenizer.convert_tokens_to_ids("</s>"):
        new_end_pos += 1

    outputs_token = list(tokenizer("Helper: ", add_special_tokens=False).input_ids[:1]) + outputs_token[new_start_pos:new_end_pos]

    input_ids += outputs_token
    input_ids += [tokenizer.convert_tokens_to_ids("</s>")] 

    otext = tokenizer.decode(
        outputs_token, 
        skip_special_tokens=False
    )[8:]
       
    if task_type=='kc':
        return {'model_output':otext}
    elif task_type=='norm':
        
        inference_answer = otext.split('推荐可能对应的标准词为：')[-1]
        if term_type == 'disease':
            inference_answer_path = [dis_level_tree.generate_path(i) for i in inference_answer.split('##')]
        elif term_type == 'operation':
            inference_answer_path = [op_level_tree.generate_path(i) for i in inference_answer.split('##')]
        else:
            raise(NotImplementedError('term_type should be within the limits of disease and operation'))
        
        return {'model_output':otext,'inference_answer_path':inference_answer_path}
    else:
        raise(NotImplementedError('More tasks are under construction'))
        


if __name__ == '__main__':
    model_name_or_path = 'Johnnyfans/normpulse'
    vec_model_name_or_path = 'moka-ai/m3e-base'
    op_tree_path = '../data/ICD-9-CM3_医保v2_tree.json'
    dis_tree_path = '../data/ICD-10_医保v2_tree.json'
    
    
    tokenizer = AutoTokenizer.from_pretrained(
        pretrained_model_name_or_path = model_name_or_path,
        padding_side='left',
    )
    model = AutoModelForCausalLM.from_pretrained(
        pretrained_model_name_or_path = model_name_or_path,
        torch_dtype=torch.float16,
        device_map = 'auto'
    )
    model.eval()
    
    with open(dis_tree_path,'r+', encoding='utf-8') as f:
        dis_code = json.load(f)
    with open(op_tree_path, 'r+', encoding='utf-8') as f:
        op_code = json.load(f)
        
    dis_level_tree = StdLevelTree(tree=dis_code)
    op_level_tree = StdLevelTree(tree=op_code)

    dis_code_card = list(set([dis_code[i]['term_name'] for i in dis_code]))
    op_code_card = list(set([op_code[i]['term_name'] for i in op_code]))
    
    dis_vec_engine = Vec_Search_Controller(model_name_or_path=vec_model_name_or_path, init_kb=dis_code_card)
    op_vec_engine = Vec_Search_Controller(model_name_or_path=vec_model_name_or_path, init_kb=op_code_card)
    
    dis_name2code = [{} for _ in range(dis_level_tree.depth)]
    for dis_c in dis_code:
        dis_name2code[dis_code[dis_c]['level']-1].update({dis_code[dis_c]['term_name']:dis_c})
    
    op_name2code = [{} for _ in range(op_level_tree.depth)]
    for op_c in op_code:
        op_name2code[op_code[op_c]['level']-1].update({op_code[op_c]['term_name']:op_c})
    
    uvicorn.run(app, host='localhost', port=2233, workers=1)
