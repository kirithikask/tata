import csv
import random
import itertools

random.seed(42)

MACHINES = [f"EXC-{i:03d}" for i in range(1, 11)]

# failure -> (component(s), [symptom base templates], [resolution templates])
FAILURES = {
    "Internal pump leakage": {
        "components": ["Hydraulic Pump"],
        "symptoms": [
            "slow boom movement and weak digging force {mod}",
            "digging force dropped noticeably {mod}",
            "arm feels sluggish under load {mod}",
            "overall power loss across all functions {mod}",
            "reduced lifting capacity {mod}",
            "boom and arm both weaker than normal {mod}",
            "struggles to lift full bucket load {mod}",
            "noticeable loss of hydraulic power {mod}",
        ],
        "resolutions": [
            "Replaced pump seal kit",
            "Replaced pump wear plate",
            "Rebuilt main pump assembly",
            "Replaced pump seal kit and flushed system",
            "Repaired internal pump components",
        ],
    },
    "Cooler restriction": {
        "components": ["Oil Cooler"],
        "symptoms": [
            "machine slows down noticeably {mod}",
            "operation fine at start but slows {mod}",
            "overheating warning light followed by slow response {mod}",
            "performance drops as oil temperature rises {mod}",
            "cooler fan not spinning, oil temperature rising {mod}",
            "gradual power loss tied to running time {mod}",
        ],
        "resolutions": [
            "Cleaned and flushed cooler",
            "Replaced fan belt and cleaned fins",
            "Pressure-washed cooler core",
            "Replaced cooling fan motor",
            "Replaced seized cooling fan bearing",
        ],
    },
    "Filter blockage": {
        "components": ["Hydraulic Filter"],
        "symptoms": [
            "jerky and inconsistent boom motion {mod}",
            "loss of power during simultaneous functions {mod}",
            "gradual power loss over several days {mod}",
            "filter warning light on dashboard {mod}",
            "sudden jerky movement after refueling {mod}",
            "inconsistent response across functions {mod}",
        ],
        "resolutions": [
            "Replaced return line filter",
            "Cleaned suction strainer",
            "Replaced hydraulic filter element",
            "Cleaned suction strainer contaminated with debris",
        ],
    },
    "Valve problem": {
        "components": ["Control Valve"],
        "symptoms": [
            "boom does not respond smoothly to lever input {mod}",
            "arm drifts down on its own when idle {mod}",
            "one function works fine but another is weak {mod}",
            "bucket curl function completely unresponsive {mod}",
            "swing function delayed by a few seconds {mod}",
            "uneven response between functions {mod}",
        ],
        "resolutions": [
            "Cleaned and lubricated spool valve",
            "Replaced valve seal kit",
            "Replaced directional control valve",
            "Cleaned and adjusted spool valve linkage",
        ],
    },
    "Accumulator pressure loss": {
        "components": ["Accumulator"],
        "symptoms": [
            "delayed response when starting boom movement {mod}",
            "jerky start on hydraulic functions after startup {mod}",
            "sudden jolt when starting any hydraulic function {mod}",
            "jerky start that smooths out once moving {mod}",
        ],
        "resolutions": [
            "Recharged accumulator to spec pressure",
            "Replaced accumulator bladder",
            "Serviced accumulator and recharged pressure",
        ],
    },
    "Oil contamination": {
        "components": ["Hydraulic Oil"],
        "symptoms": [
            "overall sluggish performance across all functions {mod}",
            "unusual noise and reduced power in all functions {mod}",
            "performance degraded steadily over a month {mod}",
            "foamy oil visible in reservoir sight glass {mod}",
            "metallic smell from hydraulic tank {mod}",
            "system-wide power loss with visible oil issue {mod}",
        ],
        "resolutions": [
            "Drained and replaced hydraulic oil",
            "Flushed system and replaced oil",
            "Replaced with correct oil grade",
            "Drained oil, replaced breather cap, refilled",
            "Flushed system, replaced oil and filter",
        ],
    },
    "Cylinder leakage": {
        "components": ["Boom Cylinder", "Arm Cylinder", "Bucket Cylinder"],
        "symptoms": [
            "visible fluid leak near the cylinder {mod}",
            "cylinder slowly drops on its own when parked {mod}",
            "weak force compared to other functions {mod}",
            "oil residue building up on the cylinder rod {mod}",
            "creeps down over several minutes when parked {mod}",
        ],
        "resolutions": [
            "Replaced cylinder seal kit",
            "Rebuilt cylinder",
            "Replaced cylinder assembly",
            "Replaced cylinder rod seal",
            "Replaced cylinder holding valve",
        ],
    },
    "Pilot pressure problem": {
        "components": ["Pilot System"],
        "symptoms": [
            "levers feel light and unresponsive {mod}",
            "inconsistent control response across functions {mod}",
            "machine feels unresponsive right after startup {mod}",
            "all functions feel weak but pump pressure tests normal {mod}",
        ],
        "resolutions": [
            "Replaced pilot pressure reducing valve",
            "Replaced pilot filter",
            "Repaired pilot pump",
        ],
    },
    "Line restriction": {
        "components": ["Hydraulic Line"],
        "symptoms": [
            "gradual loss of pressure during long digging cycles {mod}",
            "slow function only on one side of the machine {mod}",
            "intermittent loss of power only during turns {mod}",
        ],
        "resolutions": [
            "Replaced hydraulic hose",
            "Replaced fitting and line section",
            "Replaced worn hydraulic hose near swing joint",
        ],
    },
}

MODIFIERS = [
    "under load", "after a long shift", "when cold", "when hot",
    "at high RPM", "during simultaneous functions", "after startup",
    "during digging cycles", "on uneven ground", "intermittently",
    "after refueling", "on a slope",
]

TARGET_TOTAL = 1000

# Roughly even split across the 9 failure types
failure_list = list(FAILURES.keys())
per_failure = TARGET_TOTAL // len(failure_list)
remainder = TARGET_TOTAL - per_failure * len(failure_list)

rows = []
seen_signatures = set()
case_num = 1

for idx, failure in enumerate(failure_list):
    info = FAILURES[failure]
    count = per_failure + (1 if idx < remainder else 0)

    combos = list(itertools.product(
        info["components"], info["symptoms"], MODIFIERS, info["resolutions"], MACHINES
    ))
    random.shuffle(combos)

    generated = 0
    for component, symptom_t, mod, resolution, machine in combos:
        if generated >= count:
            break
        symptom = symptom_t.format(mod=mod)
        signature = (machine, component, failure, symptom)
        if signature in seen_signatures:
            continue
        seen_signatures.add(signature)
        case_id = f"CASE-{case_num:04d}"
        rows.append([case_id, machine, component, failure, symptom, resolution])
        case_num += 1
        generated += 1

random.shuffle(rows)
# reassign sequential case_ids after shuffle so IDs aren't grouped by failure type
for i, row in enumerate(rows, start=1):
    row[0] = f"CASE-{i:04d}"

with open("data/maintenance_cases.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["case_id", "machine_id", "component", "failure", "symptoms", "resolution"])
    w.writerows(rows)

print(f"Wrote {len(rows)} cases")

# quick duplicate check on (machine, component, failure, symptom)
sigs = [(r[1], r[2], r[3], r[4]) for r in rows]
print("Unique signatures:", len(set(sigs)), "of", len(sigs))
