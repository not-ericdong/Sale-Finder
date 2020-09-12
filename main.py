import scraper
import database
import time
import smtpd, ssl, smtplib
from email.mime.text import MIMEText

url_input = str(input("Enter the URL of the item you want to price track, if you want to check prices just hit enter. "))  # press space after input - pycharm

# reads the txtfile db and returns a dictionary key=url value=dictionary
entries_in_db = database.read_db()


def send_email(new_data, old_data):
    sale_perc = round((float(old_data)-float(new_data))/float(old_data), 2)*100
    port = 465

    # Change this to your email to recieve emails
    r_email = open("reciever_email.txt", "r")
    reciever_email = r_email.readline()
    r_email.close()

    message = MIMEText(f"\n Hello, the following item is now on sale: {url_input}"
                       f"\n The old price was {old_data}."
                       f"\n The price is now {new_data}."
                       f"\n The item is {sale_perc}% off!"
                       f"\n \n This item is still being tracked."
                       )
    password = 'haruc4h9'
    sender_email = "salefinder.ned@gmail.com"
    smtp_server = 'smtp.gmail.com'
    message['Subject'] = "Sale Finder"

    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL(smtp_server, port, context=context)
    server.login(sender_email, password)
    server.sendmail(sender_email, reciever_email, message.as_string())
    server.quit
    print("Email sent!")


def main(url_to_check):
    data = scraper.get_item_info(url_to_check)

    if database.is_empty():  # writing first entry
        database.write_db(data)
        print("Item added.")
    else:
        if str(url_to_check) not in entries_in_db:  # if already in don't write
            database.write_db(data)
            print("Item added.")

        else:  # if item is already in db then check the price
            new_price = data['price']
            old_price = entries_in_db[str(url_to_check)]['price']
            print(f"Item already exists, checking {url_to_check}")
            # print("Price now: " + str(new_price))
            # print("Price before: " + str(old_price))
            try:
                if new_price < old_price:  # if new price < old
                    print("There is a sale!")
                    entries_in_db[str(url_to_check)]['sale'] = True
                    database.delete_db(data["url"])  # delete line with same url
                    database.write_db(data)         # add line back with new price
                elif new_price > old_price:  # if new price > old
                    database.delete_db(data["url"])
                    database.write_db(data)
            except TypeError:
                pass

            if entries_in_db[str(url_to_check)]['sale'] is True:
                print("Sending email...")
                send_email(new_price, old_price)


if url_input is not "":  # todo handle none url inputs
    main(url_input)
for url_key in entries_in_db:
    main(url_key)

# while True:
#     print(main())
#     time.sleep(600)
