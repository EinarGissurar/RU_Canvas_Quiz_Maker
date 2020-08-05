# Version 1.2
# Author: Einar Örn Gissurarson (einarog05@ru.is)

#Used in conjunction with config.txt, quiz_data.csv, and question_data.csv. Do not run without these files.
#Usage: python quiz_maker.py quiz_data.csv question_data.csv

#!/usr/bin/python
import sys, os.path, csv, json, requests, itertools, collections

def main():
	if len(sys.argv) != 3:
		sys.exit('Usage: python quiz_maker.py you_quiz_data.csv your_question_data.csv')
	else:
		quiz_datafile = sys.argv[1]
		question_datafile = sys.argv[2]

	if os.path.isfile('./Config/config.csv') and os.path.isfile(quiz_datafile) and os.path.isfile(question_datafile):
		print('Files present, attempting validation')

		#Fetch Config Data
		with open('./Config/config.csv' , newline='', encoding='utf-8-sig') as csvconfig:
			try:
				config_reader = csv.DictReader(csvconfig, delimiter=',')
				config_CSV_data = next(config_reader)
				if config_CSV_data["User_Access_token"] == 'put access token here':
					sys.exit('Access token missing. Please see readme on how to aquire a token and edit config.csv accordingly.')
				if config_CSV_data["Course_ID"] == 'put course id here':
					sys.exit('Course ID missing. Please see readme on how to aquire a token and edit config.csv accordingly.')
			except IOError:
				sys.exit('Config file read error')
		
		headers = {'Authorization' : 'Bearer '+config_CSV_data["User_Access_token"]}
		url = 'https://reykjavik.instructure.com//api/v1/courses/'+config_CSV_data["Course_ID"]+'/quizzes'

		#Fetch Quiz Data
		with open(quiz_datafile , newline='', encoding='utf-8-sig') as csvquiz:
			try:
				quiz_reader = csv.DictReader(csvquiz, delimiter=',')
				quiz_CSV_data = next(quiz_reader)
			except IOError:
				sys.exit('Quiz_data read error')		
	else:
		sys.exit('Please ensure the following files exist: config.txt, quiz_data.csv, question_data.csv')

	quiz_data = {
		'quiz[title]' : quiz_CSV_data["title"],
		'quiz[description]' : quiz_CSV_data["description"],
		'quiz[quiz_type]' : quiz_CSV_data["quiz_type"],
		'quiz[assignment_group_id]' : quiz_CSV_data["assignment_group_id"],
		'quiz[time_limit]' : quiz_CSV_data["time_limit"],
		'quiz[shuffle_answers]' : quiz_CSV_data["shuffle_answers"],
		'quiz[hide_results]' : quiz_CSV_data["hide_results"],
		'quiz[show_correct_answers]' : quiz_CSV_data["show_correct_answers"],
		'quiz[show_correct_answers_last_attempt]' : quiz_CSV_data["show_correct_answers_last_attempt"],
		'quiz[show_correct_answers_at]' : quiz_CSV_data["show_correct_answers_at"],
		'quiz[hide_correct_answers_at]' : quiz_CSV_data["hide_correct_answers_a"],
		'quiz[one_time_results]' : quiz_CSV_data["one_time_results"],
		'quiz[allowed_attempts]' : quiz_CSV_data["allowed_attempts"],
		'quiz[scoring_policy]' : quiz_CSV_data["scoring_policy"],
		'quiz[one_question_at_a_time]' : quiz_CSV_data["one_question_at_a_time"],
		'quiz[cant_go_back]' : quiz_CSV_data["cant_go_back"],
		'quiz[access_code]' : quiz_CSV_data["access_code"],
		'quiz[ip_filter]' : quiz_CSV_data["ip_filter"],
		'quiz[due_at]' : quiz_CSV_data["due_at"],
		'quiz[lock_at]' : quiz_CSV_data["lock_at"],
		'quiz[unlock_at]' : quiz_CSV_data["unlock_at"],
		'quiz[published]' : quiz_CSV_data["published"],
		'quiz[only_visible_to_overrides]' : quiz_CSV_data["only_visible_to_overrides"]
	}

	r = requests.post(url, headers = headers, params = quiz_data)

	if r.status_code == 200 :
		print('Quiz created - Output:')
		y = r.json()
		print(y)
	else:
		sys.exit('Quiz creation failed with following output:\n'+str(r.status_code)+'\n'+r.text)
	print('\n===========================================\n')

	quiz_id = y['id']
	group_data = {
		'quiz_groups[][name]' : quiz_CSV_data["quiz_group_name"],
		'quiz_groups[][pick_count]' : quiz_CSV_data["quiz_group_pick_count"],
		'quiz_groups[][question_points]' : quiz_CSV_data["quiz_group_question_points"]
	}

	r = requests.post(url+'/'+str(quiz_id)+'/groups', headers = headers, params = group_data)

	if r.status_code == 201 :
		print('Quiz group created - Output:')
		y = r.json()
		group_id = y['quiz_groups'][0]['id']
		print(y)
	else:
		sys.exit('Quiz group creation failed with following output:\n'+str(r.status_code)+'\n'+r.text)
	print('\n===========================================\n')
	
	#Fetch Question Data
	with open(question_datafile , newline='', encoding='utf-8-sig') as csvquestions:
		try:
			#Column reader used to determine maximum number of viable answers.	
			column_reader, row_reader = itertools.tee(csv.reader(csvquestions, delimiter=','))
			columns = len(next(column_reader))
			del column_reader
		except IOError:
			sys.exit('Question_data read error')

		#question_pos used to give questions a valid position in list.
		question_pos = 0
			
		#Ignore headers
		next(row_reader)
		for row in row_reader:
			question_data = collections.defaultdict(list)

			question_data['question[question_name]'].append(row[0])
			question_data['question[question_text]'].append(row[1])
			question_data['question[quiz_group_id]'].append(group_id)
			question_data['question[question_type]'].append(row[2])
			question_data['question[position]'].append(question_pos)
			question_data['question[points_possible]'].append(row[3])

			#answer_pos used to give answers a valid position for each question.
			answer_pos = 0

			#Populate each question with valid answers. 
			#If valid answers are fewer than maximum number of answers, columns should be blank and thus ignored.
			iterator = range(4, columns, 3)
			for n in iterator:
				if row[n] is not '':
					question_data['question[answers]['+str(answer_pos)+'][text]'].append(row[n])
					question_data['question[answers]['+str(answer_pos)+'][comments]'].append(row[n+1])
					question_data['question[answers]['+str(answer_pos)+'][comments_html]'].append('<p>'+row[n+1]+'</p>')
					question_data['question[answers]['+str(answer_pos)+'][weight]'].append(row[n+2])

					answer_pos += 1
			question_pos += 1

			#Post each question into canvas. Then delete data, so it can be repopulated.
			r = requests.post(url+'/'+str(quiz_id)+'/questions', headers = headers, params = question_data)
			if r.status_code == 200 :
				print('Question #'+str(question_pos)+' created - Output:')
				print(r.json())
			else:		
				print('Failed to create Question #'+str(question_pos)+' - Output')
				print(r.status_code)
				print(r.text)
			print('\n===========================================\n')
			del question_data

	print('Done. Go to https://reykjavik.instructure.com/courses/'+config_CSV_data["Course_ID"]+'/question_banks where you can assign your questions to a question bank.')


if __name__ == "__main__":
    main()
		
