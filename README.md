# VACAS
Vehicle Accounts Automation Service

This program is used to create a confluence page with a list of vehicle accounts. These vehicle accounts are taken from CDC-int and CDC-emea and then formatted to an html.

It was created using Python and has both CLI and GUI interfaces, which was created using pysimplegui.
It was originally created to run on MAC.

The best use of it is to run after each log in. For that you can use Automate from MAC to run a shell script and then use the automate application to run everytime you log.

Also, you may set an environment variable with your password:
export PASSWORD = --insert password here--
