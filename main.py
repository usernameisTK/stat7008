from nltk.chat.util import Chat, reflections
from function1 import keywords
from function2 import get_topic_by_filename
from pairs import pairs


def list_pdf_files(folder_path):
    import os
    return [f for f in os.listdir(folder_path) if f.lower().endswith('.txt')]

def chat():
    print("Hi! I am a chatbot for your service")
    print("Please select an option:")
    print("1. Start a daily conversation")
    print("2. List and choose a PDF file")
    print("3. Exit")

    while True:
        try:
            choice = int(input("Chatbot: Your choice (1/2/3): "))
            if choice == 1:
                print("Chatbot: Starting the conversation...")
                chatbot = Chat(pairs, reflections)
                while True:
                    user_input = input("You: ")
                    if user_input.lower() in ["exit", "quit"]:
                        print("Chatbot: Goodbye!")
                        return
                    response = chatbot.respond(user_input)
                    if user_input.lower() == "back":
                        print("Chatbot: Returning to the main menu...")
                        break
                    if response:
                        print(f"Chatbot: {response}")
                    else:
                        print("Chatbot: I don't understand that. Can you rephrase?")
            elif choice == 2:
                folder_path = "extracted_text"
                pdf_files = list_pdf_files(folder_path)
                if pdf_files:
                    print("Chatbot: Here are the PDF files:")
                    for idx, file in enumerate(pdf_files, start=1):
                        print(f"{idx}. {file}")
                    try:
                        pdf_choice = int(input("Chatbot: Select a PDF by number: "))
                        if 1 <= pdf_choice <= len(pdf_files):
                            selected_pdf = pdf_files[pdf_choice - 1]
                            print(f"Chatbot: You selected '{selected_pdf}'.")
                            print("Chatbot: What do you want to do with this PDF?")
                            print("※ 1. Find keywords of ESG report")
                            print("※ 2. Topic classifications")
                            print("※ 3. Sentiment analysis")
                            print("※ 4. Data mining and/or text analysis methods")
                            print("※ 5. Prediction model")
                            print("※ 6. Summarization")
                            print("※ 7. Back to the main menu")
                            choice = int(input("Chatbot: Your function choice (1/2/3/4/5/6): "))
                            if choice == 1:
                                keywords(selected_pdf)
                            elif choice == 2:
                                print("Chatbot: The topic is ", get_topic_by_filename(selected_pdf))
                            elif choice == 3:
                                print("Function3: This function is under construction.")
                            elif choice == 4:
                                print("Function4: This function is under construction.")
                            elif choice == 5:
                                print("Function5: This function is under construction.")
                            elif choice == 6:
                                print("Function6: This function is under construction.")
                            elif choice == 7:
                                print("Chatbot: Returning to the main menu...")
                            else:
                                print("Chatbot: Invalid choice! Please select 1, 2, or 3.")
                        else:
                            print("Chatbot: Invalid number. Please choose a valid PDF number.")
                    except ValueError:
                        print("Chatbot: Invalid input! Please enter a valid number.")
                else:
                    print("Chatbot: No PDF files found in the folder.")
            elif choice == 3:
                print("Chatbot: Goodbye!")
                break
            else:
                print("Invalid choice! Please select 1, 2, or 3.")
        except ValueError:
            print("Invalid input! Please enter a number (1/2/3).")

if __name__ == "__main__":
    chat()
