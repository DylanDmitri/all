
neutrals = dict(
    kobold            =dict(gold=( 6, 8), xp=20),
    kobold_soldier    =dict(gold=(14,18), xp=20),
    kobold_foreman    =dict(gold=(20,25), xp=33),
    hill_troll        =dict(gold=(20,24), xp=33),
    hill_troll_priest =dict(gold=(19,22), xp=33),
    vhoul_assassin    =dict(gold=(20,24), xp=33),
    ghost             =dict(gold=(28,34), xp=50),
    fell_spirit       =dict(gold=(17,20), xp=33),
    harpy_scout       =dict(gold=(21,24), xp=33),
    harpy_stormcrafter=dict(gold=(29,33), xp=50),

    centaur_large     =dict(gold=(53,62), xp=95),
    centaur_small     =dict(gold=(16,19), xp=30),
    wolf_small        =dict(gold=(18,21), xp=50),
    wolf_large        =dict(gold=(30,36), xp=70),
    satyr_small       =dict(gold=(12,14), xp=33),
    satyr_medium      =dict(gold=(22,26), xp=50),
    satyr_large       =dict(gold=(62,73), xp=95),
    ogre_orange       =dict(gold=(18,38), xp=33),
    ogre_frost        =dict(gold=(28,36), xp=50),
    golem_mud         =dict(gold=(24,27), xp=34),
    golem_shard       =dict(gold=( 8,13), xp=18),

    hellbear_potato   =dict(gold=(36,44), xp=70),
    hellbear_tomato   =dict(gold=(61,70), xp=95),
    wildwing_small    =dict(gold=(12,16), xp=20),
    wildwing_large    =dict(gold=(54,70), xp=90),

    troll_small       =dict(gold=(21,26), xp=50),
    troll_large       =dict(gold=(43,50), xp=95),
    skeleton_warrior  =dict(gold=( 6,12), xp=12),

    l_melee           =dict(gold=(34,38), xp=40),
    l_ranged          =dict(gold=(42,48), xp=90),
    l_catapult        =dict(gold=(66,80), xp=88),
    l_melee_super     =dict(gold=(16,24), xp=25),
    l_ranged_super    =dict(gold=(18,26), xp=25),
    l_melee_mega      =dict(gold=(16,24), xp=25),
    l_ranged_mega     =dict(gold=(18,26), xp=25),
)


chop = lambda n: "{:.2f}".format(n).rjust(6)

def toGPM(v):
    return 60*((200-v)/100)

for d in neutrals.values():
    d['gpm'] = 200-(sum(d['gold'])/2)
    d['xpm'] = (d['xp']*0.85)

for k, v in neutrals.items():
    print(k, chop(v['gpm']), chop(v['xpm']), sep='\t')
