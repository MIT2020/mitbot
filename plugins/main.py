import time
import requests
import json
from random import randint, choice
import goslate

crontable = []
outputs = []

# How to add the things and the stuff:
# Add some code in the process_message function
# Use the "txt" variable to access the text from a message
# To submit a response, call say(data, "your message")
# (have to pass the data variable so it knows which channel to post it to)


def choose(letter, size):
	with open("data/mit/" + letter + ".txt", "r") as f:
		choice = randint(0, size)
		for a, line in enumerate(f):
			if a == choice:
				return(line[:-2])
				
def say(data, msg):
	outputs.append([data['channel'], msg])
	
def shorten(link):
	print("Shortening: " + link)
	api = 'https://www.googleapis.com/urlshortener/v1/url'
	payload = {'longUrl': link}
	headers = {'content-type': 'application/json'}
	r = requests.post(api, headers=headers, params={"key" : "AIzaSyBOCnpz-Vc8wv5cAb0upfNwgixrRHBQEgU"}, data=json.dumps(payload))
	print("Reponse: " + str(r.json()))
	return str(r.json()['id'])
	
def fortune():
	verb = ['eat', 'destroy', 'stomp on', 'pulvarize', 'swallow', 'transmute', 'take naps with', 'be married to', 'attend CPW with']
	adj = ['slimy', 'repulsive', 'yummy', 'blue', 'mildly interesting', 'mediocre', 'oddly charming']
	noun = ['rocks', 'underground tunnels', 'guinea pigs', 'skype clients', 'C++ compilers', 'candy', 'speakers', 'unidentified creatures']
	prep = ["inside your dad's", 'next to your favorite', 'beside a', 'underneath a', 'within a']
	loc = ['restaurant', 'car', 'factory', 'dirt hole', 'cage', 'very large sandwich', 'dank meme']

	return ('In the year {0}, you will {1} {2} {3} {4} {5}'.format(
		randint(2016, 2099), choice(verb), choice(adj), choice(noun), choice(prep), choice(loc)))
	
def process_message(data):
	txt = str(data['text']).lower()
	print("Incoming message: " + txt)
	
	if 'tell a joke' in txt:
		r = requests.get("http://tambal.azurewebsites.net/joke/random")
		say(data, r.json()['joke'])
	elif 'what' in txt and ("probability" in txt or "chances" in txt):
		say(data, "My sources indicate a " + str(randint(0,100)) + "% probability")
	elif any([(txt.startswith(a)) for a in ('where is', 'who is', 'what is', 'what are', 'what do', 'why')]) and (not any([(a in txt) for a in ('this', 'my', 'their', 'you', 'his', 'her', 'our')])) and '?' in txt:
		#actually sending a request here is pretty useless right now
		r = requests.get("http://google.com/search", params={"q" : txt})
		say(data, "Let me Google that for you: " + shorten(r.url))
	elif txt.startswith("shorten "):
		say(data, shorten(txt.split("<")[1].split(">")[0]))
	elif txt.startswith("echo"):
		say(data, txt.split('echo')[1])
	elif 'ayy lmao' in txt:
		say(data, 'http://put.nu/files/' + choice(('5785U2A.jpg', 'dBSU_J7.gif', 'mW-rnI2.jpg', 'n5rD3GS.jpg', 'DURylFZ.jpg', '5AR4xo8.jpg', 'wnCTLWV.png', 'UD-FMiC.jpg', 'zr-PLxK.jpg')))
	elif any([txt.startswith(q) for q in ('is', 'are', 'should', 'can', 'does', 'do', 'will', 'has', 'have', 'am')]) and '?' in txt:
		say(data, choice(('No way.', 'Definitely not.', 'Without a doubt.', 'My sources indicate yes.', 'I have no idea.', 'Idk, ask Chris Peterson', 'What a stupid question. Obviously not.', 'Yes!', 'NOPE.', 'Yeah, I think so.')))
	elif "my fortune" in txt:
		say(data, fortune())
	elif "has joined the channel" in txt:
		say(data, "Welcome " + txt.split('|')[1].split('>')[0] + "! Here is a one-of-a-kind image we thought you might like. It's based on your personality as interpreted by an algorithm we have been developing over the last few months specifically for this. http://goo.gl/1fkHTt#" + str(randint(1,999999)))
	elif "random image" in txt:
		say(data, "Here: http://bit.do/bQdnb#" + str(randint(1,999999)))
	elif "nonsensify" in txt:
		meme = txt.split('nonsensify')[1]
		key = 'trnsl.1.1.20160318T202525Z.9433c9941967fc80.a36f7812f8621025e8f7235672a00d5913814a06'
		api = 'https://translate.yandex.net/api/v1.5/tr.json/translate'

		for lang in ('en-ja','ja-ru', 'ru-zh', 'zh-en'):
			info = {'text': meme, 'lang': lang, 'format': 'plain', 'key':key}
			r = requests.post(api, params=info).json()
			meme = r['text'][0]
			
		say(data, meme)
	elif txt.startswith("cpw:"):
		result = ""
		search = txt.split("cpw:")[1]
		with open("data/cpw.txt", "r") as f:
			for line in f:
				if search.strip() in line.lower().split(':')[-1]:
					result += line + "\n"
		say(data, result if result else "Nothing found")
	elif txt.startswith("cpw at "):
		result = ""
		date,time = txt.split(" ")[2:4]
		with open("data/cpw.txt", "r") as f:
			for line in f:
				date_l = int(line[3:5])
				time_s = int(line.split(":")[1].strip())
				time_e = int(line.split(":")[2][-2:])
				print(date)
				print(time)
				print(date_l)
				print(time_s)
				print(time_e)
				if time_s <= int(time) and time_e >= int(time) and int(date) == date_l:
					result += line + "\n"
		say(data, result if result else "Nothing found")
	elif (' mit ' in txt) or txt.startswith('mit ') or txt.endswith(' mit') or txt == 'mit':
		#could probably do something with regex to get rid of those stupid conditions
		say(data, choose('m', 900) + ' ' + choose('i', 2851) + ' of ' + choose('t', 3575))
	elif "dootdoot" in txt:
		say(data, """```
     _.--""--._        
   ."          ".     
  | .   `      ` |    
  \(            )/   
   \)__.    _._(/  
   //   >..<   \\  
   |__.' vv '.__/ 
      l'''"''l    
      \_    _/  
 _      )--(     _  
| '--.__)--(_.--' |  
 \ |`----''----'| / 
  ||  `-'  '--' || 
  || `--'  '--' || 
  |l `--'--'--' |l  
 |__|`--'  `--'|__| 
 |  |    )-(   |  | 
  ||     )-(    \|| 
  || __  )_(  __ \\  
  ||'  `-   -'  \ \\ 
  ||\_   `-'   _/ |_\ 
 /_\ _)J-._.-L(   /`-\ 
|`- I_)O /\ O( `--l\\\| 
||||( `-'  `-') .-' ||| 
 \\\ \       / /   /// 
    \ \     / / 
     \ \   / / 
     /  \ /  \ 
     |_()I()._| 
     \   /\   / 
      | /  \ | 
      | |   \ \ 
      | |    \ \ 
      | |     \ \ 
      | |-     \ \_ 
      | |      /-._\ 
     |.-.\    //.-._) 
      \\\\   /// 
       \\\\-''' ```
""")
		
