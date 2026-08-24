from dotenv import load_dotenv
from openai import OpenAI
import file_utils

load_dotenv()

client = OpenAI()

model_name = "gpt-5.5"
second_model_name = "gpt-5.6-luna"
response_heading = "\n--- Model answer ---"


def get_ai_response(prompt, model=model_name):
    response = client.responses.create(
        model=model,
        input=prompt
    )

    return response.output_text

def get_user_prompt():
    raw_prompt = input("What would you like to ask the AI?\n")
    return raw_prompt.strip()



def validate_prompt(prompt):
    prompt_length = len(prompt)

    if prompt == "":
        return "empty"
    
    if prompt_length < 10:
        return "too short"
    
    if prompt_length > 500:
        return "too long"
    
    return "valid"


def create_interaction_record(prompt, answer):
    prompt_length = (len(prompt))
    return {
        "prompt": prompt,
        "answer": answer,
        "prompt_length": prompt_length
    }



def print_session_summary(records):
    print("\n--- Session Summary ---")
    print("Total interactions:", len(records))

    total_prompt_length = 0

    for record in records:
        total_prompt_length += record["prompt_length"]
        print("-", record["prompt"], "-", record["prompt_length"], "characters")

    print("Total prompt characters:", total_prompt_length)



def save_interaction_history(interaction_records, filename):
        existing_records = file_utils.load_results(filename)
        existing_records.extend(interaction_records)
        file_utils.save_results(existing_records, filename)



def main():
    interaction_records = []


    app_is_running = True


    while app_is_running:

        user_prompt = get_user_prompt()

        prompt_status = validate_prompt(user_prompt)



        if prompt_status == "empty":
            print("You did not enter a prompt. Please type a question.")
            continue

        elif prompt_status == "too short":
            print("Your prompt is too short. Please enter a more detailed question")
            continue

        elif prompt_status == "too long":
            print("Your prompt is too long. Please shorten it and try again.")
            continue

        
            
        answer = get_ai_response(

                
            prompt = user_prompt
        )



        interaction_record = create_interaction_record(
            user_prompt,
            answer
        )

        interaction_records.append(interaction_record)

        print(response_heading)
        print(answer)

        print("Interactions recorded:", len(interaction_records))


        while True:
            user_choice = input("\nDo you want to ask another question? yes/no\n").strip().lower()
            if user_choice == "no":
                app_is_running = False
                break
            elif user_choice == "yes":
                print('Continuing...')
                break
            else: 
                print("Please enter only yes or no")



    print_session_summary(interaction_records)




    save_interaction_history(
    interaction_records,
    "interaction_records.json"
)


if __name__ == "__main__":
    main()




    













