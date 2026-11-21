"""
===============================================
    Smart Hire AI Agent
===============================================
Author: Prajakta Shinde
Date:   14th Nov 2026

Description: 
This project is text based AI mock Interview Agent

This project demonstrates the practical implementation of 
1. AI Agent
2. LLM Integration
3. Prompt Engineering
4. Answer Evaluation
5. Interview Automation
6. Report Generation
7. Memory through Interview History

===============================================
""" 

from questions import questions
from interview_agent import MockInterviewAgent
from report_generator import save_report

def print_header():
    """
        Function Name : print_header
    """

    print("="*70)
    print("         AI Mock Interview Agent")
    print("         Text Based Version")
    print("         Author: Prajakta Shinde")
    print("         Date: 14th Nov 2026")
    print("="*70)

def show_menu():
    """
        Function Name : show_menu
        Description: Displays the interview mode options to the user
    """

    print("\n Select Interview Mode")
    print("1. Start Full Interview")
    print("2. Start Topic-wise Interview")
    print("3. Exit")

def get_available_topics():
    """
        Function Name : get_available_topics
        Description: Extracts unique topics from the question bank
        Return Value : List of available topics
    """

    topics = []
    # Traverse all the questions and collect unique topics
    for items in questions:
        if items["topic"] not in topics:
            topics.append(items["topic"])
    return topics

def start_interview(agent, selected_questions):
    """
        Function Name : start_interview
        Description: Conducts the interview by asking selected questions.
        Parameters: 
        agent : Object of MockInterviewAgent class
        selected_questions : List of questions selected for interview
    """

    # Ask question one by one
    for index, item in enumerate(selected_questions, start= 1):
        topic = item["topic"]
        question = item["question"]

        print("\n" + "=" * 70)
        print(f"Question {index}")
        print("Topic : ",topic)
        print("Question : ", question)
        print("="*70)

        # Accept Student's answer through text input
        answer = input("\n Enter your Answer: \n")

        # Handle empty answer case
        if answer.strip() == "":
            answer = "Student didn't give any answer"

        print("\nEvaluating your answer using Groq's openai/gpt-oss-120b model...")
        print("Please wait while your response is getting evaluated by AI Interview Agent")

        # Send Question and Answer to AI Agent for evaluation
        evaluation = agent.evaluate_answer(topic, question, answer)
        print("\n Evaluation Result :")
        print("="*70)
        print(evaluation)
        print("="*70)

        # Ask user whether to continue the interview or stop
        choice = input("\nDo you want to continue? yes/no: ")

        if choice.strip().lower() != "yes":
            break

def main():
     
    """
        Function Name : main
        Description: Entery point of AI Mock Interview Agent Project
    """
     
    print_header()
    print("Welcome to SmartHire AI Mock Interview Agent")
    print("This system conducts technical interviews using Groq's openai/gpt-oss-120b model.")
    print("This project is designed for practical understanding of AI Agents.\n")

    # Accept Student name
    student_name = input("Enter Student name: ")

    # if student name is empty then use default name
    if student_name.strip() == "":
        student_name = "Student"

    # Create object of MockInterviewAgent
    agent = MockInterviewAgent(student_name)

    print(f"\nWelcome {student_name} to AI Mock Interview")
    print("The interview will evaluate your technical answers using LLM")

    while True:
        show_menu()

        choice = input("\n Enter your choice: ")

        # Full Interview Mode
        if choice == "1":
            start_interview(agent, questions)

            # Generate final report after interview completion
            report = agent.generate_final_report()
            print(report)

            # Save final report into reports folder
            filename = save_report(student_name, report)

            print("\nInterview completed successfully.")
            print("Final report generated successfully.")
            print("Report saved at:", filename)
            break
        # Topic-wise interview mode
        elif choice == "2":
            topics = get_available_topics()
            print("\nAvailable Topics:")

            # Display available topics
            for index, topic in enumerate(topics, start=1):
                print(f"{index}. {topic}")

            try:
                topic_choice = int(input("\nSelect topic number: "))

                # Validate topic choice
                if topic_choice < 1 or topic_choice > len(topics):
                    print("\nInvalid topic number. Please try again.")
                    continue

                selected_topic = topics[topic_choice - 1]
                selected_questions = []

                # Select questions matching selected topic
                for item in questions:
                    if item["topic"] == selected_topic:
                        selected_questions.append(item)

                print(f"\nYou selected topic: {selected_topic}")

                start_interview(agent, selected_questions)

                # Generate final report
                report = agent.generate_final_report()
                print(report)

                # Save final report
                filename = save_report(student_name, report)

                print("\nInterview completed successfully.")
                print("Final report generated successfully.")
                print("Report saved at:", filename)
                break

            except ValueError:
                print("\nInvalid input. Please enter a valid number.")

        # Exit option
        elif choice == "3":
            print("\nThank you for using AI Mock Interview Agent.")
            print("Keep learning, keep practicing.")
            break
        # Invalid menu option
        else:
            print("\nInvalid choice. Please try again.")
            
# Program execution starts from here            
if __name__ == "__main__":
    main()