
"""This service helps the table management, with fix and or calculated values"""

USER_ENTERED = "USER_ENTERED"

INSERT_ROWS = "INSERT_ROWS"

"""Major Dimensions"""
MD_ROWS = "ROWS"
MD_COLUMNS = "COLUMNS"

"""Value Render Options"""
VRO_FORMATTED_VALUE = "FORMATTED_VALUE"    # Use as default
VRO_UNFORMATTED_VALUE = "UNFORMATTED_VALUE"

"""Date Time Option"""
DATE_FORMATTED_STRING = "FORMATTED_STRING"


def calc_range():
    """Table range (table width)
    :return: String table_range"""

    # Temporarily solution is to provide the whole table width
    # It works without any error
    return 'A1:Z1'
