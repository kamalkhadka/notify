# NotifyMe

## Overview:
NotifyMe is a mass messaging service. It can be accessed at https://notify-mass.herokuapp.com/

### Goal:
Make mass communication organized, fast, and easy. 

### Expected Users:
Any company / group that wants to send mass messages can use NotifyMe. Some user case scenarios are emergency notifications, event changes or updates, reminders, announcements, appointment reminders etc.

### Data:
This application will make use of [SendGrid API](https://sendgrid.com/docs/API_Reference/api_v3.html) to send emails and [Authy](https://authy.com/) for email verification for the user. This app will collect basic user information to signup. A user is allowed to add contact and send email messages after signing up.

### Outline:
**Database Schema:**
    User : Name, Email, Password, Phone
    Contact: Name, email
    Group: Name

**Security:**
    Secure user password
    Secure application feature for logged in user only


**Functionality:**
		
 >Anonymous user can
 >- Read about service
 		
>Registered user can
> - Add contact
> - Create group 
> - Send message