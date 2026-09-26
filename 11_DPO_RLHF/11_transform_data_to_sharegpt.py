from datasets import load_dataset

def convert_func(batch):
    conversation_list = batch["conversation"]

    message_list = []

    for conversation in conversation_list:
        user_msg = conversation[0]["human"]
        assistant_msg = conversation[0]["assistant"]

        message = [
            {"role": "user", "content": user_msg},
            {"role": "assistant", "content": assistant_msg}
        ]

        message_list.append(message)

    return {"messages": message_list}

dataset = load_dataset("json", data_files="./data/keywords_data_train.jsonl")

new_dataset = dataset.map(convert_func, batched=True, remove_columns=dataset["train"].column_names)

new_dataset["train"].to_json("./data/keywords_data_sharegpt.jsonl", force_ascii=False)