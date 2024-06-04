from flask import (Flask, flash, redirect, render_template, request, send_from_directory, session, url_for)
from datetime import datetime

app = Flask(__name__)

c = datetime.now()
f = c.strftime("%Y%m%d%H%M")

print(f)