import uuid
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Any, Optional, Dict
from faker import Faker
import random


fake = Faker()


@dataclass
class Classifications:
    """
        Data class representing a Classification.

        Attributes:
            uuid (str): The unique id for Classification.
            classificationUid (int): The ID for Classification.
            subclassificationUid (int): The ID for Sub-Classification.
            classificationLabel (str): The Classification label.
            verificationFieldUid (int): The verification field ID.
            verificationFieldLabel (str): The verification field label.
            isActive (bool): Whether the Classification is active or not.
            isDeleted (bool): Whether the Classification is deleted or not.

        Methods:
            generate_classification: Generates a sample Classification object with random attributes.

        """

    uuid: str
    classificationUid: int
    subclassificationUid: int
    classificationLabel: str
    verificationFieldUid: int
    verificationFieldLabel: str
    isActive: bool
    isDeleted: bool

    @classmethod
    def generate_classification(cls) -> 'Classifications':
        """Generate sample classification object
        :return: Classifications
        """

        return Classifications(
            uuid=str(uuid.uuid4()),
            classificationUid=random.randint(1, 100),
            subclassificationUid=random.randint(1, 100),
            classificationLabel=fake.company()[:10],
            verificationFieldUid=random.randint(1, 100),
            verificationFieldLabel=fake.company()[:10],
            isActive=random.choice([True, False]),
            isDeleted=random.choice([True, False])
        )


@dataclass
class Group:
    """
    Data class representing a group.

    Attributes:
        customerId (int): The ID of the customer associated with the group.
        name (str): The name of the group.
        description (str): The description of the group.
        classifications (List[Classifications]): A list of Classification object
        customGroups (List[Any]): A list of custom groups associated with the group.
        isActive (bool): Whether the group is active or not.
        isDeleted (bool): Whether the group is deleted or not.

    Methods:
        generate_base_group: Generates a base group object(as dict if specified) with random attributes.
        generate_full_group: Generates a full group object(as dict if specified) with random attributes.

    """

    customerId: int = None
    name: str = None
    description: Optional[str] = None
    classifications: Optional[List[Classifications]] = None
    customGroups: Optional[List[str]] = None
    isActive: Optional[bool] = None
    isDeleted: Optional[bool] = None

    @staticmethod
    def generate_base_group(customer_id: Optional[int], as_json: Optional[bool] = False ) -> 'Group' or Dict[str, Any]:
        """
        Generate a base group object with random attributes.

        :param as_json:
            optional (bool)default is False, if user wants to return as dict can set to True
        :param customer_id:
            (int): The ID of the customer associated with the group.

        :return:
            depending on as_json is True or False will return Group obj or Group obj as dict
        """
        name = "Group " + f"{fake.uuid4()[:5]}"
        description = fake.text(max_nb_chars=200)
        customer_id = customer_id if customer_id else 208230
        custom_groups = [fake.word() for _ in range(random.randint(1, 5))]
        is_active = random.choice([True, False])
        is_deleted = random.choice([True, False])

        group = Group(
            customerId=customer_id,
            name=name,
            description=description,
            customGroups=custom_groups,
            isActive=is_active,
            isDeleted=is_deleted
        )

        if as_json:
            return asdict(group)

        return group

    @classmethod
    def generate_full_group(cls, customer_id: Optional[int] = None, as_json: Optional[bool] = False) -> 'Group' or Dict[str, Any]:
        """
        Generate full group object
        :param customer_id:
            optional (int) customer id, if not set used default customer id 208230
        :param as_json:
            optional (bool) default is False, if user wants to return as dict can set to True
        :return:
            depending on as_json is True or False will return Group obj or Group obj as dict
        """

        customer_id = customer_id if customer_id else 208230
        name = fake.company()
        description = fake.text(max_nb_chars=200)
        classifications = [Classifications.generate_classification() for _ in range(2)]
        custom_groups = [fake.word() for _ in range(random.randint(1, 5))]
        is_active = random.choice([True, False])
        is_deleted = random.choice([True, False])

        group = Group(
            customerId=customer_id,
            name=name,
            description=description,
            classifications=classifications,
            customGroups=custom_groups,
            isActive=is_active,
            isDeleted=is_deleted,
        )

        if as_json:
            return asdict(group)

        return group
