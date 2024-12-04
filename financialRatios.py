from models import RatioCalculation, FinancialStatementItem, FinancialStatement
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

        cash_dict = {item[0]: item[1] for item in total_cash}
        liabilities_dict = {item[0]: item[1] for item in current_liabilities}

        for fs_id in cash_dict.keys():
            if fs_id in liabilities_dict:
                total_cash = cash_dict[fs_id]
                liabilities = liabilities_dict[fs_id]

                if liabilities != 0:
                    cash_ratio = total_cash / liabilities
                    ratio = RatioCalculation(
                        ratio_list_id=1,
                        ratioNameEng= "cash ratio",
                        ratioNamePer= "نقد به بدهی‌های جاری",
                        financial_statement_id=fs_id,
                        company_original_id=db.session.query(FinancialStatement.company_id).filter(FinancialStatement.id == fs_id).scalar(),
                        fiscal_year_end=db.session.query(FinancialStatement.fiscal_year_end).filter(FinancialStatement.id == fs_id).scalar(),
                        calculated_ratio=cash_ratio,
                    )
                    db.session.add(ratio)
        db.session.commit()


"""
نسبت جاری
current ratio
"""


def calculate_current_ratio():
    with app.app_context():
        current_assets = (
            db.session.query(
                FinancialStatementItem.financial_statement_id,
                FinancialStatementItem.amount,
            )
            .filter(FinancialStatementItem.title == "جمع دارایی‌های جاری")
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

        assets_dict = {item[0]: item[1] for item in current_assets}
        liabilities_dict = {item[0]: item[1] for item in current_liabilities}

        for fs_id in assets_dict.keys():
            if fs_id in liabilities_dict:
                assets = assets_dict[fs_id]
                liabilities = liabilities_dict[fs_id]

                if liabilities != 0:
                    current_ratio = assets / liabilities
                    ratio = RatioCalculation(
                        ratio_list_id=2,
                        ratioNameEng= "current ratio",
                        ratioNamePer= "نسبت جاری",
                        financial_statement_id=fs_id,
                        company_original_id=db.session.query(FinancialStatement.company_id).filter(FinancialStatement.id == fs_id).scalar(),
                        fiscal_year_end=db.session.query(FinancialStatement.fiscal_year_end).filter(FinancialStatement.id == fs_id).scalar(),
                        calculated_ratio=current_ratio,
                    )
                    db.session.add(ratio)
        db.session.commit()


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

        assets_dict = {item[0]: item[1] for item in total_quick_assets}
        liabilities_dict = {item[0]: item[1] for item in current_liabilities}

        for fs_id in assets_dict.keys():
            if fs_id in liabilities_dict:
                assets = assets_dict[fs_id]
                liabilities = liabilities_dict[fs_id]

                if liabilities != 0:
                    quick_ratio = assets / liabilities
                    ratio = RatioCalculation(
                        ratio_list_id=3,
                        ratioNameEng= "quick ratio",
                        ratioNamePer= "نسبت سریع",
                        financial_statement_id=fs_id,
                        company_original_id=db.session.query(FinancialStatement.company_id).filter(FinancialStatement.id == fs_id).scalar(),
                        fiscal_year_end=db.session.query(FinancialStatement.fiscal_year_end).filter(FinancialStatement.id == fs_id).scalar(),
                        calculated_ratio=quick_ratio,
                    )
                    db.session.add(ratio)
        db.session.commit()
