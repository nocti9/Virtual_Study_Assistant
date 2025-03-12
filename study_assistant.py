#Stage 1
if __name__ == '__main__':
    progress = 0
    study_schedule = {}
    while True:
        subject = input("Enter subject name: ")
        if subject != "":
            while True:
                try:
                    time = int(input(f"Enter time allocated for {subject}: "))
                    if time <= 0:
                        print("Invalid input. Please enter positive value.")
                        continue
                    else:
                        break
                except ValueError:
                    print("Invalid input. Please enter an integer value.")
            study_schedule[subject] = time
        else:
            break

#Stage 2
    tot_time = int(sum(study_schedule.values())) # Total study time
    tot_t_breaks = tot_time + ((tot_time // 45)*15) # Total study time + 15 minutes breaks

    if study_schedule != {}:
        print("Your study plan:")
        for subject, time in study_schedule.items():
            print(f"{subject}: {time} minutes")
        print(f"""Total study time: {tot_time} minutes
Total time including breaks: {tot_t_breaks} minutes""")
#Stage 3
        t_spent_st = int(input("Enter time spent studying: "))

        if tot_time > 0:
            progress = (t_spent_st * 100 / tot_time)
        else:
            progress = 0
        if progress >= 100:
            progress = 100
        print(f"You have completed {progress:.2f}% of your planned study time.")

#Stage 4
        import os
        from dotenv import load_dotenv

        load_dotenv()

        api_key = os.getenv("api_key")
        if api_key is None:
            raise ValueError("API key not found. Make sure your .env file is set up correctly.")

        from huggingface_hub import InferenceClient

        client = InferenceClient(token=api_key)
        prompt = """
        I have to prepare for my {subjects} exams. I've completed {completeness:.2f}% of my curriculum. My motivation should be:
        """.format(
            subjects = ', '.join(study_schedule.keys()),
            completeness = progress
        )

        response = client.text_generation(
            prompt = prompt,
            model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            temperature = 0.01,
            max_new_tokens = 50,
            seed = 42,
            return_full_text = True,
        )
        print(response)