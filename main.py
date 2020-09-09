import scraper
import database
import time
import smtpd, ssl, smtplib, getpass

# url = str(input("Enter the item you want price track. ")) #press space after input
# url = scraper.url


def send_email():
    #  salefinder.NED@gmail.com
    port = 465
    password = ''  # todo getpass.getpass()
    sender_email = "salefinder.ned@gmail.com"
    reciever_email = "ericdong97@gmail.com"
    smtp_server = 'smtp.gmail.com'
    message = f"Hello, the following item is now on sale: {123}"

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, reciever_email, message)


entries_in_db = database.read_db()
# print(entries_in_db)


def main(url_to_check):
    data = scraper.get_item_info(url_to_check)
    if database.is_empty():
        database.write_db(data)

    # reads the txtfile db and returns a dictionary key=url value=dictionary
    if str(url_to_check) not in entries_in_db:  # if already in dont write
        print("Item added.")
        database.write_db(data)
    else:
        print(f"Item already exists, checking {url_to_check}")
        print(data)
        print(data['price'])  # todo its this one
        print(entries_in_db[str(url_to_check)]['price'])
        if data['price'] < entries_in_db[str(url_to_check)]['price']:  # todo this needs to change
            print("There is a sale!")
            entries_in_db[str(url_to_check)]['sale'] = True
            # database.delete_db(data["url"])

        if entries_in_db[str(url_to_check)]['sale'] is True:
            send_email()

main(str(input("Enter the item you want price track. ")))
for url_key in entries_in_db:
    main(url_key)



# while True:
#     print(main())
#     time.sleep(60)
