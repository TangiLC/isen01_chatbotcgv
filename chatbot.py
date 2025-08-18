from openai import OpenAI
import mysql.connector as mysql
from datetime import datetime
from dotenv import load_dotenv
import os


load_dotenv()
BDD_USER = os.getenv("BDD_USER")
BDD_PASSWORD = os.getenv("BDD_PASSWORD")
client = OpenAI()


################### Saisie du prompt par l'utilisateur ########################
def saisie_utilisateur():
    pr=input("Comment puis-je vous aider ?")
    return pr

################### création d'une conversation dans la BDD ##########

def create_conversation():
  
    try:
        bdd = mysql.connect(
            host='localhost',
            user=BDD_USER,
            password=BDD_PASSWORD,
            database='Logs',
            port=3306
        )
        cursor = bdd.cursor()

        insert_query = "INSERT INTO conversations () VALUES ()"
        cursor.execute(insert_query)
        bdd.commit()

        conversation_id = cursor.lastrowid

        cursor.close()
        bdd.close()
        return conversation_id

    except Exception as err:
        print("Erreur lors de l'accès à la base de données :", err)
        return None


################### Envoi du prompt au chatbot ################################
def envoi_au_chatbot(prompt):
    conv_id = create_conversation()
    response = None
    statut = 2  # fail
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        response = client.responses.create(
            model="ft:gpt-4.1-nano-2025-04-14:jn-formation::Bqy2C4rj",
            instructions="Réponses au ton professionnel liées aux CGV fine-tunées. En cas d'absence de réponse renvoyer 'Je ne peux pas répondre à votre requête dans le cadre des CGV'",
            input=prompt
        )
        statut = 1  # success
        affiche_message(f"{conv_id}_{now}:{response.output[0].content[0].text}")
    except Exception as e:
        affiche_message(f"Erreur lors de l'envoi au chatbot : {e}")
    
    finally:
        stockage_log(conv_id, now, prompt, response.output[0].content[0].text, statut)

       

################### Affichage d'un message dans le terminal ###################       
def affiche_message(mssg):
  print(f"%>{mssg}")
  
################### Stockage d'une nouvelle entrée dans les logs ##############
def stockage_log(conv_id,now, prompt, response, statut):
    try:
        bdd = mysql.connect(
            host='localhost',
             user=BDD_USER,
            password=BDD_PASSWORD,
            database='Logs',
            port=3306
        )
        cursor = bdd.cursor()

        insert_query = """
            INSERT INTO echanges (conversation, date, prompt, response, statut)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, (
            conv_id,
            now,
            prompt,
            response,
            statut
        ))

        bdd.commit()
        cursor.close()
        bdd.close()

    except Exception as err:
        print("Erreur lors de l'enregistrement du log :", err)

################### Proposition d'une nouvelle question #######################
def nouvelle_question():
  new = input("Souhaitez-vous poser une autre question (O/N) ? ")
  if new.lower() == "o":
    return True
  else:
    return False
  
################### MAIN ######################################################
def main():
  new_try=True
  while new_try:
    prompt=saisie_utilisateur()
    
    envoi_au_chatbot(prompt)
        
    new_try = nouvelle_question()
      

################### Lancement de Main #########################################
if __name__ == "__main__":
    main()  
  