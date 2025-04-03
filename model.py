from PIL import Image
import torch
from transformers import Qwen2VLForConditionalGeneration, AutoTokenizer, AutoProcessor, Qwen2_5_VLForConditionalGeneration
from transformers import AutoModelForCausalLM, MllamaForConditionalGeneration
#  MllamaForConditionalGeneration
from qwen_vl_utils import process_vision_info
def LLM(model):
    model_dict = {}
    if model == 'qwen':
        print('init llm model')       
        model_name = "Qwen/Qwen2.5-7B-Instruct"
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype="auto",
            device_map="auto"
        )
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model_dict['model'] = model
        model_dict['tokenizer'] = tokenizer
        return model, tokenizer, model_dict
def llm_proposal(model,tokenizer,prompt,model_name='qwen'):
    if model_name =='qwen':
        messages = [ {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."},
            {"role": "user", "content": prompt}]
        text = tokenizer.apply_chat_template(
            messages, tokenize=False,
            add_generation_prompt=True)
        
        model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

        generated_ids = model.generate(
            **model_inputs, max_new_tokens=512)
        
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)]

        response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return response   
def llama(model):
    if model == 'llama':
        print('init llama 3.2 vision 11b model')
        model_id = "meta-llama/Llama-3.2-11B-Vision-Instruct"
        model = MllamaForConditionalGeneration.from_pretrained(
            model_id,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )
        processor = AutoProcessor.from_pretrained(model_id)
        return model, processor

def qwen(model):
#Qwen/Qwen2.5-VL-7B-Instruct
    if model == 'Qwen2_5':
        print('init qwen2.5 vl 7b model')
        Qwen2_5 = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            'Qwen/Qwen2.5-VL-7B-Instruct', torch_dtype=torch.bfloat16, device_map="auto", 
            # attn_implementation='flash_attention_2',
        )
        min_pixels = 256*28*28
        max_pixels = 1280*28*28
        Qwen2_5_processor = AutoProcessor.from_pretrained("Qwen/Qwen2.5-VL-7B-Instruct", min_pixels=min_pixels, max_pixels=max_pixels)
        # Qwen2_5_processor = AutoProcessor.from_pretrained()

        return Qwen2_5, Qwen2_5_processor


def get_proposal(model, processor, prompt, img_path, model_name ='llama'):
    #temperature=0.7, max_tokens=2048, seed=170, max_length=2048, truncation=True,do_sample=True, max_new_tokens=1024
    if model_name == 'qwen':
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
            generated_ids = model.generate(**inputs, max_new_tokens=512)
            generated_ids_trimmed = [
                out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
            ]
            response = processor.batch_decode(
                generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False)

        if not response:
            print(f'obtain<qwen>response fail!\n')
            return []
        return response[0]

    elif model_name == 'llama':

        image = Image.open(img_path)

        messages = [
            {"role": "user", "content": [
                {"type": "image"},{"type": "text","text": f"{prompt}"}]}
                ]
        input_text = processor.apply_chat_template(messages, add_generation_prompt=True)
        inputs = processor(
            image,
            input_text,
            add_special_tokens=False,
            return_tensors="pt"
        ).to(model.device)

        output = model.generate(**inputs, max_new_tokens=512)
        output_text = processor.decode(output[0])
        split_text = output_text.split("<|end_header_id|>", 2)  # 최대 2번만 분할

        # 두 번째 "<|end_header_id|>" 이후 부분 가져오기 (있다면)
        cleaned_text = split_text[2].strip()
        cleaned_text = cleaned_text.replace("<|eot_id|>", "")
        print('get_proposal:최종 텍스트:')
        print(cleaned_text)
        return cleaned_text




