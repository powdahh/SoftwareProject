from flask import Flask, render_template, request, redirect, url_for
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import smtplib, ssl, email
import os
import datetime
import csv
from app.support import support_bp


@support_bp.route('/create_ticket')  # create support ticket page
def support_ticket():
    return render_template('support.html')


@support_bp.route('/support_confirm', methods=['POST', 'GET'])
def support_confirm():  # would take previous form create a ticket
    if request.method == 'POST':
        result = request.form
        receiver_email = ("crunchmovietest@gmail.com", result['email'])
        sender_email = "crunchmovietest@gmail.com"
        time = datetime.datetime.now().strftime("%Y%m%d%I%M%S")  # create ticket number
        subject = "Support ticket #%s" % (time)
        email = result['message']
        user = result['user']
        message = MIMEMultipart()
        text = """/
        User: %s

        %s""" % (user, email)
        message.attach(MIMEText(text, 'plain'))
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = receiver_email

        for x in receiver_email:  # would send to our and their email
            context = ssl.create_default_context()  # send email
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, 'crunchtest123')
                server.sendmail(sender_email, receiver_email, message.as_string())

        with open('support.txt', mode='a') as support:  # add new support ticket to csv
            support_writer = csv.writer(support, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            support_writer.writerow([time, user, 'Unresolved'])
        with open('support.txt', 'r') as f:  # create list with csv and sort
            reader = csv.reader(f)
            your_list = list(reader)
        your_list.sort(reverse=True)
        with open('support.txt', mode='w') as a:  # write csv with updated list
            writer = csv.writer(a)
            writer.writerows(your_list)
    return render_template('support_confirm.html')


@support_bp.route('/support_ticket')  # look at list and allow to set a ticket to resolved
def support_check():
    with open('support.txt', 'r') as f:  # create list with csv and sort
        csv_reader = csv.reader(f, delimiter=',')
        ticket = list(csv_reader)
    ticket.sort(reverse=True)
    return render_template('support_ticket.html', ticket=ticket)


@support_bp.route('/support_resolved', methods=['POST', 'GET'])
def support_remove():  # takes ticket number and set it to resolved
    if request.method == 'POST':
        result = request.form
        ticket = result['ticket']
        with open('support.txt', 'r') as f:
            reader = csv.reader(f)
            your_list = list(reader)
        for x in your_list:
            if ticket == x[0]:
                x[0] = ticket
                x[2] = 'Resolved'
            else:
                pass
        with open('support.txt', mode='w') as support:  # write csv with updated list
            writer = csv.writer(support)
            writer.writerows(your_list)
    return render_template('ticket_resolved.html')