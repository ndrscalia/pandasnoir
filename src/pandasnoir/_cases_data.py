from dataclasses import dataclass

@dataclass
class CaseInfo:
    """Dataclass for storing case information."""

    case_id: int
    title: str
    description: str
    instructions: str
    objectives: list
    datasets: list[str]
    level: str
    solution: str
    solved: bool = False

CASES = [
        CaseInfo(
            case_id = 1,
            title="The Vanishing Briefcase",
            description="A briefcase containing sensitive documents has vanished from the Blue Note Lounge. Follow the clues to identify the thief.",
            instructions="Set in the gritty 1980s, a valuable briefcase has disappeared from the Blue Note Lounge. A witness reported that a man in a trench coat was seen fleeing the scene. Investigate the crime scene, review the list of suspects, and examine interview transcripts to reveal the culprit.",
            objectives=[
                "Retrieve the correct crime scene details to gather the key clue.",
                "Identify the suspcet whose profile matches the witness description.",
                "Verify the suspect using their interview transcript."
                ],
            datasets=["crime_scene.csv", "suspects.csv", "interviews.csv"],
            level="Beginner",
            solution="Frankie Lombardi"
            ),

        CaseInfo(
            case_id = 2,
            title="The Stolen Sound",
            description="A prized vinyl record has been stole from West Hollywood Records. Follow the clues to uncever the culprit.",
            instructions="In the neon glow of 1980s Los Angeles, the West Hollywood Records store was rocked by a daring theft. A prized vinyl record, worth over $10,000, vanished during a busy evening, leaving the store owner desperate for answers. Vaguely recalling the details, you know the incident occurred on July 15, 1983, at this famous store. Your task is to track down the thief and bring them to justice.",
            objectives=[
                "Retrieve the crime scene report for the record theft using the known date and location.",
                "Retrieve the witness records linked to that crime scene to obtain their cluse.",
                "Use the clues from the witnesses to find the suspcet in the suspcets table.",
                "Retrieve the suspect's interview transcript to confirm the confession."
                ],
            datasets=["crime_scene.csv", "witnesses.csv", "suspects.csv", "interviews.csv"],
            level="Beginner",
            solution="Rico Delgado"
            ),

        CaseInfo(
            case_id=3,
            title="The Miami Marina Murder",
            description="A body was found at Coral Bay Marina. Two potential suspects were last seen near the scene. Find the murderer and bring them to justice.",
            instructions="A body was found floating near the docks of Coral Bay Marina in the early hours of August 14, 1986. Your job, detective, is to find the murderer and bring them to justice. This case might require the use of JOINs, wildcard searches, and logical deduction. Get to work, detective.",
            objectives=[
                "Find the murderer."
                ],
            datasets=["crime_scene.csv", "person.csv", "interviews.csv", "hotel_checkins.csv", "surveillance_records.csv", "confessions.csv"],
            level="Intermediate",
            solution="Thomas Brown"
            ),
        
        CaseInfo(
            case_id=4,
            title="The Vanishing Diamond",
            description="The famous 'Heart of Atlantis' diamond necklace suddenly disappeared from its display at the charity gala.",
            instructions="At Miami’s prestigious Fontainebleau Hotel charity gala, the famous 'Heart of Atlantis' diamond necklace suddenly disappeared from its display.",
            objectives=[
                "Find who stole the diamond."
                ],
            datasets=[
                "crime_scene.csv",
                "guest.csv",
                "witness_statements.csv",
                "attire_registry.csv",
                "marina_rentals.csv",
                "final_interviews.csv"
                ],
            level="Intermediate",
            solution="Mike Manning"
            ),

        CaseInfo(
            case_id=5,
            title="The Midnight Masquerade Murder",
            description="Leonard Pierce was murdered at a Coconut Grove masked ball. Follow the clues to reveal the true murderer.",
            instructions="On October 31, 1987, at a Coconut Grove mansion masked ball, Leonard Pierce was found dead in the garden. Can you piece together all the clues to expose the true murderer?",
            objectives=[
                "Reveal the true murderer of this complex case."
                ],
            datasets=[
                "crime_scene.csv",
                "person.csv",
                "witness_statements.csv",
                "hotel_checkins.csv",
                "surveillance_records.csv",
                "phone_records.csv",
                "final_interviews.csv",
                "vehicle_registry.csv",
                "catering_orders.csv"
                ],
            level="Advanced",
            solution="Marco Santos"
            ),

        CaseInfo(
            case_id=6,
            title="The Silicon Sabotage",
            description="Miami’s leading tech corporation, was about to unveil its groundbreaking microprocessor. Just hours before the reveal, the prototype was destroyed.",
            instructions="QuantumTech, Miami’s leading technology corporation, was about to unveil its groundbreaking microprocessor called “QuantaX.” Just hours before the reveal, the prototype was destroyed, and all research data was erased. Detectives suspect corporate espionage.",
            objectives=[
                "Find who sabotaged the microprocessor."
                ],
            datasets=[
                "incident_reports.csv",
                "witness_statements.csv",
                "keycard_access_logs.csv",
                "computer_access_logs.csv",
                "email_logs.csv",
                "facility_access_logs.csv",
                "employee_records.csv"
                ],
            level="Advanced",
            solution="Hristo Bogoev"
            ),
        ]
