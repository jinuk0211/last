# llm_prompt = """Evaluate the given solution (not necessarily complete) based on the clarity, coherence, and correctness of the logical reasoning process. Assess whether the steps follow a structured, step-by-step approach, ensuring that intermediate steps are neither skipped nor incorrect. Consider whether assumptions are clearly stated, conclusions logically follow from premises, and the response adheres to formal rules in mathematical proofs or coding logic. 

# Provide only decimal score between 0 and 10. The output format is limited to: "Score:..." where ... represents the omitted output content, which you need to fill in.

# Input: 
# Problem:"""

# image_description_score = '''Score how well the image description relates to the given problem and image. Higher accuracy of description should result in a higher score. The score should be a decimal between 0 and 10. The output format is limited to: "Score:...", where ... represents the omitted output content, which you need to fill in.
# Input:
# Problem: '''

# critic_simplified = '''Your task is to evaluate whether the given steps can successfully solve the provided problem and output a score. The score should be a decimal between 0 and 10. If all the steps are correct and the answer is calculated, the score is 10. The closer the steps are to the final answer, the closer the score is to 10. A score of 9 or higher must be given only if the specific numerical answer has been calculated.
# First, generate an analysis, then provide the score. Your analysis and scoring should be entirely based on the input steps provided. Do not generate additional steps.
# Now, given a problem, image, image description and the provided steps, provide the score and the scoring should be entirely based on the input steps and image description provided.
# The output format is limited to: "Score:...", where ... represents the omitted output content, which you need to fill in.

# Input:
# Problem: '''

# single_reflection_prompt_simple_en = '''
# You are an expert in math. Given a problem, image, image description and some corresponding steps (not necessarily complete) to answer it, you need to determine whether the given steps have completely solved the problem.

# You need to distinguish between two cases and give the corresponding output.
# Case 1: If the given steps have already solved the problem and provided the final answer to the question, then you should output: "Problem solved" and nothing else.
# Case 2: If the given steps have not yet calculated the answer to the question or have not finished reasoning, then please output: "Problem unsolved" with no other content.
# Note that if the existing steps do not compute the answer or do not simplify the answer expression as required by the question, then it should be considered unsolved.
# Here is the input, please follow the requested output instructions, you do not need to answer the question.

# Problem: '''


# GPT_PREFIX_PROMPT = """
# generate a step-by-step reasoning process to solve the problem. Ensure the steps are logical and concise.
# Finally, provide a concise summary of the final answer in the following format: 'The final answer is: xxx'. If the question is multiple-choice, provide the options along with their content. If it is free-form, directly present the final result. Do not provide any explanation.

# Format your response with the following sections, separated by ###:
# Image Description:
# Let's think step by step.
# Step 1:
# Step 2:
# ...
# ### The final answer is: 

# {question}

# Please complete the response based on the reasoning prefix without altering its content.

# Reasoning prefix: {reasoning_prefix}"""

# # zero_single_proposal_prompt_en = '''
# # Your task is to give the correct next step, given image, problem, image description and an existing partial solution (not a complete answer).
# # the format of the input is:
# # "Problem: ...
# # Image Description: ...
# # Step 1: ...
# # Step 2: ...
# # ...
# # Step n: ..."
# # where ... denotes omitted input information.
# # If no existing steps are provided, you need to output the first step. Otherwise, you need to output the next step (step n+1) that you think is correct, 
# # The output format is limited to:
# # "Next step: ..."
# # where ... indicates omitted output information, which is the part you should fill in. Your output should be a complete reasoning step that includes calculations, reasoning, choosing answers, etc.
# # Here is the input, please follow the restricted output format.

# # Problem: '''

# zero_single_proposal_prompt_en = '''
# generate a step-by-step reasoning process to solve the problem. Ensure the steps are logical and concise.the format of the input is:
# "Problem: 
# Image Description: 
# Let's think step by step.

# Step 1: 
# Step 2: 
# ...
# Step n: "

# {question}

# Please complete the response based on the reasoning prefix without altering its content.

# {reasoning_prefix}

llm_prompt = """Evaluate the given solution (not necessarily complete) based on the clarity, coherence, and correctness of the logical reasoning process. Assess whether the steps follow a structured, step-by-step approach, ensuring that intermediate steps are neither skipped nor incorrect. Consider whether assumptions are clearly stated, conclusions logically follow from premises, and the response adheres to formal rules in mathematical proofs or coding logic. 

Provide only decimal score between 0 and 10. The output format is limited to: "Score:..." where ... represents the omitted output content, which you need to fill in.

Input: 
Problem:"""

# image_description_score = '''Score how well the image description relates to the given problem and image. Higher accuracy of description should result in a higher score. The score should be a decimal between 0 and 10. The output format is limited to: "Score:...", where ... represents the omitted output content, which you need to fill in.
# Input:
# Problem: '''
image_description_score = '''Your task is to evaluate how well the image description describes the given image. The score should be a decimal between 0 and 10.  Higher accuracy of description should result in a higher score. 
Your scoring should be entirely based on the input image description and image provided. Do not generate additional Image Description or solution.
Now given image and image description,  Provide the score. 
The output format is limited to: "Score:...", where ... represents the omitted output content, which you need to fill in.
Input:
'''


critic_simplified = '''Your task is to evaluate whether the given steps can successfully solve the provided problem and output a score. The score should be a decimal between 0 and 10. If all the steps are correct and the answer is calculated, the score is 10. The closer the steps are to the final answer, the closer the score is to 10. A score of 9 or higher must be given only if the specific numerical answer has been calculated.
First, generate an analysis, then provide the score. Your analysis and scoring should be entirely based on the input steps provided. Do not generate additional steps.
Now, given a problem, image, image description and the provided steps, provide the score and the scoring should be entirely based on the input steps and image description provided.
The output format is limited to: "Score:...", where ... represents the omitted output content, which you need to fill in.

Input:
Problem: '''

single_reflection_prompt_simple_en = '''
You are an expert in math. Given a problem, image, image description and some corresponding steps (not necessarily complete) to answer it, you need to determine whether the given steps have completely solved the problem.

You need to distinguish between two cases and give the corresponding output.
Case 1: If the given steps have already solved the problem and provided the final answer to the question, then you should output: "Problem solved" and nothing else.
Case 2: If the given steps have not yet calculated the answer to the question or have not finished reasoning, then please output: "Problem unsolved" with no other content.
Note that if the existing steps do not compute the answer or do not simplify the answer expression as required by the question, then it should be considered unsolved.
Here is the input, please follow the requested output instructions, you do not need to answer the question.

Problem: '''


# image_description_prompt = '''
# your task is to provide the image description based on a given image and problem, the output format is limited to "Image Description:..." where ... represents the output result, which you should fill in.
# Here is the input, please follow the restricted output format.
# Given problem:
# '''
image_description_prompt = '''generate image description based on given image. the otput format is limited to "Image Description:..." where ... represents the output result, which you should fill in.'''

zero_single_proposal_prompt_en = '''
Your task is to give the correct next step, given image, problem, image description and an existing partial solution (not a complete answer).
the format of the input is:
"Problem: ...
Image Description: ...
Step 1: ...
Step 2: ...
...
Step n: ..."
where ... denotes omitted input information.
If no informations are provided, you need to output the first step. Otherwise, you need to output the next step (step n+1) that you think is correct, 
The output format is limited to:
"Next step: ..."
where ... indicates the part you should fill in. Your output should be a complete reasoning step
Here is the input, please follow the restricted output format.

Problem: '''

