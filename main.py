import scraper
import database
import time
import smtpd, ssl, smtplib, getpass

# url = str(input("Enter the item you want price track. ")) #press space after input
url = scraper.url
# todo okay i should pass the entire list of urls to check for sale each time main.py runs
 # it will still ask for a link - giveuser option if no link just check urls
 # also add exception handles for None types everywhere


def send_email():
    #  salefinder.NED@gmail.com
    port = 465
    password = 'haruc4h9'  # todo getpass.getpass()
    sender_email = "salefinder.ned@gmail.com"
    reciever_email = "ericdong97@gmail.com"
    smtp_server = 'smtp.gmail.com'
    message = f"Hello, the following item is now on sale: {url}"

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, reciever_email, message)


def main():
    data = scraper.get_item_info(url)
    if database.is_empty():
        database.write_db(data)

    dict_db = database.read_db()
    # reads the txtfile db and returns a dictionary key=url value=dictionary
    if str(url) not in dict_db:  # if already in dont write
        database.write_db(data)
    else:


        try:
            if data['price'] < dict_db[str(url)]['price']:
                dict_db[str(url)]['sale'] = True
                # todo delete data entry
                database.delete_db(data["url"])

            if dict_db[str(url)]['sale'] is True:
                send_email()
        except KeyError:
            print('key does not exist2')

# while True:
#     print(main())
#     time.sleep(60)

main()
