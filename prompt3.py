

llm_prompt = """Evaluate the given solution (not necessarily complete) based on the clarity, coherence, and correctness of the logical reasoning process. Assess whether the steps follow a structured, step-by-step approach, ensuring that intermediate steps are neither skipped nor incorrect. Consider whether assumptions are clearly stated, conclusions logically follow from premises, and the response adheres to formal rules in mathematical proofs or coding logic. 

Provide only decimal score between 0 and 10. The output format is limited to: "Score:..." where ... represents the omitted output content, which you need to fill in.
Here is the input you should score.
Input: 
Problem:"""

# image_description_score = '''Score how well the image description relates to the given problem and image. Higher accuracy of description should result in a higher score. The score should be a decimal between 0 and 10. The output format is limited to: "Score:...", where ... represents the omitted output content, which you need to fill in.
# Input:
# Problem: '''
# image_description_score = '''Your task is to evaluate how well the image description describes the given image. The score should be a decimal between 0 and 10.  Higher accuracy of description should result in a higher score. 
# Your scoring should be entirely based on the input image description and image provided. Do not generate additional Image Description or solution.
# Now given image and image description,  Provide the score. 
# The output format is limited to: "Score:...", where ... represents the omitted output content, which you need to fill in.
# Input:
# '''
image_description_score = '''Your task is to evaluate how well the image description describes the given image. The score should be a decimal between 0 and 10.  Higher accuracy of description should result in a higher score. 
Your scoring should be entirely based on the input image description and image provided. Do not generate additional Image Description or solution.
The output format is limited to: "Score:...", where ... represents the omitted output content, which you need to fill in.
Here is the image description, Only generate the score and follow the restricted format. Do not generate additional explanation.
Input:
'''

critic_simplified = '''Your task is to evaluate whether the given steps can solve the provided problem and output a score. The score should be a decimal between 0 and 10. If all the steps are correct and the answer is calculated, the score is 10. The closer the steps are to the final answer, the closer the score is to 10.
Now, given a problem, image, image description and the provided steps, provide only the score and the scoring should be entirely based on the input image, image description,reasoning steps provided.
The output format is limited to: "Score:...", where ... represents the omitted output content, which you need to fill in.

Input:
Problem: '''

single_reflection_prompt_simple_en = '''
You are an expert in math. Given a problem, image, image description and reasoning steps (not necessarily complete) to answer it, you need to determine whether the given steps have completely solved the problem.
If the given steps have provided the final answer to the question, then you should generate "Problem solved" and nothing else.
If the given steps have not yet calculated the answer to the question or have not finished reasoning, then please generate "Problem unsolved" with no other content.
Note that if the existing steps do not simplify the answer expression as required by the question, then it should be considered unsolved.
Here is the input, please generate either "Problem solved" or "Problem unsolved".

Problem: '''


# image_description_prompt = '''
# your task is to provide the image description based on a given image and problem, the output format is limited to "Image Description:..." where ... represents the output result, which you should fill in.
# Here is the input, please follow the restricted output format.
# Given problem:
# '''

image_description_prompt = '''generate image description based on given image.'''

zero_single_proposal_prompt_en = '''
Your task is to give the correct next step, given image, problem, image description and an existing partial solution (not a complete answer).
The output format is limited to:
"Next step: ..."
where ... indicates the part you should fill in. Your output should be a one complete reasoning step
Here is the input, please follow the restricted output format. 

Problem: '''

