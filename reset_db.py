from src.infrastructure.database.supabase_client import SessionLocal
from src.infrastructure.database.models import CategoryModel, QuestionModel
from src.infrastructure.seed_data import seed_database
db = SessionLocal()
db.query(QuestionModel).delete()
db.query(CategoryModel).delete()
db.commit()
seed_database(db)
print("DB Reset & Seeded Successfully!")
db.close()
