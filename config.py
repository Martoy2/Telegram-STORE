TOKEN = "TELEGRAM TOKEN"

admins = "id admin"

managers = "id manager"

QIWI = "QIWI API Token"


steam_auto=False
gplay_auto=False

#цены
def get_price():
    file1 = open("price.cfg", "r")
    price=file1.readlines()
    for line in price:
        if "basic_moth" in line:
            basic_moth = line.split("=")[1]
            basic_moth = basic_moth.replace("\n", "").replace("\r", "")
        elif "basic_year" in line:
            basic_year = line.split("=")[1]
            basic_year = basic_year.replace("\n", "").replace("\r", "")
        elif "full_moth" in line:
            full_moth = line.split("=")[1]
            full_moth = full_moth.replace("\n", "").replace("\r", "")
        elif "full_year" in line:
            full_year = line.split("=")[1]
            full_year = full_year.replace("\n", "").replace("\r", "")
        elif "xbox_lifetime" in line:
            xbox_lifetime = line.split("=")[1]
            xbox_lifetime = xbox_lifetime.replace("\n", "").replace("\r", "")
        elif "steam_rg" in line:
            steam_rg = line.split("=")[1]
            steam_rg = steam_rg.replace("\n", "").replace("\r", "")
        elif "steam_20" == line.split("=")[0]:
            steam_20 = line.split("=")[1]
            steam_20 = steam_20.replace("\n", "").replace("\r", "")
        elif "steam_50" in line:
            steam_50 = line.split("=")[1]
            steam_50 = steam_50.replace("\n", "").replace("\r", "")
        elif "steam_100" in line:
            steam_100 = line.split("=")[1]
            steam_100 = steam_100.replace("\n", "").replace("\r", "")
        elif "steam_200" == line.split("=")[0]:
            steam_200 = line.split("=")[1]
            steam_200 = steam_200.replace("\n", "").replace("\r", "")
        elif "gplay_25" == line.split("=")[0]:
            gplay_25 = line.split("=")[1]
            gplay_25 = gplay_25.replace("\n", "").replace("\r", "")
        elif "gplay_50" == line.split("=")[0]:
            gplay_50 = line.split("=")[1]
            gplay_50 = gplay_50.replace("\n", "").replace("\r", "")
        elif "gplay_100" == line.split("=")[0]:
            gplay_100 = line.split("=")[1]
            gplay_100 = gplay_100.replace("\n", "").replace("\r", "")
        elif "gplay_250" == line.split("=")[0]:
            gplay_250 = line.split("=")[1]
            gplay_250 = gplay_250.replace("\n", "").replace("\r", "")
        elif "gplay_500" == line.split("=")[0]:
            gplay_500 = line.split("=")[1]
            gplay_500 = gplay_500.replace("\n", "").replace("\r", "")
        elif "gplay_1000" == line.split("=")[0]:
            gplay_1000 = line.split("=")[1]
            gplay_1000 = gplay_1000.replace("\n", "").replace("\r", "")

    d=dict()
    d["basic_moth"]=basic_moth
    d["basic_year"]=basic_year
    d["full_moth"]=full_moth
    d["full_year"]=full_year
    d["xbox_lifetime"]=xbox_lifetime
    d["steam_rg"]=steam_rg
    d["steam_20"]=steam_20
    d["steam_50"]=steam_50
    d["steam_100"]=steam_100
    d["steam_200"]=steam_200
    d["gplay_25"]=gplay_25
    d["gplay_50"]=gplay_50
    d["gplay_100"]=gplay_100
    d["gplay_250"]=gplay_250
    d["gplay_500"]=gplay_500
    d["gplay_1000"]=gplay_1000
    return d
