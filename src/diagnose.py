import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# 1. Load data
# --------------------------------------------------

machines = pd.read_csv("data/machines.csv")
cases = pd.read_csv("data/maintenance_cases.csv")


# --------------------------------------------------
# 2. Select machine
# --------------------------------------------------

machine_id = input("Enter Machine ID: ").strip()

machine = machines[machines["machine_id"] == machine_id]

if machine.empty:
    print("\nMachine not found.")
    exit()


machine_info = machine.iloc[0]

print("\n" + "=" * 65)
print("ENGINEERING MEMORY — MACHINE CONTEXT")
print("=" * 65)

print("Machine ID      :", machine_info["machine_id"])
print("Model           :", machine_info["machine_model"])
print("Type            :", machine_info["machine_type"])
print("Manufacturer    :", machine_info["manufacturer"])
print("Operating Hours :", machine_info["operating_hours"])
print("Status          :", machine_info["status"])


# --------------------------------------------------
# 3. Current symptoms
# --------------------------------------------------

symptoms = input("\nEnter current symptoms: ").strip()


# --------------------------------------------------
# 4. Get historical cases for this machine
# --------------------------------------------------

machine_cases = cases[
    cases["machine_id"] == machine_id
].copy()

if machine_cases.empty:
    print("\nNo historical cases found for this machine.")
    exit()


# --------------------------------------------------
# 5. Create searchable historical text
# --------------------------------------------------

machine_cases["search_text"] = (
    machine_cases["symptom"].fillna("") + " " +
    machine_cases["inspection_finding"].fillna("") + " " +
    machine_cases["failure_mode"].fillna("") + " " +
    machine_cases["component"].fillna("")
)


# --------------------------------------------------
# 6. Convert text to vectors
# --------------------------------------------------

vectorizer = TfidfVectorizer(stop_words="english")

case_vectors = vectorizer.fit_transform(
    machine_cases["search_text"]
)

query_vector = vectorizer.transform([symptoms])


# --------------------------------------------------
# 7. Calculate similarity
# --------------------------------------------------

scores = cosine_similarity(
    query_vector,
    case_vectors
)[0]

machine_cases["similarity"] = scores

results = machine_cases.sort_values(
    "similarity",
    ascending=False
)


# --------------------------------------------------
# 8. Display diagnosis
# --------------------------------------------------

print("\n" + "=" * 65)
print("ENGINEERING MEMORY — DIAGNOSIS")
print("=" * 65)

top_case = results.iloc[0]

top_score = top_case["similarity"]

# Convert similarity into a simple confidence score
confidence = min(top_score * 100, 95)


print("\nTOP CANDIDATE")
print("-" * 65)

print("Likely Cause :", top_case["failure_mode"])
print("Component    :", top_case["component"])
print("Confidence   :", round(confidence, 1), "%")


print("\nHISTORICAL EVIDENCE")
print("-" * 65)

print("Case ID      :", top_case["case_id"])
print("Previous Symptom:")
print(top_case["symptom"])

print("\nInspection Finding:")
print(top_case["inspection_finding"])

print("\nPrevious Successful Repair:")
print(top_case["repair_action"])

print("\nPrevious Outcome:")
print(top_case["outcome"])


# --------------------------------------------------
# 9. Alternative causes
# --------------------------------------------------

if len(results) > 1:

    print("\n" + "=" * 65)
    print("ALTERNATIVE HISTORICAL CAUSES")
    print("=" * 65)

    for _, case in results.iloc[1:3].iterrows():

        alt_confidence = min(
            case["similarity"] * 100,
            95
        )

        print("\nCause      :", case["failure_mode"])
        print("Component  :", case["component"])
        print("Confidence :", round(alt_confidence, 1), "%")
        print("Case       :", case["case_id"])


# --------------------------------------------------
# 10. Recommended inspection
# --------------------------------------------------

print("\n" + "=" * 65)
print("RECOMMENDED INSPECTION")
print("=" * 65)

print(
    "Review the inspection findings from the highest-ranked "
    "historical case before replacing components."
)

print("\nNote:")
print(
    "This system provides decision support based on historical "
    "engineering cases. It does not confirm the physical root cause."
)