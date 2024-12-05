from datetime import datetime
from zoneinfo import ZoneInfo
from pydantic import BaseModel

# Generic message model for endpoints responses
class Message(BaseModel):
    message: str
    
def parse_date(date_str):
        for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d %H:%M:%S"):
            try:
                utc_time = datetime.strptime(date_str, fmt).replace(tzinfo=ZoneInfo("UTC"))

                # Converter para o horário de São Paulo
                brasilia_time = utc_time.astimezone(ZoneInfo("America/Sao_Paulo"))
                return brasilia_time

            except ValueError:
                continue
        raise ValueError(f"time data '{date_str}' does not match any expected format")

def convert_mongo_document(doc):
    if 'c_date' in doc:
        if isinstance(doc.get('c_date'), dict) and '$date' in doc['c_date']:
            # doc['c_date'] = doc['c_date']['$date']
            c_date = str(doc['c_date']['$date'])
            doc['c_date'] = parse_date(c_date)
    if 'initial_date' in doc and doc['initial_date'] != "":
        initial_date = str(doc['initial_date']['$date'])
        doc['initial_date'] = parse_date(initial_date)
    if '_id' in doc:
        doc['id'] = str(doc['_id']['$oid'])
    if 'historic' in doc and doc['historic'] is not None:
        for item in doc['historic']:
            if 'initial_date' in item:
                initial_date = str(item['initial_date']['$date'])
                item['initial_date'] = parse_date(initial_date)

    return doc

