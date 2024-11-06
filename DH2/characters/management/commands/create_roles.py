from django.core.management.base import BaseCommand
from characters.models import Role, Aptitude

class Command(BaseCommand):
    help = "Creates predefined roles with aptitudes and bonuses"

    def handle(self, *args, **options):
        # Define roles and their attributes
        roles_data = [
            {
                "name": "Assassin (Ballistic Skill)",
                "aptitudes": ["Agility", "Ballistic Skill", "Fieldcraft", "Finesse", "Perception"],
                "role_bonus": "Sure Kill: In addition to the normal uses of Fate points, when an Assassin with Ballistic Skill successfully hits with an attack, he may spend a Fate point to inflict additional damage equal to his degrees of success on the first hit the attack inflicts."
            },
            {
                "name": "Assassin (Weapon Skill)",
                "aptitudes": ["Agility", "Weapon Skill", "Fieldcraft", "Finesse", "Perception"],
                "role_bonus": "Sure Kill: In addition to the normal uses of Fate points, when an Assassin with Weapon Skill successfully hits with an attack, he may spend a Fate point to inflict additional damage equal to his degrees of success on the first hit the attack inflicts."
            },
            {
                "name": "Chirurgeon",
                "aptitudes": ["Fieldcraft", "Intelligence", "Knowledge", "Strength", "Toughness"],
                "role_bonus": "Dedicated Healer: In addition to the normal uses of Fate points, when a Chirurgeon character fails a test to provide First Aid, he can spend a Fate point to automatically succeed instead with the degrees of success equal to his Intelligence bonus."
            },
            {
                "name": "Desperado",
                "aptitudes": ["Agility", "Ballistic Skill", "Defense", "Fellowship", "Finesse"],
                "role_bonus": "Move and Shoot: Once per round, after performing a Move action, a Desperado character may perform a single Standard Attack with a Pistol weapon he is currently wielding as a Free Action."
            },
            {
                "name": "Hierophant",
                "aptitudes": ["Fellowship", "Offence", "Social", "Toughness", "Willpower"],
                "role_bonus": "Sway the Masses: In addition to the normal uses of Fate points, a Hierophant character may spend a Fate point to automatically succeed at a Charm, Command, or Intimidate skill test with a number of degrees of success equal to his Willpower bonus."
            },
            {
                "name": "Mystic",
                "aptitudes": ["Defense", "Intelligence", "Knowledge", "Perception", "Willpower"],
                "role_bonus": "Stare into the Warp: A Mystic character starts the game with the Psyker elite advance. It is recommended that a character who wishes to be a Mystic have a Willpower of at least 35."
            },
            {
                "name": "Sage",
                "aptitudes": ["Intelligence", "Knowledge", "Perception", "Tech", "Willpower"],
                "role_bonus": "Quest for Knowledge: In addition to the normal uses of Fate points, a Sage character may spend a Fate point to automatically succeed at a Logic or any Lore skill test with a number of degrees of success equal to his Intelligence bonus."
            },
            {
                "name": "Seeker",
                "aptitudes": ["Fellowship", "Intelligence", "Perception", "Social", "Tech"],
                "role_bonus": "Nothing Escapes My Sight: In addition to the normal uses of Fate points, a Seeker character may spend a Fate point to automatically succeed at an Awareness or Inquiry skill test with a number of degrees of success equal to his Perception bonus."
            },
            {
                "name": "Warrior",
                "aptitudes": ["Ballistic Skill", "Defense", "Offence", "Strength", "Weapon Skill"],
                "role_bonus": "Expert at Violence: In addition to the normal uses of Fate points, after making a successful attack test, but before determining hits, a Warrior character may spend a Fate point to substitute his Weapon Skill (for melee) or Ballistic Skill (for ranged) bonus for the degrees of success scored on the attack test."
            },
            {
                "name": "Crusader",
                "aptitudes": ["Knowledge", "Offence", "Strength", "Toughness", "Willpower"],
                "role_bonus": "Smite the Unholy: In addition to the normal uses of Fate Points, a Crusader can also spend a Fate Point to automatically pass a Fear test with a DoS equal to his Willpower Bonus. In addition, whenever he inflicts a hit with a melee weapon against a target with the Fear (X) trait, he inflicts X additional damage and counts his weapon's Penetration as being X higher."
            },
            {
                "name": "Fanatic",
                "aptitudes": ["Leadership", "Offence", "Toughness", "Weapon Skill", "Willpower"],
                "role_bonus": "Death to All Who Oppose Me!: In addition to the normal uses of Fate points, a Fanatic character may spend a Fate point to count as having the Hatred talent against his current foe for the duration of the encounter. Should he choose to leave combat against a Hated foe in that encounter, however, he gains 1 Insanity point."
            },
            {
                "name": "Penitent",
                "aptitudes": ["Agility", "Fieldcraft", "Intelligence", "Offence", "Toughness"],
                "role_bonus": "Cleansing Pain: Whenever a Penitent character suffers 1 or more points of damage (after reductions for Toughness bonus and Armour), he gains a +10 bonus to the first test he makes before the end of his next turn."
            },
            {
                "name": "Ace",
                "aptitudes": ["Agility", "Finesse", "Perception", "Tech", "Willpower"],
                "role_bonus": "Right Stuff: In addition to the normal uses of Fate points, an Ace character may spend a Fate point to automatically succeed at an Operate or Survival skill test involving vehicles or living steeds with a number of degrees of success equal to his Agility bonus."
            }
        ]


        for role_data in roles_data:
            # Fetch or create the role object
            role, created = Role.objects.get_or_create(
                name=role_data["name"],
                defaults={"role_bonus": role_data["role_bonus"]}
            )

            # Update the role_bonus if the role already exists but bonus has changed
            if not created and role.role_bonus != role_data["role_bonus"]:
                role.role_bonus = role_data["role_bonus"]
                role.save()
                self.stdout.write(self.style.WARNING(f"Updated role bonus for: {role.name}"))

            # Clear current aptitudes to prevent duplicates and add the new ones
            role.aptitudes.clear()
            for aptitude_name in role_data["aptitudes"]:
                aptitude, _ = Aptitude.objects.get_or_create(name=aptitude_name)
                role.aptitudes.add(aptitude)

            role.save()
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created role: {role.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Role {role.name} already exists and was updated"))

        self.stdout.write(self.style.SUCCESS("Roles creation and update complete"))