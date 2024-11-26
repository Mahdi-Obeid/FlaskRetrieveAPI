from models import FinancialStatementItem, CashRatio, FinancialStatement
from config import db, app


"""
نقد به بدهی‌های جاری
cash on current liabilities
"""


def calculate_cash_ratio():
    with app.app_context():
        total_cash = (
            db.session.query(
                FinancialStatementItem.financial_statement_id,
                FinancialStatementItem.amount,
            )
            .filter(FinancialStatementItem.title == "موجودی نقد")
            .all()
        )

        current_liabilities = (
            db.session.query(
                FinancialStatementItem.financial_statement_id,
                FinancialStatementItem.amount,
            )
            .filter(FinancialStatementItem.title == "جمع بدهی‌های جاری")
            .all()
        )

        # Convert to dictionaries for easier lookup
        cash_dict = {item[0]: item[1] for item in total_cash}
        liabilities_dict = {item[0]: item[1] for item in current_liabilities}

        for fs_id in cash_dict.keys():
            if fs_id in liabilities_dict:
                total_cash = cash_dict[fs_id]
                liabilities = liabilities_dict[fs_id]

                if liabilities != 0:
                    cash_ratio = total_cash / liabilities

                company_id = (
                    db.session.query(FinancialStatement.company_id)
                    .filter(FinancialStatement.id == fs_id)
                    .scalar()
                )

                ratio_entry = CashRatio(
                    financial_statement_id=fs_id,
                    company_id=company_id,
                    cash_ratio=cash_ratio,
                )
                db.session.add(ratio_entry)
        db.session.commit()
