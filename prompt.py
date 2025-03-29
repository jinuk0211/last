llm_prompt = """Evaluate the given solution (not necessarily complete) based on the clarity, coherence, and correctness of the logical reasoning process. Assess whether the steps follow a structured, step-by-step approach, ensuring that intermediate steps are neither skipped nor incorrect. Consider whether assumptions are clearly stated, conclusions logically follow from premises, and the response adheres to formal rules in mathematical proofs or coding logic. 

Provide only decimal score between 0 and 1

Input: 
Problem:"""

image_description_score = '''Score how well the image description relates to the given problem. Higher accuracy of description should result in a higher score, which must be between 0 and 1.
Input:
Problem: '''

critic_simplified = '''Your task is to evaluate whether the given steps can successfully solve the provided problem and output a score. The score should be a decimal between 0 and 1. If all the steps are incorrect (every step is wrong), the score is 0. If all the steps are correct and the answer is calculated, the score is 1. The more incorrect steps there are, the closer the score is to 0. The closer the steps are to the final answer, the closer the score is to 1. Steps that only contain textual descriptions without calculation formulas should generally receive a low score. A score of 0.9 or higher must be given only if the specific numerical answer has been calculated (a complete thought process without calculating the answer or only listing the calculation formula must receive a score below 0.9). 

First, generate an analysis, then provide the score. Your analysis and scoring should be entirely based on the input steps provided. Do not generate additional steps.

Now, given a problem and the provided steps, provide the analysis and score. Note that the analysis should not include the next steps, and the scoring should be entirely based on the input steps and image description provided.
The output format is limited to: "Analysis:...\nScore:...", where ... represents the omitted output content, which you need to fill in.

Input:
Problem: '''

single_reflection_prompt_simple_en = '''
You are an expert in science. Given a science problem and some corresponding steps (not necessarily complete) to answer it, you need to determine whether the given steps have completely solved the problem.

You need to distinguish between two cases and give the corresponding output.
Case 1: If the given steps have already solved the problem and provided the final answer to the question, then you should output: "Problem solved" and nothing else.
Case 2: If the given steps have not yet calculated the answer to the question or have not finished reasoning, then please output: "Problem unsolved" with no other content.
Note that if the existing steps do not compute the answer or do not simplify the answer expression as required by the question, then it should be considered unsolved.
Here is the input, please follow the requested output instructions, you do not need to answer the question.

Problem: '''

single_proposal_prompt = '''
Your task is to provide the correct next step based on a given problem, image description and the existing solution steps (which may not be complete). Below are a few examples for you to learn from.

Assuming the input consists of n steps, the input format is:
"Problem:...
Image description: ...
Given steps:
Step 1:...
Step 2:...
...
Step n:..."
where ... represents the omitted input information.
If n equals 0, you need to start by briefly analyzing the problem-solving approach and then output the first step. If n is not equal to 0, you need to briefly analyze the problem-solving method based on the input steps and, following the logic and analysis of the existing steps, output what you believe to be the correct next step (Step n+1).
The output format is limited to:
"Analysis:...\nNext step:..."
where ... represents the omitted output information, which you should fill in.
Below is the input, please provide the output according to the specified format without including extra information or restating the problem.

Problem:'''

zero_single_proposal_prompt_en = '''
Your task is to give the correct next step, given probl em, image description and an existing partial solution (not a complete answer).
Assuming the input is n-steps, then the format of the input is:
"Problem: ...
Existing Steps:
Step 1: ...
Step 2: ...
...
Step n: ..."
where ... denotes omitted input information.
If no existing steps are provided, you need to briefly analyze the problem from scratch and then output the first step. Otherwise, you need to output the next step (step n+1) that you think is correct, following the ideas and analysis of the existing steps.
The output format is limited to:
"Next step: ..."
where ... indicates omitted output information, which is the part you should fill in. Your output should be a complete reasoning step that includes calculations, reasoning, choosing answers, etc.
Here is the input, please follow the restricted output format.

Problem: '''

zero_single_proposal_prompt_use_reflection_en = '''
Your task is to give the correct next step, given a science problem, an existing partial solution (not a complete answer) and some analysis for the next step.
Assuming the input is n-steps, then the format of the input is:
"Problem: ...
Existing Steps:
Step 1: ...
Step 2: ...
...
Step n: ...
Analysis: ..."

where ... denotes omitted input information.
If no existing steps are provided, you need to output the first step referring to the given analysis. Otherwise, you need to output the next step (step n+1) that you think is correct, following the ideas of the existing steps and provided analysis.
The output format is limited to:
"Next step: ..."
where ... indicates omitted output information, which is the part you should fill in. Your output should be a complete reasoning step that includes calculations, reasoning, choosing answers, etc.
Here is the input, please follow the restricted output format.

Problem: '''


single_reflection_prompt_en = '''
Given a science problem with existing answer steps (not necessarily complete answers), your task is to determine if the existing steps have solved the problem. If it has not been solved, give comments and brief ideas for next steps in response to the steps already in place.
Assuming that the steps already available are n steps, the input would be of the form:
"Problem: ...
Existing Steps:
Step 1: ...
Step 2: ...
...
Step n: ..."

where ... denotes omitted input information.
You need to distinguish between two cases and give the corresponding output.
Case 1: If these steps have already solved the problem and computed the final answer, then just output: "Problem solved" and nothing else.
Case 2: If the problem has not been completely solved, you need to analyze the existing steps, and point out the brief idea of the next step. If no existing steps are provided, then you need to briefly analyze the problem. The output format is limited to: "Analysis: ...", where ... indicates omitted output information, which is the part you should fill in.
Here is the input, please follow the requested output instructions, do not try to answer the whole question.

Problem: '''