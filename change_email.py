reciever_email = input("Please enter the email you would like to recieve notifications at: ")
file_name = "reciever_email.txt"

email_text = open(file_name, "w")
email_text.write(reciever_email)
email_text.close()