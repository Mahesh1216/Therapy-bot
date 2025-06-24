from datasets import load_dataset

# Download and save nbertagnolli/counsel-chat (train split)
print("Downloading nbertagnolli/counsel-chat ...")
ds1 = load_dataset("nbertagnolli/counsel-chat", split="train")
ds1.save_to_disk("local_counsel_chat")
print("Saved to local_counsel_chat")

# Download and save Amod/mental_health_counseling_conversations (train split)
print("Downloading Amod/mental_health_counseling_conversations ...")
ds2 = load_dataset("Amod/mental_health_counseling_conversations", split="train")
ds2.save_to_disk("local_mental_health_counseling")
print("Saved to local_mental_health_counseling")

# Download and save EmoCareAI/Psych8k (private/gated, train split)
print("Downloading EmoCareAI/Psych8k ...")
ds3 = load_dataset("EmoCareAI/Psych8k", split="train")
ds3.save_to_disk("local_psych8k")
print("Saved to local_psych8k")

