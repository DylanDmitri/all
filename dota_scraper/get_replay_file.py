import dota2api
api = dota2api.Initialise("D7E45FFEB492E701B53D6920C2AE960D")

# http://replay224.valve.net/570/3070331101_298785994.dem.bz2

def getReplay(id):
    return replay(matchInfo(id))

def matchInfo(id):
    s = api.get_match_details(id)
    print(s)
    return dict(
        cluster = s.cluster,
        match_id = s.match_id,
        salt = s
    )

# "http://replay" + match.cluster + ".valve.net/570/" + match.match_id + "_" + match.replay_salt + ".dem.bz2?v=1"
# http://replay133.valve.net/570/3077416603_1375684498.dem.bz2
# http://replay{cluster_num}.valve.net/{?}/{match_id}_{

matchInfo(3077416603)
