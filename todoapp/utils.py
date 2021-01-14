from django.core.mail import EmailMultiAlternatives, get_connection, send_mail
from django.template.loader import render_to_string
from django.template import Context
from django.conf import settings
import codecs
import string
import random


def send_welcome_email(recipient_email, user_name="User"):
    subject, from_email, to = 'Welcome to Hr App', 'nakfaaltu@gmail.com', recipient_email
    text_content = 'This is an important message.'
    f = codecs.open("templates/welcome_message.html", 'r')
    html_content = f.read()
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def senInvitation(email, link):
    context = {"email": email, "link": link}
    msg_plain = render_to_string('invitation.txt', context=context)
    msg_html = render_to_string('invitation.html', context=context)

    try:    
        connection = get_connection(host=settings.EMAIL_HOST,
                                    port=settings.EMAIL_PORT,
                                    username=settings.EMAIL_HOST_USER,
                                    password=settings.EMAIL_HOST_PASSWORD,
                                    use_tls=settings.EMAIL_USE_TLS)

        send_mail(
            'HRAPP Invite you to join',
            msg_plain,
            settings.EMAIL_HOST_USER,
            [email],
            html_message=msg_html,
            connection=connection,
            fail_silently=False
        )
        return True
    except Exception as e:
        print(e)
        return False


def send_password_reset_email(name, email, otp, link):
    newName = "Anonymous"
    if(name != None):
        newName = name.capitalize()

    print("name = " + newName)
    print("link = " + link)

    context = {"name": newName, "otp": otp, "logo_link": link}

    msg_plain = render_to_string('reset_email.txt', context=context)
    msg_html = render_to_string('reset_email.html', context=context)

    connection = get_connection(host=settings.EMAIL_HOST,
                                port=settings.EMAIL_PORT,
                                username=settings.EMAIL_HOST_USER,
                                password=settings.EMAIL_HOST_PASSWORD,
                                use_tls=settings.EMAIL_USE_TLS)

    send_mail(
        'COI Password reset request confirmation',
        msg_plain,
        settings.EMAIL_HOST_USER,
        [email],
        html_message=msg_html,
        connection=connection,
        fail_silently=False
    )


def sortArray(array_of_dic):
    sortedArray = sorted(array_of_dic, key=lambda x: (
        x["helperDigit"] is None, x["helperDigit"], x["helperText"]))
    return sortedArray


def takeStrings(s):
    result = ''.join([i for i in s if not i.isdigit()])
    return result


def takeDigits(s):
    result = ''.join([i for i in s if i.isdigit()])
    return result


def makeTextClean(text):
    if(text):
        newText = text.replace("\n", "").replace("\r", "").replace("\t", " ").replace(
            "    ", " ").replace("   ", " ").replace("  ", " ").replace("\xa0", " ").strip()
        return newText
    return text


def is_roman(text):
    try:
        roman.fromRoman(text)
        return True
    except Exception as e:
        return False


def seperateRomanValue(text):
    value = ""
    string = ""
    validRomanNumerals = ["M", "D", "C", "L", "X", "V", "I"]
    for item in text:
        if(item in validRomanNumerals):
            if is_roman(value+item):
                value += item
            else:
                string += item
        else:
            string += item
    return {"roman": value, "string": string}


def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


def generateChunkFile(data):
    myfile = io.StringIO()
    splitedData = data.split()
    for item in splitedData:
        chunk = " "+item
        myfile.write(chunk)
    return myfile


def makeUrl(request):
    host_port = request.build_absolute_uri()
    count = 0
    result = ""
    for char in host_port:
        if count == 3:
            break
        result += char
        if char == "/":
            count += 1
    return result


def get_host(self):
    request = self.context.get('request')
    host = makeUrl(request)
    return host

# function to generate OTP


def generateOTP():
    digits = "0123456789"
    OTP = ""
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


def generateRandomString():
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(10))
