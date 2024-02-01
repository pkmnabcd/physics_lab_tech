def lon_subfolder(minus_amount):
    """
    Generates the subfolder for changing longitude. If minus_amount > 0, stub is: McMurdo_minus_lon_15#
    :param minus_amount: int number between 0 and 23
    :return: string corresponding to the minus amount inputted
    """
    if minus_amount == 0:
        return "McMurdo"
    else:
        return "McMurdo_minus_lon_15#" + str(minus_amount)


def lat_subfolder(amount, is_plus=True):
    """
    Generates the subfolder for changing latitude. If amount = 0, returns McMurdo_minus_lon_15#20.
    Else, stub is: McMurdo_minus_lon_15#20_plus_lat_5#
    :param is_plus: True for plus, False for minus
    :param amount: int number between 0 and 33
    :return: string corresponding to the amount inputted and if is_plus is true and false
    """
    if amount == 0:
        return "McMurdo_minus_lon_15#20"
    else:
        if is_plus:
            return "McMurdo_minus_lon_15#20_plus_lat_5#" + str(amount)
        else:
            return "McMurdo_minus_lon_15#20_minus_lat_5#" + str(amount)
