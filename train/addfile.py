from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
INPUT_FILE = "train.jsonl"

client = OpenAI()

file = client.files.create(
  file=open(INPUT_FILE, "rb"),
  purpose="fine-tune"
)

# notez absolument l'id du fichier, il sera nécessaire pour le fine-tuning
print("File has been uploaded to OpenAI with id ", file.id)