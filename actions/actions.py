import rasa_sdk
from rasa_sdk import Tracker, Action, FormValidationAction
import rasa_sdk.events
from rasa_sdk.executor import CollectingDispatcher

import pandas as pd

import dateparser

from datetime import datetime
from typing import Any, Text, Dict, List

appointments = pd.read_csv("appointments.csv")

class ValidateReservationForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_reservation_form"
    
    def __save_csv(self, tracker: Tracker):
        name = tracker.get_slot("name")
        date = tracker.get_slot("date")
        time_start = tracker.get_slot("time_start")
        
        time_end = tracker.get_slot("time_end")
        time_end = dateparser.parse(time_end, languages=["en"])
        time_end = time_end.strftime("%H:%M:%S")
            
        new_appointments = pd.concat([appointments, pd.DataFrame(
            [[name, date, time_start, time_end]], columns=["Name", "Date", "Start", "End"]
        )])
        new_appointments.to_csv("appointments.csv", index=False)

    def validate_name(self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # if tracker.latest_message['intent'].get('affirm'):
        #     return{"name": slot_value.title()}
        
        # # TODO: other intent is catched
        # if slot_value is None:
        #     dispatcher.utter_message("I'm sorry I didn't quite catch that, please enter your name again")
        # elif slot_value is not None and tracker.latest_message['intent'].get('inform') is False:
        #     dispatcher.utter_message(f"Is your name {slot_value}?")
        # else:
            # return {"name": slot_value.title()}

        return {"name": slot_value.title()}
    
    def validate_date(self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        date = dateparser.parse(slot_value, languages=["en"])
        date = date.strftime("%Y-%m-%d")
        
        return {"date": date}

    def validate_time_start(self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        time = dateparser.parse(slot_value, languages=["en"])
        time = time.strftime("%H:%M:%S")
        
        return {"time_start": time}
    
    def validate_time_end(self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        time_end = dateparser.parse(slot_value, languages=["en"])
        time_end = time_end.strftime("%H:%M:%S")

        date_str = tracker.get_slot('date')
        date_datetime = datetime.strptime(date_str, "%Y-%m-%d").date()
        
        time_start_hour = tracker.get_slot("time_start")
        time_start_hour = datetime.strptime(time_start_hour, "%H:%M:%S").time()
        
        dates = appointments["Date"].to_list()
        dates = [datetime.strptime(tmp_date, "%Y-%m-%d").date() for tmp_date in dates]
        
        if date_datetime in dates:
            appointments_time_start = appointments['Start'].loc[pd.to_datetime(appointments['Date']).dt.date == pd.to_datetime(date_str).date()]
            appointments_time_start = [datetime.strptime(tmp_time, "%H:%M:%S").time() for tmp_time in appointments_time_start]
            appointments_time_end = appointments['End'].loc[pd.to_datetime(appointments['Date']).dt.date == pd.to_datetime(date_str).date()]
            appointments_time_end = [datetime.strptime(tmp_time, "%H:%M:%S").time() for tmp_time in appointments_time_end]
            
            for idx, _ in enumerate(appointments_time_start):
                if appointments_time_start[idx] < time_start_hour < appointments_time_end[idx]:
                    dispatcher.utter_message(f"Sorry the time {appointments_time_start[idx]} to {appointments_time_end[idx]} is booked, please select another date")
                    return{"date":None, "time_start":None, "time_end":None}
                else:
                    self.__save_csv(tracker)
                    
                    return{"time_end": time_end}
        else:
            self.__save_csv(tracker)
            
            return{"time_end": time_end}
        
class ActionResetAllSlots(Action):
    def name(self) -> Text:
        return "action_reset_all_slots"
    
    def run(self, dispatcher, tracker, domain):
        return [rasa_sdk.events.AllSlotsReset()]