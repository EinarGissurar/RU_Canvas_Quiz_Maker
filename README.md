# Canvas Quiz Maker For Reykjavik University

Canvas Quiz reader is indented to be used for courses in University or Reykjavik, although it can be modified for use in other institutions

## Initial Configuration

In Config folder, edit the config.csv file accordingly:

- Under "user\_access\_token," insert your Canvas Access Token
  - [How do I get an Access token?](https://community.canvaslms.com/docs/DOC-10806-how-do-i-manage-api-access-tokens-as-an-admin)
- Under "course\_id" input the numeric ID of your course.
  - This can be found in the course url: https://reykjavik.instructure.com/courses/**Course\_ID**

## Setup

**First things first.** 
If you are fetching this configuration from the Google Drive make sure to download the folder to your own local directory, before editing any of the sample files.

Additionally, if you intend on working with the google/excel sheets to set up the quiz/questions, make sure you finsih by exporting the Data sheets as CSV.

---

Quiz Maker requires two files to work. Quiz-Data.csv and Questions-Data.csv

Sample Files are provided that you can run to see examples of different types of questions. We recommend keeping a copy of it someplace for an easy reference.

It is recommended that you use the Google sheets document to set up the quiz and questsions sheet and then download the data sheet as a CSV file.

Under Templates folder are empty template files that you can edit accordingly:

#### Quiz-Data.csv:
- title
  - A descriptive name for quiz
- description
  - Description for quiz
- quiz\_type
  - Use to control the type of quiz. Available types are:
    - practice\_quiz
      - The Standard Ungraded Quiz of multiple questions
    - assignment
      - The Standard Graded Quiz of multiple questions
    - graded\_survey
      - Intended for surveys, where students get graded for answering few questions.
    - survey
      - The Ungraded version of surveys.
- quiz\_group\_name
  - Name of question group (not to be fonfused with question bank)
- quiz\_group\_pick_count
  - Number of questions you want to pull from the question bank
- quiz\_group\_question\_points
  - How many points students get for each correct question
    - Note, Canvas limits you to use this instead of the points selected for each individual questions. Keep this in mind if you intend on creating quizes with questions that have different points
- assignment\_group\_id
  - Leave blank (**TODO:** Look into possible usage)
- time\_limit
  - Can be used to implement a time limit on exam. Value given is in minutes (60 for a hour, etc)
  - Leave blank for no time limit
- shuffle\_answers
  - True/False value
  - Randomize order of multiple answer/choice options
- hide_results
  - Used to hide results from student. Available options:
    - always - Always hidden
    - until\_after\_last\_attempt - Used for quizes that can be attempted multiple times. Hides results until student submits quiz for the final time.
  - Leave blank to allows show result.
- show\_correct\_answers
  - True/False value
  - Shows correct answers when student hands in quiz
  - Only applies if results are visible
- show\_correct\_answers\_at
  - Requires ISO 8601 format (YYYY-MM-DD)
  - Shows answers after given date. Leave blank to allow students to see as soon as they hand in
  - Only applies is answers are made visible
- hide\_correct\_answers\_at
  - Requires ISO 8601 format (YYYY-MM-DD)
  - Hides answers after given date. Leave blank to allow students to always see the answers
  - Only applies is answers are made visible
- allowed\_attempts
  - Number of times students are allowed to take test
  - Defaults to 1 time, if left blank
- scoring\_policy
  - If multiple attempts are allowed, controls what grade is picked. Available options:
    - keep_highest
      - Keep the best attempt
    - keep_latest
      - Keep the last attempt
  - Defaults to "keep_highest" if left blank
- one\_question\_at\_a\_time
  - True/False value
  - If left True, only one question is made visible at a time. False will show all questions at once
  - Defaults to False, if left blank
- cant\_go\_back
  - True/False value
    - if True, students will be unable to hit the back button and revisit previous questions
  - Defaults to False, if left blank
- access\_code
  - Set a password that's required to access quiz
  - Leave blank for no password
- ip\_filter
  - Resticts access to quiz from within certain IP range. Could be used to restict usage within school WIFI
  - Leave blank for no filter
  - **TODO:** Check with IT department about possible usage. And update the guide accordingly
- due\_at
  - Requires ISO 8601 format (YYYY-MM-DD)
  - Determines when quiz is due (students flagged as handing in late if handing in past this point) 
- lock\_at
  - Requires ISO 8601 format (YYYY-MM-DD)
  - Determines when quiz is no longer available 
- unlock\_at
  - Requires ISO 8601 format (YYYY-MM-DD)
  - Determines when quiz becomes available
- published
  - True/False value
  - Unpublished quizes are hidden from student view.
- one\_time\_results
  - True/False value
  - If set to True and results are not hidden, students will only be able to see the results once, after handing it in.
- only\_visible\_to\_overrides
  - Leave blank (**TODO:** Look into possible usage)

#### question\_data.csv:
- question\_name
  - Short title
- question\_text
  - The main content for question
- question\_type
  - Lists possible type of questions, which detemins the expected answer. Available types are:
    - multiple\_answers\_question
      - Student can check multiple correct answers
      - Graded automatically
    - multiple\_choice\_question 
      - Student can only check one correct answer 
      - Graded automatically
    - true\_false\_question
      - Students pick between a true or false value
      - Graded automatically
    - short\_answer\_question 
      - Intended for one word "fill-in-the-blank" questions
      - Graded automatically
    - essay\_question 
      - Intended for longer written answers
      - Requires manual grading
    - file\_upload\_question 
      - Intended for file uploads 
      - Requires manual grading.
- answer\_option\_1 (mandatory)
  - Acceptable answer (case sensitive)
- option\_1\_comment
  - A comment that is given if students pick this question
- option\_1\_weight
  - Percentile weight for picking this answer 
  - 100 is full marks, 50 for half, etc
- answer\_option\_n (optional)
  - Alternative acceptable answers. These can be as many as you want. 
    - Note that you must also fill in option\_n\_comment and option\_n\_weight for each optional answer that you add.
	
**Note:** You can make as many questions as you want and each question does no require to have the same number of available answers. See sample file for example.

## Usage
Run quiz reader, once the above files have been correctly set up with the following arguments:
```
python quiz_maker.py you-quiz-data.csv your-question-data.csv
```
Program will output the return values from the API and inform you when it is done. A link should be provided that takes you directly to the course question banks, where you are asked to move your newly generated questions into a question bank of your choosing.

## Bugs and manual work
Currently, it is impossible to use the API to automatically assign questions to a question bank. Instead the questions are automatically placed into a default bank called " Unfiled questions."

Running the Quiz reader multiple times will cause all generated questions to go into that same default bank. Thus, should the user desire to generated multiple banks, it is highly recommended that they manually move the newly generated questions into a new bank after every run. 

Should a field be incorrectly filled, the program should output an error message explaining what's wrong (some error handling generated by API). Should you choose to run the script again, possibly after fixing incorrect values, make sure to delete the partially generated quiz/questions first. Otherwise, multiple copies will be created.

##### TODO 
Decide whether or not to halt run if errors are detected and possibly delete incorrectly/partially generated quiz and questions.

##Contributors

Author: Einar Örn Gissurarson (einarog05@ru.is)

Supervised: Jacky Mallett, Ph.D. Assistant Professor


##License and Attribution

Canvas Quiz Maker was developed by Einar Örn Gissurarson.

The owners (licensors) grant public use of this software under the following terms:

- Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License
- "AS IS" Disclaimer

This software is provided free for non-commercial course purposes under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0):

https://creativecommons.org/licenses/by-nc-sa/4.0/

In short, under this license you are free to: Share - copy and redistribute the material in any medium or format

Under the following conditions: Attribution - You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use. NonCommercial - You may not use the material for commercial purposes. ShareAlike - If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.

—— “AS IS” Disclaimer ——

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
