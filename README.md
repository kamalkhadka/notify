# NotifyMe

## Overview:
NotifyMe is a mass messaging service.  

### Goal:
Make mass communication organized, fast, and easy. 

### Expected Users:
Any company / group that wants to send mass messages can use NotifyMe. Some user case scenarios are emergency notifications, weather alerts, event changes or updates, reminders, announcements, appointment reminders etc.

### Data:
This application will make use of Twilio API for sending SMS and SendGrid API to send emails. This app will collect basic user information to signup. A user is allowed to add contact and send messages to them via sms, email.

### Outline:
**Database Schema:**
    User : Name, Email, Password
    Contact: Name, Phone numbers, emails
    Group: Name
    Template: Name, Type (sms/email)

**Security:**
    Secure user password
    Secure application feature for logged in user only


**Functionality:**
		
 >Anonymous user can
 >- Read about service
 >- View pricing
 >- Onboarding process 
		
>Registered user can
> - Add contact
> - Create sms / email template
> - Create group 
> - Broadcast message