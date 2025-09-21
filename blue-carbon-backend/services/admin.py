from database import SessionLocal
from models.db_model import MRVData

def approve_data(data_id: int):
    db = SessionLocal()
    record = db.query(MRVData).filter(MRVData.id == data_id).first()
    if record:
        record.verified = True
        db.commit()
        db.refresh(record)
    db.close()
    return record

def reject_data(data_id: int):
    db = SessionLocal()
    record = db.query(MRVData).filter(MRVData.id == data_id).first()
    if record:
        db.delete(record)
        db.commit()
    db.close()
    return True
