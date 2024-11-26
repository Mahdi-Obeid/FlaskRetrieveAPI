from models import FinancialStatementItem, QuickRatio, FinancialStatement
from config import db, app


"""
نسبت سریع
quick ratio
"""


def calculate_quick_ratio():
    with app.app_context():
        total_quick_assets = (
            db.session.query(
                FinancialStatementItem.financial_statement_id,
                FinancialStatementItem.amount,
            )
            .filter(FinancialStatementItem.title == "جمع دارایی‌های سریع ")
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
        assets_dict = {item[0]: item[1] for item in total_quick_assets}
        liabilities_dict = {item[0]: item[1] for item in current_liabilities}

        for fs_id in assets_dict.keys():
            if fs_id in liabilities_dict:
                assets = assets_dict[fs_id]
                liabilities = liabilities_dict[fs_id]

                if liabilities != 0:
                    quick_ratio = assets / liabilities

                company_id = (
                    db.session.query(FinancialStatement.company_id)
                    .filter(FinancialStatement.id == fs_id)
                    .scalar()
                )

                ratio_entry = QuickRatio(
                    financial_statement_id=fs_id,
                    company_id=company_id,
                    quick_ratio=quick_ratio,
                )
                db.session.add(ratio_entry)
        db.session.commit()
