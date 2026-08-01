import csv
import io
from typing import List, Dict, Any

class ReportGenerator:
    def generate_csv(self, data: List[Dict[str, Any]], fieldnames: List[str]) -> str:
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            # filter out fields not in fieldnames
            filtered_row = {k: v for k, v in row.items() if k in fieldnames}
            writer.writerow(filtered_row)
        return output.getvalue()
        
    def generate_user_growth_report(self) -> str:
        # Conceptual: query DB for user signups grouped by day
        data = [
            {"date": "2023-10-01", "signups": 150},
            {"date": "2023-10-02", "signups": 200},
        ]
        return self.generate_csv(data, ["date", "signups"])
        
    def generate_marketplace_report(self) -> str:
        data = [
            {"marketplace": "Spinny", "active_listings": 4500, "avg_price": 500000},
            {"marketplace": "Cars24", "active_listings": 6000, "avg_price": 480000},
        ]
        return self.generate_csv(data, ["marketplace", "active_listings", "avg_price"])

report_generator = ReportGenerator()
