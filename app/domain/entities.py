# Κανόνες και οντότητες ανεξάρτητες από βάση.



from dataclasses import dataclass


@dataclass(frozen=True)
class Member:
    first_name: str
    last_name: str
    address: str
    organization_duty: str
    rank: str
    phone_number: str
    group_id: int

    def validate(self) -> None:
        fields = {
            "Όνομα": self.first_name,
            "Επώνυμο": self.last_name,
            "Διεύθυνση": self.address,
            "Καθήκον": self.organization_duty,
            "Βαθμός": self.rank,
            "Τηλέφωνο επικοινωνίας": self.phone_number,
        }
        for label, value in fields.items():
            if not value or not value.strip():
                raise ValueError(f"Το πεδίο «{label}» είναι υποχρεωτικό.")
        if not self.phone_number.replace("+", "").replace(" ", "").replace("-", "").isdigit():
            raise ValueError("Ο αριθμός επικοινωνίας δεν είναι έγκυρος.")


@dataclass(frozen=True)
class Group:
    name: str
    description: str | None = None

    def validate(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Το όνομα της ομάδας είναι υποχρεωτικό.")
