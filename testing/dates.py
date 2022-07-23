from datetime import datetime

string_input_with_date = "2017-7-13"
past = datetime.strptime(string_input_with_date, "%Y-%m-%d")
present = datetime.now()
print(past.date() < present.date())