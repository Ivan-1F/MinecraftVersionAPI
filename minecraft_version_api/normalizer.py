"""
Normalize Minecraft versions to semver format
Inspired by Fabric Loader
"""
import re


def normalize(version: str) -> str:
    if normalize_special_version(version) is not None:
        return normalize_special_version(version)
    if normalize_snapshot_version(version) is not None:
        return normalize_snapshot_version(version)
    if normalize_pre_release_version(version) is not None:
        return normalize_pre_release_version(version)
    if normalize_release_candidate_version(version) is not None:
        return normalize_release_candidate_version(version)
    if normalize_experimental_snapshot_version(version) is not None:
        return normalize_experimental_snapshot_version(version)
    return version


def normalize_special_version(version: str):
    mapping = {
        "13w12~": "1.5.1-snapshot.13.12.a",  # A pair of debug snapshots immediately before 1.5.1-pre
        "15w14a": "1.8.4-snapshot.15.14.a+loveandhugs",  # The Love and Hugs Update, forked from 1.8.3
        "1.RV-Pre1": "1.9.2-rv+trendy",
        # The Trendy Update, probably forked from 1.9.2 (although the protocoldata versions immediately follow 1.9.1-pre3)
        "3D Shareware v1.34": "1.14-snapshot.19.13.shareware",  # Minecraft 3D, forked from 19w13b
        "20w14~": "1.16-snapshot.20.13.inf",
        # Not to be confused with the actual 20w14a
        # The Ultimate Content update, forked from 20w13b
        "1.14.3 - Combat Test": "1.14.3-rc.4.combat.1",  # The first Combat Test, forked from 1.14.3 Pre-Release 4
        "Combat Test 2": "1.14.5-combat.2",  # The second Combat Test, forked from 1.14.4
        "Combat Test 3": "1.14.5-combat.3",  # The third Combat Test, forked from 1.14.4
        "Combat Test 4": "1.15-rc.3.combat.4",  # The fourth Combat Test, forked from 1.15 Pre-release 3
        "Combat Test 5": "1.15.2-rc.2.combat.5",  # The fifth Combat Test, forked from 1.15.2 Pre-release 2
        "Combat Test 6": "1.16.2-beta.3.combat.6",  # The sixth Combat Test, forked from 1.16.2 Pre-release 3
        "Combat Test 7": "1.16.3-combat.7",  # Private testing Combat Test 7, forked from 1.16.2
        "1.16_combat-2": "1.16.3-combat.7.b",  # Private testing Combat Test 7b, forked from 1.16.2
        "1.16_combat-3": "1.16.3-combat.7.c",  # The seventh Combat Test 7c, forked from 1.16.2
        "1.16_combat-4": "1.16.3-combat.8",  # Private testing Combat Test 8(a?), forked from 1.16.2
        "1.16_combat-5": "1.16.3-combat.8.b",  # The eighth Combat Test 8b, forked from 1.16.2
        "1.16_combat-6": "1.16.3-combat.8.c",  # The ninth Combat Test 8c, forked from 1.16.2
        "22w13oneBlockAtATime": "1.18.2-snapshot.20.13-obaat"
    }
    if version in mapping:
        return mapping[version]
    else:
        return None


def normalize_snapshot_version(version: str):
    def get_snapshot_release(year: int, week: int):
        if year == 22:
            return '1.19'
        elif year == 21 and 37 <= week <= 44:
            return '1.18'
        elif year == 20 and 45 <= week <= 51 or year == 21 and 5 <= week <= 18:
            return '1.17'
        elif year == 20 and 6 <= week <= 30:
            return "1.16"
        elif year == 19 and week >= 34:
            return "1.15"
        elif year == 18 and week >= 43 or year == 19 and week <= 14:
            return "1.14"
        elif year == 18 and 30 <= week <= 33:
            return "1.13.1"
        elif year == 17 and week >= 43 or year == 18 and week <= 22:
            return "1.13"
        elif year == 17 and week == 31:
            return "1.12.1"
        elif year == 17 and 6 <= week <= 18:
            return "1.12"
        elif year == 16 and week == 50:
            return "1.11.1"
        elif year == 16 and 32 <= week <= 44:
            return "1.11"
        elif year == 16 and 20 <= week <= 21:
            return "1.10"
        elif year == 16 and 14 <= week <= 15:
            return "1.9.3"
        elif year == 15 and week >= 31 or year == 16 and week <= 7:
            return "1.9"
        elif year == 14 and 2 <= week <= 34:
            return "1.8"
        elif year == 13 and 47 <= week <= 49:
            return "1.7.4"
        elif year == 13 and 36 <= week <= 43:
            return "1.7.2"
        elif year == 13 and 16 <= week <= 26:
            return "1.6"
        elif year == 13 and 11 <= week <= 12:
            return "1.5.1"
        elif year == 13 and 1 <= week <= 10:
            return "1.5"
        elif year == 12 and 49 <= week <= 50:
            return "1.4.6"
        elif year == 12 and 32 <= week <= 42:
            return "1.4.2"
        elif year == 12 and 15 <= week <= 30:
            return "1.3.1"
        elif year == 12 and 3 <= week <= 8:
            return "1.2.1"
        elif year == 11 and week >= 47 or year == 12 and week <= 1:
            return "1.1"
        return None

    result = re.match(r'(\d\d)w(\d\d)([a-z])', version)
    if result is None:
        return None
    snapshot_year = int(result.group(1))
    snapshot_week = int(result.group(2))
    release = get_snapshot_release(snapshot_year, snapshot_week)
    return '{}-snapshot.{}.{}.{}'.format(release, snapshot_year, snapshot_week, result.group(3))


def normalize_pre_release_version(version: str):
    result = re.match(r'(.*) Pre-release (\d)', version)
    if result is None:
        return None
    release = result.group(1)
    pre = result.group(2)
    return '{}-pre{}'.format(release, pre)


def normalize_release_candidate_version(version: str):
    result = re.match(r'(.*) Release Candidate (\d)', version)
    if result is None:
        return None
    release = result.group(1)
    pre = result.group(2)
    return '{}-rc{}'.format(release, pre)


def normalize_experimental_snapshot_version(version: str):
    result = re.match(r'(.*) Experimental Snapshot (\d)', version)
    if result is None:
        return None
    release = result.group(1)
    pre = result.group(2)
    return '{}-experimental{}'.format(release, pre)


if __name__ == '__main__':
    while True:
        version_name = input('> ')
        print(normalize(version_name))
