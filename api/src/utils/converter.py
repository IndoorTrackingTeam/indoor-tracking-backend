from datetime import datetime

from pydantic import BaseModel

# Generic message model for endpoints responses
class Message(BaseModel):
    message: str
    
def parse_date(date_str):
        for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d %H:%M:%S"):
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        raise ValueError(f"time data '{date_str}' does not match any expected format")

def convert_mongo_document(doc):
    if 'c_date' in doc:
        if isinstance(doc.get('c_date'), dict) and '$date' in doc['c_date']:
            doc['c_date'] = doc['c_date']['$date']

    if 'initial_date' in doc and doc['initial_date'] != "":
        doc['initial_date'] = doc['initial_date']['$date']
    if '_id' in doc:
        doc['id'] = str(doc['_id']['$oid'])
    if 'historic' in doc and doc['historic'] is not None:
        for item in doc['historic']:
            if 'initial_date' in item:
                item['initial_date'] = item['initial_date']['$date']

    return doc

