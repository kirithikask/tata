import csv

models = [
    ("EX210", 2019), ("EX70", 2021), ("EX130", 2018), ("EX200", 2020),
    ("EX55", 2022), ("EX300", 2017), ("EX120", 2020), ("EX55U", 2021),
    ("EX210LC", 2019), ("EX100", 2022),
]
locations = ["Site-A", "Site-B", "Site-C", "Site-D"]
statuses = ["Active", "Active", "Active", "Maintenance"]

rows = []
for i, (model, year) in enumerate(models, start=1):
    machine_id = f"EXC-{i:03d}"
    hours = 2000 + (i * 913) % 10000
    loc = locations[i % len(locations)]
    status = statuses[i % len(statuses)]
    rows.append([machine_id, "Excavator", f"Tata Hitachi {model}", year, hours, loc, status])

with open("data/machines.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["machine_id", "machine_type", "model", "manufacture_year", "operating_hours", "location", "status"])
    w.writerows(rows)

print(f"Wrote {len(rows)} machines")
