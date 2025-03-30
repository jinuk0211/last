import torch
from transformers import Qwen2VLForConditionalGeneration, AutoTokenizer, AutoProcessor, Qwen2_5_VLForConditionalGeneration
#  MllamaForConditionalGeneration
from qwen_vl_utils import process_vision_info

def qwen(model):
#Qwen/Qwen2.5-VL-7B-Instruct
    if model == 'Qwen2_5':
        print('init qwen2.5 vl 7b model')
        Qwen2_5 = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            'Qwen/Qwen2.5-VL-7B-Instruct', torch_dtype=torch.bfloat16, device_map="auto", 
            # attn_implementation='flash_attention_2',
        )
        # min_pixels = 256*28*28
        # max_pixels = 1280*28*28
        # Qwen2_5_processor = AutoProcessor.from_pretrained(args.Qwen2_5, min_pixels=min_pixels, max_pixels=max_pixels)
        Qwen2_5_processor = AutoProcessor.from_pretrained("Qwen/Qwen2.5-VL-7B-Instruct")

        return Qwen2_5, Qwen2_5_processor


def get_proposal(model, processor, prompt, img_path):
    #temperature=0.7, max_tokens=2048, seed=170, max_length=2048, truncation=True,do_sample=True, max_new_tokens=1024
    
    response = []
    cnt = 2
    while not response and cnt:
        cnt -= 1
        messages = [{"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."},
                    { "role": "user", 
                    "content": [{"type": "image", "image": f"file://{img_path}"},
                    {"type": "text", "text": f"{prompt}"},],
                    }]
        text = processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        image_inputs, video_inputs = process_vision_info(messages)
        inputs = processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
        )
        inputs = inputs.to("cuda")

        # Inference: Generation of the output
        generated_ids = model.generate(**inputs, max_new_tokens=128)
        generated_ids_trimmed = [
            out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]
        response = processor.batch_decode(
            generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False)

    if not response:
        print(f'obtain<qwen>response fail!\n')
        return []
    return response[0]





