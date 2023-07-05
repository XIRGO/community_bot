from pythorhead import Lemmy
from dotenv import dotenv_values

def check_pms():

    config = dotenv_values(".env")

    print(".env loaded")
    
    USERNAME = config["USERNAME"]
    PASSWORD = config["PASSWORD"] 
    INSTANCE = config["INSTANCE"]
    COMMUNITY = config["COMMUNITY"]
    SCORE = config["SCORE"]

    lemmy = Lemmy(INSTANCE)
    lemmy.log_in(USERNAME, PASSWORD)

    pm = lemmy.private_message.list(True,1)

    # check PMs

    unread_pm = lemmy.private_message.list(True,1)

    private_messages = unread_pm['private_messages']

    for pm in private_messages:
        pm_sender = pm['private_message']['creator_id']
        pm_username = pm['creator']['name']
        pm_context = pm['private_message']['content']
        pm_id = pm['private_message']['id']

        output = lemmy.user.get(pm_sender)
        user_score = output['person_view']['counts']['comment_score']

        print (pm_username + " (" + str(pm_sender) + ") sent " + pm_context + " - user score is " + str(user_score))

        if pm_context == "!help":
            lemmy.private_message.create("Hey, " + pm_username + ". These are the commands I currently know:" + "\n\n - `!help` - See this message. \n - `!score` - See your user score. \n - `!create` - Create a new community. Use @ to specify the name of the community you want to create, for example `!create @bot_community`. " + "\n \n I am a Bot. If you have any queries, please contact [Demigodrick](/u/demigodrick@lemmy.zip) or [Sami](/u/sami@lemmy.zip). Beep Boop.", pm_sender)
            lemmy.private_message.mark_as_read(pm_id, True)
            continue

        if pm_context == "!score":
            lemmy.private_message.create("Hey, " + pm_username + ". Your comment score is " + str(user_score) + "\n \n I am a Bot. If you have any queries, please contact [Demigodrick](/u/demigodrick@lemmy.zip) or [Sami](/u/sami@lemmy.zip). Beep Boop.", pm_sender)
            lemmy.private_message.mark_as_read(pm_id, True)
            continue

        if pm_context.split(" @")[0] == "!create":
            community_name = pm_context.split("@")[1]

            #check user score
            if user_score < int(SCORE):
                lemmy.private_message.create("Hey, " + pm_username + ". Your comment score is too low to create a community. Please interact with other communities first. You can check your score at any time by sending me a message with `!score` and I will let you know!"  "\n \n I am a Bot. If you have any queries, please contact [Demigodrick](/u/demigodrick@lemmy.zip) or [Sami](/u/sami@lemmy.zip). Beep Boop.", pm_sender)
                lemmy.private_message.mark_as_read(pm_id, True)           
                continue

            #check if it already exists
            check_community = lemmy.discover_community(community_name)

            if check_community is not None:
                lemmy.private_message.create("Hey, " + pm_username + ". Sorry, it looks like the community you are trying to create already exists. \n \n I am a Bot. If you have any queries, please contact [Demigodrick](/u/demigodrick@lemmy.zip) or [Sami](/u/sami@lemmy.zip). Beep Boop.", pm_sender)
                lemmy.private_message.mark_as_read(pm_id, True)
                continue

            #create community - add user and remove bot as mod
            lemmy.community.create(community_name,community_name)
            community_id = lemmy.discover_community(community_name)
            lemmy.community.add_mod_to_community(True,community_id,pm_sender)
            lemmy.community.add_mod_to_community(False,community_id,303747) #your bot id number

            lemmy.private_message.create("Hey, " + pm_username + ". Your new community, " + community_name + ", has been created. You can now set this community up to your liking." + "\n \n I am a Bot. If you have any queries, please contact [Demigodrick](/u/demigodrick@lemmy.zip) or [Sami](/u/sami@lemmy.zip). Beep Boop.", pm_sender)
            lemmy.private_message.mark_as_read(pm_id, True)


        else:
            lemmy.private_message.create("Hey, " + pm_username + ". Sorry, I did not understand your request. Please try again or use `!help` for a list of commands. \n \n I am a Bot. If you have any queries, please contact [Demigodrick](/u/demigodrick@lemmy.zip) or [Sami](/u/sami@lemmy.zip). Beep Boop.", pm_sender)
            lemmy.private_message.mark_as_read(pm_id, True)
            continue
