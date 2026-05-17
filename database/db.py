from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Transaction
from datetime import date, timedelta
import random

DATABASE_URL = "sqlite:///data_finance.db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Create tables if they don't exist."""
    Base.metadata.create_all(bind=engine)

def get_session():
    """Provide a transactional scope around a series of operations."""
    return SessionLocal()

def seed_dummy_data():
    """Populate database with sample data if empty."""
    session = get_session()
    if session.query(Transaction).count() == 0:
        categories = ['Food', 'Rent', 'Transport', 'Entertainment', 'Utilities']
        for i in range(30):
            days_ago = random.randint(0, 60)
            txn_date = date.today() - timedelta(days=days_ago)
            
            # Generate Expenses
            expense = Transaction(
                amount=round(random.uniform(10.0, 150.0), 2),
                category=random.choice(categories),
                type='Expense',
                description=f'Sample Expense {i}',
                transaction_date=txn_date
            )
            session.add(expense)
            
            # Generate Income occasionally
            if i % 5 == 0:
                income = Transaction(
                    amount=round(random.uniform(1000.0, 3000.0), 2),
                    category='Salary/Freelance',
                    type='Income',
                    description='Sample Income',
                    transaction_date=txn_date
                )
                session.add(income)
        session.commit()
    session.close()