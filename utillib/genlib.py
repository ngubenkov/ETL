


def parse_date_YYYY_MM_DD(s):
    import datetime
    d = datetime.date(
        int(s[0:4]),
        int(s[5:7]),
        int(s[8:10])
    )
    return d


def trunc(dt):
    import datetime
    return(datetime.date(dt.year, dt.month, dt.day))