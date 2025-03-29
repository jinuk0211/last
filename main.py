from model import qwen
from mctstask import MCTS_Task
from node import treeNode
from mcts import selectNode, get_next_steps_expand, expand

from vlmeval.dataset import build_dataset
import torch
import os
import os.path as osp
import pandas as pd
from PIL import Image
from transformers import Qwen2_5_VLForConditionalGeneration, AutoTokenizer, AutoProcessor
from qwen_vl_utils import process_vision_info
from easydict import EasyDict

os.environ["OPENAI_API_KEY"] = "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"# Replace with your 
os.environ["OPENAI_API_BASE"] = "https://api.openai.com/v1/chat/completions" # Replace with your actual base
api_key = os.getenv("OPENAI_API_KEY")
api_base = os.getenv("OPENAI_API_BASE")


def run(args):
    print('-'*30, 'Begin testing', '-'*30, '\n')
    try:
        dataset_kwargs = {}
        dataset_name = args.dataset#"MathVista_MINI"
        dataset = build_dataset(dataset_name, **dataset_kwargs)

        data_len = len(dataset.data)
    except Exception as e:
        print(f'File must be standardized json!\nError type:{e}\n')
        return
    assert data_len > 0, "Data list is empty!\n"

    model, processor = qwen('Qwen2_5')
    output_list = []
    correct_count = 0
    for i in len(dataset.data):
        image = dataset.data.iloc[i]['image']
        dataset.dump_image(dataset.data.iloc[i])
        img = osp.join(dataset.img_root, f"{dataset.data.iloc[i]['index']}.jpg")
        question = dataset.data.iloc[i]['question']
        if not pd.isnull(dataset.data.iloc[i]['choices']):
            choices = dataset.data.iloc[i]['choices']

# base_args.add_argument('--propose_method', type=str, choices=['gpt', 'glm', 'llama', 'local'], default='glm')
# base_args.add_argument('--value_method', type=str, choices=['gpt', 'glm', 'local'], default='local')
        Task = MCTS_Task(question, model, processor, args.propose_method, args.value_method, args.branch, args.end_gate,
                            args.roll_policy, args.roll_branch, args.roll_forward_steps, args.time_limit,
                            args.iteration_limit, args.exploration_constant, args.alpha, args.inf,
                            args.temperature, use_case_prompt=args.use_case_prompt, use_reflection=args.use_reflection,
                            low=args.low, high=args.high, evaluate=args.evaluate,img_path=img)
        output, root = Task.run()

        # evaluate metrics
        if args.evaluate:
            dataset.data['prediction'] = output
            dataset.data = dataset.data.drop(columns=['image'])
        output_path = '/content/output/dataset.xlsx'
        dataset.data.to_excel(output_path, index=False)
        judge_kwargs = {
            'nproc': 4,
            'verbose': False,
            'retry': 3,
            'model': "gpt_4o_mini"}

        eval_results = dataset.evaluate('/content/output/dataset.xlsx', **judge_kwargs)
        # output

    



def get_args():
    args = EasyDict({
        'task_name': 'scibench',
        'file': 'thermo_standardized',
        'propose_method': 'qwen',  # choices: ['qwen', 'gpt', 'llamaV_o1', 'llama3', 'llava']
        'value_method': 'qwen',  # choices: ['gpt', 'glm', 'local']
        'mode': 'mcts',  # choices: ['cot', 'tot', 'mcts']
        'temperature': 0.7,
        'time_limit': None,
        'iteration_limit': 30,
        'roll_policy': 'greedy',  # choices: ['random', 'greedy']
        'exploration_constant': 0.4,
        'roll_forward_steps': 2,
        'end_gate': 0.9,  # End threshold
        'branch': 3,
        'roll_branch': 1,
        'inf': 0.8,
        'evaluate': 'mathvista',  # Empty string means no evaluation
        'alpha': 0.5,
        'visualize': False,  # visualization
        'use_case_prompt': False,  # Use sample prompts
        'use_reflection': 'simple',  # choices: ['simple', 'common']
        'low': 0.0,
        'high': 1.0,
        'algorithm': 'dfs',  # choices: ['dfs', 'bfs']
        'select_branch': 2,
        'max_depth': 8,
        'select_method': 'greedy',  # choices: ['greedy', 'sample']
        'consistency': True,
        'model': '',
        'dataset': 'MathVista_MINI',
        'judge_args': None,
        'llamaV_o1': None,
        'Qwen2_5': "Qwen/Qwen2.5-VL-3B-Instruct",
        'llama3_vision_11b_model_path': None,
        'llava_next_8b_model_path': None,
        'openai_api_key': None,
        'openai_base_url': 'https://api.openai.com/v1',
        'dataset' :  'MathVista_MINI',
        'clip_model_path': 'openai/clip-vit-large-patch14-336'
        # --gpt_version 'gpt-4o' \


    })
    return args

# Example usage
args = get_args()
print(args.task_name)  # 'scibench'

if __name__ == "__main__":
    torch.cuda.empty_cache()
    
    dataset_kwargs = {}
    dataset_name = "MathVista_MINI"
    dataset = build_dataset(dataset_name, **dataset_kwargs)
    args = get_args()
    print(args.task_name)

    # clip_model = CLIPModel.from_pretrained(args.clip_model_path)
    # clip_processor = AutoProcessor.from_pretrained(args.clip_model_path)
    data_len = len(dataset.data)
    # for i in range(len(dataset.data)):
    image = dataset.data.iloc[1]['image']
    dataset.dump_image(dataset.data.iloc[1])
    img_path = osp.join(dataset.img_root, f"{dataset.data.iloc[1]['index']}.jpg")
    question = dataset.data.iloc[1]['question']
    model, processor = qwen('Qwen2_5')
    task = MCTS_Task(question, model, processor, args.propose_method, args.value_method, args.branch, args.end_gate,
                    args.roll_policy, args.roll_branch, args.roll_forward_steps, args.time_limit,
                    args.iteration_limit, args.exploration_constant, args.alpha, args.inf,
                    args.temperature, use_case_prompt=args.use_case_prompt, use_reflection=args.use_reflection,
                    low=args.low, high=args.high, evaluate=args.evaluate, img_path ='/root/LMUData/images/MathVista_MINI/2.jpg')
    root = treeNode('')
    flag, node = selectNode(root, task)
    actions = get_next_steps_expand(node, task)
    print(actions)
    node = expand(node, task)
    reflection = task.get_simple_reflection(node.y, node.depth + 1)
    print(f'reflection:{reflection}')
    print(node.y)
    print(f'root.reflection:{root.reflection}')
    print(node.children)
    print(f'node.reflection:{node.reflection}')