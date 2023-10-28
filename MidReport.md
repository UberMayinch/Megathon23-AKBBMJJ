We create a model that tests a potential employee in successive steps and classifies them as suitable for a Sales Job, a Technical Job or Not Suitable for Work mainly through the use of the Big 5 model of personality (OCEAN model).

Assumptions/Prerequisites: The company provides a corpus of applications and the positions into which the applicants were selected/rejected. 

We proceed in a 3 step workflow:
Step 1: Social Media Analysis
We ask the applicant for their social media handles. Assuming that the API's for the selected social media applications are available during operation, we use methods such as Semantic analysis, NRC Emotion Lexicon etc. to extract a vector representing personality predicted on the basis of social media usage. We additionally concatenate with the outputted vector another feature that represents the size of the scraped corpus.  

Step 2: Personality Questionnare
We use a likert scale-type test to quantify an applicant's personality along the OCEAN parameters. 

Step 3: Game Evaluation
As has been mentioned in several papers, employees are incentivised to give different answers on personality Questionnares or project different personalities on Social Media. Hence, we will make them play a specific game and monitor their gameplay closely to extract data from this. 
After this we will concatenate the vectors obtained in each step and run the classifier on the new vector for the final output. 
