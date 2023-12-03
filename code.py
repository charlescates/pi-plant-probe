from flask import Flask, request, jsonify
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler

import atexit

import smtplib

import ssl
from plant_monitor import PlantMonitor


app = Flask(__name__)
CORS(app)

scheduler = BackgroundScheduler()

scheduler.start()


# Ensure that the scheduler is shut down when the app exits

atexit.register(lambda: scheduler.shutdown())


# Function to send email (fill in your own implementation)

def send_email(receiver_email, plant_type):

    # Initialize your PlantMonitor and retrieve the data

    print("Start of send_email method")

    pm = PlantMonitor()

    humidity = int(pm.get_humidity())

    moisture = pm.get_wetness()

    temp = pm.get_temp()

    temp = int(temp * 9/5 + 32)

    bool = true

    #check the plant type

    while(bool):

        if(plant_type == "Desert"):

            ideal_low_temp = 40

            ideal_high_temp = 80

            ideal_low_moisture = 1

            ideal_high_moisture = 20

            ideal_low_humidity = 40

            ideal_high_humidity = 50

            bool = False

        elif(plant_type == "Flowering"):

            ideal_low_temp = 60

            ideal_high_temp = 80

            ideal_low_moisture = 20

            ideal_high_moisture = 40

            ideal_low_humidity = 40

            ideal_high_humidity = 70

            bool = False

        elif(plant_type == "Foliage"):

            ideal_low_temp = 70

            ideal_high_temp = 80

            ideal_low_moisture = 20

            ideal_high_moisture = 40

            ideal_low_humidity = 60

            ideal_high_humidity = 80

            bool = False

        else:

            print("Invalid plant type was entered!")

            plant_type = input("ReEnter Plant Type:")

    

    

    

    

    #creates the message based on how the collected data compares to the ideal levels

    email_subject = "Plant Health Update"

    email_message = (

        f"Subject: {email_subject}\n\n"

        f"For your plant Type: {plant_type}\n\n"

        f"\tTemperature: {temp}F\n"

        f"\tMoisture: {moisture}%\n"

        f"\tHumidity: {humidity}%\n\n"

    )

    

    

    # Add additional information based on conditions

    if ideal_low_temp <= temp <= ideal_high_temp and ideal_low_moisture <= moisture <= ideal_high_moisture and ideal_low_humidity <= humidity <= ideal_high_humidity:

        email_message += "\tStatus: Your plant is healthy!\n"

    else:

        email_message += "\tAlerts:\n"

        if ideal_low_temp > temp:

            email_message += f"\t\t- Temperature is too low! (Current: {temp}F, Ideal: {ideal_low_temp}-{ideal_high_temp}F)\n"

        elif ideal_high_temp < temp:

            email_message += f"\t\t- Temperature is too high! (Current: {temp}F, Ideal: {ideal_low_temp}-{ideal_high_temp}F)\n"

    

    

        if ideal_low_moisture > moisture:

            email_message += f"\t\t- Moisture is too low! (Current: {moisture}%, Ideal: {ideal_low_moisture}-{ideal_high_moisture}%)\n"

        elif ideal_high_moisture < moisture:

            email_message += f"\t\t- Moisture is too high! (Current: {moisture}%, Ideal: {ideal_low_moisture}-{ideal_high_moisture}%)\n"

    

    

        if ideal_low_humidity > humidity:

            email_message += f"\t\t- Humidity is too low! (Current: {humidity}%, Ideal: {ideal_low_humidity}-{ideal_high_humidity}%)\n"

        elif ideal_high_humidity < humidity:

            email_message += f"\t\t- Humidity is too high! (Current: {humidity}%, Ideal: {ideal_low_humidity}-{ideal_high_humidity}%)\n"

    

    

    

    

    

    

    # Format the message with email headers

    email_subject = "Plant Health Update"

    email_message = f"Subject: {email_subject}\n\n{email_message}"

    

    

    print(email_message)  # This will now print the formatted email message

    

    

    # Connects and sends the email

    port = 465  # For SSL

    smtp_server = "smtp.gmail.com"

    sender_email = "EngeTeam10@gmail.com"  # Sender's address

    receiver_email = "charlescates@vt.edu"  # Receiver's address

    password = "joei yaos maqa davd"  # Sender's email password

    

    

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:

        print("Attempting login.")
        server.login(sender_email, password)
        print("Login successful.")

        print("Attempting to send email.")
        server.sendmail(sender_email, receiver_email, email_message)
        print("Sent email.")
        

        # For now, we'll just print a message

        print(f"Sending email to {receiver_email} for plant type {plant_type}")


# Flask route to schedule emails

@app.route('/submit', methods=['POST'])
def schedule_email():

    # Temporary initial email test email message
    send_email("charlescates@vt.edu","Desert")
    # End temporary message

    data = request.json

    receiver_email = data.get('email')

    plant_type = data.get('plant_type')

    email_frequency = data.get('frequency')


    # Define job id to allow for future modifications or removal

    job_id = f"{receiver_email}_{plant_type}"


    # Remove existing job with the same ID if it exists

    scheduler.remove_job(job_id=job_id, jobstore=None, silent=True)


    # Schedule the email job based on user-selected frequency

    if email_frequency == 'once_an_hour':

        print("Attempting to schedule an email every hour.")
        scheduler.add_job(send_email, 'interval', hours=1, id=job_id, args=[receiver_email, plant_type])
        print("Scheduled an email every hour.")

    elif email_frequency == 'once_every_two_hours':

        scheduler.add_job(send_email, 'interval', hours=2, id=job_id, args=[receiver_email, plant_type])

    elif email_frequency == 'once_a_day':

        scheduler.add_job(send_email, 'interval', days=1, id=job_id, args=[receiver_email, plant_type])

    elif email_frequency == 'twice_a_day':

        scheduler.add_job(send_email, 'interval', hours=12, id=job_id, args=[receiver_email, plant_type])

    else:

        return jsonify({"status": "error", "message": "Invalid frequency selected"}), 400


    return jsonify({"status": "success", "message": "Email schedule set successfully"}), 200


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=80)
