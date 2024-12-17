import csv
from config import db, app
from models import RatioList


def import_ratio_list(file_path):
    with app.app_context():
        with open(file_path, mode="r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                if not RatioList.query.filter_by(id=row["id"]).first():
                    ratio = RatioList(
                        id=int(row["id"]),
                        ratioNameEng=row["ratioNameEng"],
                        ratioNamePer=row["ratioNamePer"],
                        ratioSymbol=row["ratioSymbol"],
                    )
                    db.session.add(ratio)
            db.session.commit()


if __name__ == "__main__":
    file_path = "ratio_list.csv"
    import_ratio_list(file_path)
