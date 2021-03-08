# This is a reduced version; see Kevin's idea about other enumerations
# What about Categories?
# takes 577s to create schema or nearly 10m
# takes ~4s to assert a fact, implying 52hrs to assert equinox!
schema_declarations = {'combine_section_subsection_variable':True,
                       'csv_file':'equinox.csv'}
enumerations = [
    # This is only used in ScopedValue
    ("Confidence", "Confidence Tags", "Tags that can be added to values to indicate confidence in the value of some piece data", [
    ["inferred", "Inferred", "The value has been logically inferred from other evidence"], # This means that if we parse 'inferred present' we need to assert present as value w/ confidence inferred
    ["disputed", "Disputed", "The evidence is disputed - some believe this data to be incorrect"], # for {} values
    # Actually treat suspected like inferred...a type of confidence on, e.g., unknown below
    # uncertain is represented as alternative entries (triples) for the same date or as a numeric range (using a Range type)
    ]),

    # present/absent properties via ScopedEpistemicState
    ("EpistemicState", "Epistemic State", "The existence of a feature in the historical record", [
    ["absent", "Absent", "The feature was absent in this historical context"],
    ["present", "Present", "The feature was present in this historical context"],
    ["unknown", "Unknown", "It can be said with a high degree of confidence that it is not known whether the feature was present or absent in the context."],
    ["suspected_unknown", "Suspected unknown", "An RA asserts that it can be said with a high degree of confidence that it is not known whether the feature was present or absent in the context."],
    ]),
    ]

class_defns = [
    # Must have this since define_seshat_schema.py assumes this as a default domain for all properties
    ("PoliticalAuthority","Political Authority","A human social group with some autonomous political authority.", ["Organization"]),
    ("Polity","Polity","A polity is defined as an independent political unit. Kinds of polities range from villages (local communities) through simple and complex chiefdoms to states and empires. A polity can be either centralized or not (e.g., organized as a confederation). What distinguishes a polity from other human groupings and organizations is that it is politically independent of any overarching authority; it possesses sovereignty. Polities are defined spatially by the area enclosed within a boundary on the world map. There may be more than one such areas. Polities are dynamical entities, and thus their geographical extent may change with time. Thus, typically each polity will be defined by a set of multiple boundaries, each for a specified period of time. For prehistoric periods and for areas populated by a multitude of small-scale polities we use a variant called quasi-polity.",
     ["PoliticalAuthority"]),
    ("QuasiPolity","Quasi-Polity","The polity-based approach is not feasible for those periods when a region is divided up among a multitude of small-scale polities (e.g., independent villages or even many small chiefdoms). In this instance we use the concept of 'quasi-polity'. Similarly, for societies known only archaeologically we may not be able to establish the boundaries of polities, even approximately. Quasi-polity is defined as a cultural area with some degree of cultural homogeneity (including linguistic, if known) that is distinct from surrounding areas. For example, the Marshall Islands before German occupation had no overarching native or colonial authority (chiefs controlled various subsets of islands and atolls) and therefore it was not a polity. But it was a quasi-polity because of the significant cultural and linguistic uniformity.<P>We collect data for the quasi-polity as a whole. This way we can integrate over (often patchy) data from different sites and different polities to estimate what the 'generic' social and political system was like. Data is not entered for the whole region but for a 'typical' polity in it. For example, when coding a quasi-polity, its territory is not the area of the region as a whole, but the average or typical area of autonomous groups within the NGA.",
     ["PoliticalAuthority"]),
    ("Macrostate", "Macrostate","A very large centralized state", ["PoliticalAuthority"]), # Category: Macrostate
    ]

topics = [
    ("GeneralVariables","General variables","",["Topic"]),
    ("InstitutionalVariables","Institutional Variables","",["Topic"]),

    ("ReligionNormativeIdeology","Religion and Normative Ideology","",["Topic"]),
    ("DeificationRulers","Deification of Rulers","",["ReligionNormativeIdeology"]),
    ("MoralizingSupernaturalPowers","Moralizing Supernatural Powers","",["ReligionNormativeIdeology"]),
    ("NormativeIdeologicalAspectsEquityProsociality","Normative Ideological Aspects of Equity and Prosociality","",["ReligionNormativeIdeology"]),

    ("SocialComplexity","Social Complexity variables","",["Topic"]),
    ("BureaucracyCharacteristics","Bureaucracy characteristics","",["SocialComplexity"]),
    ("HierarchicalComplexity","Hierarchical Complexity","",["SocialComplexity"]),
    ("Information","Information","",["SocialComplexity"]),
    ("Law","Law","",["SocialComplexity"]),
    ("Professions","Professions","",["SocialComplexity"]),
    ("SocialScale","Social Scale","",["SocialComplexity"]),
    ("SpecializedBuildings","Specialized Buildings: polity owned","",["SocialComplexity"]),

    ("MacrostateVariables","Macrostate Variables","Information about macrostates",["Topic"]),

    ("WarfareVariables","Warfare Variables","",["Topic"]),
    ("Miltech","Military Technologies","",["WarfareVariables"]),
    ]

# issues: RA is different by 'Topic' which means that the Topics need to be instantiated and associated with a Polity
# this will be the same with Ritual
# GoldHorde: [Polity]
# sections: <sections> # several tuples: GeneralVariables_#55 SocialComplexity_#23

# GeneralVariables_#55 [GeneralVariables]
# applies_to: <GoldenHorde>
# RA: 'DanH'

# SocialComplexity_#23: [SocialComplexity]
# applies_to: <GoldenHorde>
# RA: 'Edward'
# subsections: <subsections> # several tuples BureaucracyCharacteristics_#45

# BureaucracyCharacteristics_#45 [BureaucracyCharacteristics]
# applies_to: <SocialComplexity_#23>!!
# examination_system: 'present'


unscoped_properties = [
    # Must have this for insert_to_csv to find existing Polities using original PolIDs
    ('original_PolID','xsd:string','Original Polity ID','The original name encoding on the wiki, preserving capitalization'),
    ]
# This is a flat version of Equinox: every variable is scoped, they don't involve any Topics (yet)
# and variable property names involve section and subsection and labels involve actual section and subsections
# with |, : and spaces replaced with _
# the 'label' is the text from the csv Section|Subsection|Variable for matching
scoped_properties = [
    ("General_variables__Alternative_names", "String", [], "General variables||Alternative names",""),
    ("General_variables__Capital","String",[],"General variables||Capital",""),
    ("General_variables__Degree_of_centralization","String",[],"General variables||Degree of centralization",""),
    ("General_variables__Duration","GYearRange",[],"General variables||Duration",""),
    ("General_variables__Language","String",[],"General variables||Language",""),
    ("General_variables__Original_name","String",[],"General variables||Original name",""),
    ("General_variables__Peak_Date","GYearRange",[],"General variables||Peak Date",""),
    ("General_variables__RA","String",[],"General variables||RA",""),
    ("General_variables__Supra-polity_relations","String",[],"General variables||Supra-polity relations",""),
    ("General_variables__Supracultural_entity","String",[],"General variables||Supracultural entity",""),
    ("General_variables__preceding_(quasi)polity","String",[],"General variables||preceding (quasi)polity",""),
    ("General_variables__relationship_to_preceding_(quasi)polity","String",[],"General variables||relationship to preceding (quasi)polity",""),
    ("General_variables__scale_of_supra-cultural_interaction","String",[],"General variables||scale of supra-cultural interaction",""),
    ("General_variables__succeeding_(quasi)polity","String",[],"General variables||succeeding (quasi)polity",""),
    ("Institutional_Variables_Limits_on_Power_of_the_Chief_Executive_Constraint_on_executive_by_government","EpistemicState",[],"Institutional Variables|Limits on Power of the Chief Executive|Constraint on executive by government",""),
    ("Institutional_Variables_Limits_on_Power_of_the_Chief_Executive_Constraint_on_executive_by_non-government","EpistemicState",[],"Institutional Variables|Limits on Power of the Chief Executive|Constraint on executive by non-government",""),
    ("Institutional_Variables_Limits_on_Power_of_the_Chief_Executive_Impeachment","EpistemicState",[],"Institutional Variables|Limits on Power of the Chief Executive|Impeachment",""),
    ("Institutional_Variables__RA","String",[],"Institutional Variables||RA",""),
    ("Religion_and_Normative_Ideology_Deification_of_Rulers_Ideological_reinforcement_of_equality","EpistemicState",[],"Religion and Normative Ideology|Deification of Rulers|Ideological reinforcement of equality",""),
    ("Religion_and_Normative_Ideology_Deification_of_Rulers_Ideological_thought_equates_elites_and_commoners","EpistemicState",[],"Religion and Normative Ideology|Deification of Rulers|Ideological thought equates elites and commoners",""),
    ("Religion_and_Normative_Ideology_Deification_of_Rulers_Ideological_thought_equates_rulers_and_commoners","EpistemicState",[],"Religion and Normative Ideology|Deification of Rulers|Ideological thought equates rulers and commoners",""),
    ("Religion_and_Normative_Ideology_Deification_of_Rulers_Rulers_are_gods","EpistemicState",[],"Religion and Normative Ideology|Deification of Rulers|Rulers are gods",""),
    ("Religion_and_Normative_Ideology_Deification_of_Rulers_Rulers_are_legitimated_by_gods","EpistemicState",[],"Religion and Normative Ideology|Deification of Rulers|Rulers are legitimated by gods",""),
    ("Religion_and_Normative_Ideology_Moralizing_Supernatural_Powers_Moral_concern_is_primary","EpistemicState",[],"Religion and Normative Ideology|Moralizing Supernatural Powers|Moral concern is primary",""),
    ("Religion_and_Normative_Ideology_Moralizing_Supernatural_Powers_Moralizing_enforcement_in_afterlife","EpistemicState",[],"Religion and Normative Ideology|Moralizing Supernatural Powers|Moralizing enforcement in afterlife",""),
    ("Religion_and_Normative_Ideology_Moralizing_Supernatural_Powers_Moralizing_enforcement_in_this_life","EpistemicState",[],"Religion and Normative Ideology|Moralizing Supernatural Powers|Moralizing enforcement in this life",""),
    ("Religion_and_Normative_Ideology_Moralizing_Supernatural_Powers_Moralizing_enforcement_is_agentic","EpistemicState",[],"Religion and Normative Ideology|Moralizing Supernatural Powers|Moralizing enforcement is agentic",""),
    ("Religion_and_Normative_Ideology_Moralizing_Supernatural_Powers_Moralizing_enforcement_is_certain","EpistemicState",[],"Religion and Normative Ideology|Moralizing Supernatural Powers|Moralizing enforcement is certain",""),
    ("Religion_and_Normative_Ideology_Moralizing_Supernatural_Powers_Moralizing_enforcement_is_targeted","EpistemicState",[],"Religion and Normative Ideology|Moralizing Supernatural Powers|Moralizing enforcement is targeted",""),
    ("Religion_and_Normative_Ideology_Moralizing_Supernatural_Powers_Moralizing_enforcement_of_rulers","EpistemicState",[],"Religion and Normative Ideology|Moralizing Supernatural Powers|Moralizing enforcement of rulers",""),
    ("Religion_and_Normative_Ideology_Moralizing_Supernatural_Powers_Moralizing_norms_are_broad","EpistemicState",[],"Religion and Normative Ideology|Moralizing Supernatural Powers|Moralizing norms are broad",""),
    ("Religion_and_Normative_Ideology_Moralizing_Supernatural_Powers_Moralizing_religion_adopted_by_commoners","EpistemicState",[],"Religion and Normative Ideology|Moralizing Supernatural Powers|Moralizing religion adopted by commoners",""),
    ("Religion_and_Normative_Ideology_Moralizing_Supernatural_Powers_Moralizing_religion_adopted_by_elites","EpistemicState",[],"Religion and Normative Ideology|Moralizing Supernatural Powers|Moralizing religion adopted by elites",""),
    ("Religion_and_Normative_Ideology_Normative_Ideological_Aspects_of_Equity_and_Prosociality_Ideological_reinforcement_of_equality","EpistemicState",[],"Religion and Normative Ideology|Normative Ideological Aspects of Equity and Prosociality|Ideological reinforcement of equality",""),
    ("Religion_and_Normative_Ideology_Normative_Ideological_Aspects_of_Equity_and_Prosociality_Ideological_thought_equates_elites_and_commoners","EpistemicState",[],"Religion and Normative Ideology|Normative Ideological Aspects of Equity and Prosociality|Ideological thought equates elites and commoners",""),
    ("Religion_and_Normative_Ideology_Normative_Ideological_Aspects_of_Equity_and_Prosociality_Ideological_thought_equates_rulers_and_commoners","EpistemicState",[],"Religion and Normative Ideology|Normative Ideological Aspects of Equity and Prosociality|Ideological thought equates rulers and commoners",""),
    ("Religion_and_Normative_Ideology_Normative_Ideological_Aspects_of_Equity_and_Prosociality_Ideology_reinforces_prosociality","EpistemicState",[],"Religion and Normative Ideology|Normative Ideological Aspects of Equity and Prosociality|Ideology reinforces prosociality",""),
    ("Religion_and_Normative_Ideology_Normative_Ideological_Aspects_of_Equity_and_Prosociality_production_of_public_goods","EpistemicState",[],"Religion and Normative Ideology|Normative Ideological Aspects of Equity and Prosociality|production of public goods",""),
    ("Religion_and_Normative_Ideology_Normative_ideological_Aspects_of_Equity_and_Prosociality_Ideological_reinforcement_of_equality","EpistemicState",[],"Religion and Normative Ideology|Normative ideological Aspects of Equity and Prosociality|Ideological reinforcement of equality",""),
    ("Religion_and_Normative_Ideology_Normative_ideological_Aspects_of_Equity_and_Prosociality_Ideological_thought_equates_elites_and_commoners","EpistemicState",[],"Religion and Normative Ideology|Normative ideological Aspects of Equity and Prosociality|Ideological thought equates elites and commoners",""),
    ("Religion_and_Normative_Ideology_Normative_ideological_Aspects_of_Equity_and_Prosociality_Ideological_thought_equates_rulers_and_commoners","EpistemicState",[],"Religion and Normative Ideology|Normative ideological Aspects of Equity and Prosociality|Ideological thought equates rulers and commoners",""),
    ("Religion_and_Normative_Ideology_Normative_ideological_Aspects_of_Equity_and_Prosociality_Ideology_reinforces_prosociality","EpistemicState",[],"Religion and Normative Ideology|Normative ideological Aspects of Equity and Prosociality|Ideology reinforces prosociality",""),
    ("Religion_and_Normative_Ideology_Normative_ideological_Aspects_of_Equity_and_Prosociality_production_of_public_goods","EpistemicState",[],"Religion and Normative Ideology|Normative ideological Aspects of Equity and Prosociality|production of public goods",""),
    ("Religion_and_Normative_Ideology__RA","String",[],"Religion and Normative Ideology||RA",""),
    ("Social_Complexity_variables_Bureaucracy_characteristics_Examination_system","EpistemicState",[],"Social Complexity variables|Bureaucracy characteristics|Examination system",""),
    ("Social_Complexity_variables_Bureaucracy_characteristics_Full-time_bureaucrats","EpistemicState",[],"Social Complexity variables|Bureaucracy characteristics|Full-time bureaucrats",""),
    ("Social_Complexity_variables_Bureaucracy_characteristics_Merit_promotion","EpistemicState",[],"Social Complexity variables|Bureaucracy characteristics|Merit promotion",""),
    ("Social_Complexity_variables_Bureaucracy_characteristics_Specialized_government_buildings","EpistemicState",[],"Social Complexity variables|Bureaucracy characteristics|Specialized government buildings",""),
    ("Social_Complexity_variables_Hierarchical_Complexity_Administrative_levels","Integer",[],"Social Complexity variables|Hierarchical Complexity|Administrative levels",""),
    ("Social_Complexity_variables_Hierarchical_Complexity_Military_levels","Integer",[],"Social Complexity variables|Hierarchical Complexity|Military levels",""),
    ("Social_Complexity_variables_Hierarchical_Complexity_Religious_levels","Integer",[],"Social Complexity variables|Hierarchical Complexity|Religious levels",""),
    ("Social_Complexity_variables_Hierarchical_Complexity_Settlement_hierarchy","Integer",[],"Social Complexity variables|Hierarchical Complexity|Settlement hierarchy",""),
    ("Social_Complexity_variables_Information_Articles","EpistemicState",[],"Social Complexity variables|Information|Articles",""),
    ("Social_Complexity_variables_Information_Calendar","EpistemicState",[],"Social Complexity variables|Information|Calendar",""),
    ("Social_Complexity_variables_Information_Couriers","EpistemicState",[],"Social Complexity variables|Information|Couriers",""),
    ("Social_Complexity_variables_Information_Fiction","EpistemicState",[],"Social Complexity variables|Information|Fiction",""),
    ("Social_Complexity_variables_Information_Foreign_coins","EpistemicState",[],"Social Complexity variables|Information|Foreign coins",""),
    ("Social_Complexity_variables_Information_General_postal_service","EpistemicState",[],"Social Complexity variables|Information|General postal service",""),
    ("Social_Complexity_variables_Information_History","EpistemicState",[],"Social Complexity variables|Information|History",""),
    ("Social_Complexity_variables_Information_Indigenous_coins","EpistemicState",[],"Social Complexity variables|Information|Indigenous coins",""),
    ("Social_Complexity_variables_Information_Lists_tables_and_classifications","EpistemicState",[],"Social Complexity variables|Information|Lists tables and classifications",""),
    ("Social_Complexity_variables_Information_Mnemonic_devices","EpistemicState",[],"Social Complexity variables|Information|Mnemonic devices",""),
    ("Social_Complexity_variables_Information_Non-phonetic_writing","EpistemicState",[],"Social Complexity variables|Information|Non-phonetic writing",""),
    ("Social_Complexity_variables_Information_Nonwritten_records","EpistemicState",[],"Social Complexity variables|Information|Nonwritten records",""),
    ("Social_Complexity_variables_Information_Paper_currency","EpistemicState",[],"Social Complexity variables|Information|Paper currency",""),
    ("Social_Complexity_variables_Information_Philosophy","EpistemicState",[],"Social Complexity variables|Information|Philosophy",""),
    ("Social_Complexity_variables_Information_Phonetic_alphabetic_writing","EpistemicState",[],"Social Complexity variables|Information|Phonetic alphabetic writing",""),
    ("Social_Complexity_variables_Information_Postal_stations","EpistemicState",[],"Social Complexity variables|Information|Postal stations",""),
    ("Social_Complexity_variables_Information_Practical_literature","EpistemicState",[],"Social Complexity variables|Information|Practical literature",""),
    ("Social_Complexity_variables_Information_Precious_metals","EpistemicState",[],"Social Complexity variables|Information|Precious metals",""),
    ("Social_Complexity_variables_Information_Religious_literature","EpistemicState",[],"Social Complexity variables|Information|Religious literature",""),
    ("Social_Complexity_variables_Information_Sacred_Texts","EpistemicState",[],"Social Complexity variables|Information|Sacred Texts",""),
    ("Social_Complexity_variables_Information_Scientific_literature","EpistemicState",[],"Social Complexity variables|Information|Scientific literature",""),
    ("Social_Complexity_variables_Information_Script","EpistemicState",[],"Social Complexity variables|Information|Script",""),
    ("Social_Complexity_variables_Information_Tokens","EpistemicState",[],"Social Complexity variables|Information|Tokens",""),
    ("Social_Complexity_variables_Information_Written_records","EpistemicState",[],"Social Complexity variables|Information|Written records",""),
    ("Social_Complexity_variables_Law_Courts","EpistemicState",[],"Social Complexity variables|Law|Courts",""),
    ("Social_Complexity_variables_Law_Formal_legal_code","EpistemicState",[],"Social Complexity variables|Law|Formal legal code",""),
    ("Social_Complexity_variables_Law_Judges","EpistemicState",[],"Social Complexity variables|Law|Judges",""),
    ("Social_Complexity_variables_Law_Professional_Lawyers","EpistemicState",[],"Social Complexity variables|Law|Professional Lawyers",""),
    ("Social_Complexity_variables_Professions_Professional_military_officers","EpistemicState",[],"Social Complexity variables|Professions|Professional military officers",""),
    ("Social_Complexity_variables_Professions_Professional_priesthood","EpistemicState",[],"Social Complexity variables|Professions|Professional priesthood",""),
    ("Social_Complexity_variables_Professions_Professional_soldiers","EpistemicState",[],"Social Complexity variables|Professions|Professional soldiers",""),
    ("Social_Complexity_variables_Social_Scale_Polity_Population","DecimalRange",[],"Social Complexity variables|Social Scale|Polity Population",""),
    ("Social_Complexity_variables_Social_Scale_Polity_territory","DecimalRange",[],"Social Complexity variables|Social Scale|Polity territory",""),
    ("Social_Complexity_variables_Social_Scale_Population_of_the_largest_settlement","DecimalRange",[],"Social Complexity variables|Social Scale|Population of the largest settlement",""),
    ("Social_Complexity_variables_Specialized_Buildings__polity_owned_Bridges","EpistemicState",[],"Social Complexity variables|Specialized Buildings: polity owned|Bridges",""),
    ("Social_Complexity_variables_Specialized_Buildings__polity_owned_Canals","EpistemicState",[],"Social Complexity variables|Specialized Buildings: polity owned|Canals",""),
    ("Social_Complexity_variables_Specialized_Buildings__polity_owned_Mines_or_quarries","EpistemicState",[],"Social Complexity variables|Specialized Buildings: polity owned|Mines or quarries",""),
    ("Social_Complexity_variables_Specialized_Buildings__polity_owned_Ports","EpistemicState",[],"Social Complexity variables|Specialized Buildings: polity owned|Ports",""),
    ("Social_Complexity_variables_Specialized_Buildings__polity_owned_Roads","EpistemicState",[],"Social Complexity variables|Specialized Buildings: polity owned|Roads",""),
    ("Social_Complexity_variables_Specialized_Buildings__polity_owned_drinking_water_supply_systems","EpistemicState",[],"Social Complexity variables|Specialized Buildings: polity owned|drinking water supply systems",""),
    ("Social_Complexity_variables_Specialized_Buildings__polity_owned_food_storage_sites","EpistemicState",[],"Social Complexity variables|Specialized Buildings: polity owned|food storage sites",""),
    ("Social_Complexity_variables_Specialized_Buildings__polity_owned_irrigation_systems","EpistemicState",[],"Social Complexity variables|Specialized Buildings: polity owned|irrigation systems",""),
    ("Social_Complexity_variables_Specialized_Buildings__polity_owned_markets","EpistemicState",[],"Social Complexity variables|Specialized Buildings: polity owned|markets",""),
    ("Social_Complexity_variables__RA","String",[],"Social Complexity variables||RA",""),
    ("Social_Mobility_Status_elite_status_is_hereditary","EpistemicState",[],"Social Mobility|Status|elite status is hereditary",""),
    ("Social_Mobility__RA","String",[],"Social Mobility||RA",""),
    ("Warfare_variables_Largest_scale_collective_ritual_of_the_official_cult_Duration","Integer",[],"Warfare variables|Largest scale collective ritual of the official cult|Duration",""),
    ("Warfare_variables_Military_Technologies_Atlatl","EpistemicState",[],"Warfare variables|Military Technologies|Atlatl",""),
    ("Warfare_variables_Military_Technologies_Battle_axes","EpistemicState",[],"Warfare variables|Military Technologies|Battle axes",""),
    ("Warfare_variables_Military_Technologies_Breastplates","EpistemicState",[],"Warfare variables|Military Technologies|Breastplates",""),
    ("Warfare_variables_Military_Technologies_Bronze","EpistemicState",[],"Warfare variables|Military Technologies|Bronze",""),
    ("Warfare_variables_Military_Technologies_Camels","EpistemicState",[],"Warfare variables|Military Technologies|Camels",""),
    ("Warfare_variables_Military_Technologies_Chainmail","EpistemicState",[],"Warfare variables|Military Technologies|Chainmail",""),
    ("Warfare_variables_Military_Technologies_Complex_fortifications","EpistemicState",[],"Warfare variables|Military Technologies|Complex fortifications",""),
    ("Warfare_variables_Military_Technologies_Composite_bow","EpistemicState",[],"Warfare variables|Military Technologies|Composite bow",""),
    ("Warfare_variables_Military_Technologies_Copper","EpistemicState",[],"Warfare variables|Military Technologies|Copper",""),
    ("Warfare_variables_Military_Technologies_Crossbow","EpistemicState",[],"Warfare variables|Military Technologies|Crossbow",""),
    ("Warfare_variables_Military_Technologies_Daggers","EpistemicState",[],"Warfare variables|Military Technologies|Daggers",""),
    ("Warfare_variables_Military_Technologies_Ditch","EpistemicState",[],"Warfare variables|Military Technologies|Ditch",""),
    ("Warfare_variables_Military_Technologies_Dogs","EpistemicState",[],"Warfare variables|Military Technologies|Dogs",""),
    ("Warfare_variables_Military_Technologies_Donkeys","EpistemicState",[],"Warfare variables|Military Technologies|Donkeys",""),
    ("Warfare_variables_Military_Technologies_Earth_ramparts","EpistemicState",[],"Warfare variables|Military Technologies|Earth ramparts",""),
    ("Warfare_variables_Military_Technologies_Elephants","EpistemicState",[],"Warfare variables|Military Technologies|Elephants",""),
    ("Warfare_variables_Military_Technologies_Fortified_camps","EpistemicState",[],"Warfare variables|Military Technologies|Fortified camps",""),
    ("Warfare_variables_Military_Technologies_Gunpowder_siege_artillery","EpistemicState",[],"Warfare variables|Military Technologies|Gunpowder siege artillery",""),
    ("Warfare_variables_Military_Technologies_Handheld_firearms","EpistemicState",[],"Warfare variables|Military Technologies|Handheld firearms",""),
    ("Warfare_variables_Military_Technologies_Helmets","EpistemicState",[],"Warfare variables|Military Technologies|Helmets",""),
    ("Warfare_variables_Military_Technologies_Horses","EpistemicState",[],"Warfare variables|Military Technologies|Horses",""),
    ("Warfare_variables_Military_Technologies_Iron","EpistemicState",[],"Warfare variables|Military Technologies|Iron",""),
    ("Warfare_variables_Military_Technologies_Javelins","EpistemicState",[],"Warfare variables|Military Technologies|Javelins",""),
    ("Warfare_variables_Military_Technologies_Laminar_armor","EpistemicState",[],"Warfare variables|Military Technologies|Laminar armor",""),
    ("Warfare_variables_Military_Technologies_Leather_cloth","EpistemicState",[],"Warfare variables|Military Technologies|Leather cloth",""),
    ("Warfare_variables_Military_Technologies_Limb_protection","EpistemicState",[],"Warfare variables|Military Technologies|Limb protection",""),
    ("Warfare_variables_Military_Technologies_Long_walls","Integer",[],"Warfare variables|Military Technologies|Long walls",""),
    ("Warfare_variables_Military_Technologies_Merchant_ships_pressed_into_service","EpistemicState",[],"Warfare variables|Military Technologies|Merchant ships pressed into service",""),
    ("Warfare_variables_Military_Technologies_Moat","EpistemicState",[],"Warfare variables|Military Technologies|Moat",""),
    ("Warfare_variables_Military_Technologies_Modern_fortifications","EpistemicState",[],"Warfare variables|Military Technologies|Modern fortifications",""),
    ("Warfare_variables_Military_Technologies_Plate_armor","EpistemicState",[],"Warfare variables|Military Technologies|Plate armor",""),
    ("Warfare_variables_Military_Technologies_Polearms","EpistemicState",[],"Warfare variables|Military Technologies|Polearms",""),
    ("Warfare_variables_Military_Technologies_Scaled_armor","EpistemicState",[],"Warfare variables|Military Technologies|Scaled armor",""),
    ("Warfare_variables_Military_Technologies_Self_bow","EpistemicState",[],"Warfare variables|Military Technologies|Self bow",""),
    ("Warfare_variables_Military_Technologies_Settlements_in_a_defensive_position","EpistemicState",[],"Warfare variables|Military Technologies|Settlements in a defensive position",""),
    ("Warfare_variables_Military_Technologies_Shields","EpistemicState",[],"Warfare variables|Military Technologies|Shields",""),
    ("Warfare_variables_Military_Technologies_Sling_siege_engines","EpistemicState",[],"Warfare variables|Military Technologies|Sling siege engines",""),
    ("Warfare_variables_Military_Technologies_Slings","EpistemicState",[],"Warfare variables|Military Technologies|Slings",""),
    ("Warfare_variables_Military_Technologies_Small_vessels_(canoes_etc)","EpistemicState",[],"Warfare variables|Military Technologies|Small vessels (canoes etc)",""),
    ("Warfare_variables_Military_Technologies_Spears","EpistemicState",[],"Warfare variables|Military Technologies|Spears",""),
    ("Warfare_variables_Military_Technologies_Specialized_military_vessels","EpistemicState",[],"Warfare variables|Military Technologies|Specialized military vessels",""),
    ("Warfare_variables_Military_Technologies_Steel","EpistemicState",[],"Warfare variables|Military Technologies|Steel",""),
    ("Warfare_variables_Military_Technologies_Stone_walls_(mortared)","EpistemicState",[],"Warfare variables|Military Technologies|Stone walls (mortared)",""),
    ("Warfare_variables_Military_Technologies_Stone_walls_(non-mortared)","EpistemicState",[],"Warfare variables|Military Technologies|Stone walls (non-mortared)",""),
    ("Warfare_variables_Military_Technologies_Swords","EpistemicState",[],"Warfare variables|Military Technologies|Swords",""),
    ("Warfare_variables_Military_Technologies_Tension_siege_engines","EpistemicState",[],"Warfare variables|Military Technologies|Tension siege engines",""),
    ("Warfare_variables_Military_Technologies_War_clubs","EpistemicState",[],"Warfare variables|Military Technologies|War clubs",""),
    ("Warfare_variables_Military_Technologies_Wood_bark_etc","EpistemicState",[],"Warfare variables|Military Technologies|Wood bark etc",""),
    ("Warfare_variables_Military_Technologies_Wooden_palisades","EpistemicState",[],"Warfare variables|Military Technologies|Wooden palisades",""),
    ("Warfare_variables_Most_dysphoric_collective_ritual_of_the_official_cult_Duration","Integer",[],"Warfare variables|Most dysphoric collective ritual of the official cult|Duration",""),
    ("Warfare_variables_Most_euphoric_collective_ritual_of_the_official_cult_Duration","Integer",[],"Warfare variables|Most euphoric collective ritual of the official cult|Duration",""),
    ("Warfare_variables_Most_frequent_collective_ritual_of_the_official_cult_Duration","Integer",[],"Warfare variables|Most frequent collective ritual of the official cult|Duration",""),
    ("Warfare_variables_Most_widespread_collective_ritual_of_the_official_cult_Duration","Integer",[],"Warfare variables|Most widespread collective ritual of the official cult|Duration",""),
    # Note that these are duplicates under Warfare variables|Military Technologies above!  fix the wiki?
    ("Warfare_variables__Atlatl","EpistemicState",[],"Warfare variables||Atlatl",""),
    ("Warfare_variables__Battle_axes","EpistemicState",[],"Warfare variables||Battle axes",""),
    ("Warfare_variables__Breastplates","EpistemicState",[],"Warfare variables||Breastplates",""),
    ("Warfare_variables__Bronze","EpistemicState",[],"Warfare variables||Bronze",""),
    ("Warfare_variables__Camels","EpistemicState",[],"Warfare variables||Camels",""),
    ("Warfare_variables__Chainmail","EpistemicState",[],"Warfare variables||Chainmail",""),
    ("Warfare_variables__Complex_fortifications","EpistemicState",[],"Warfare variables||Complex fortifications",""),
    ("Warfare_variables__Composite_bow","EpistemicState",[],"Warfare variables||Composite bow",""),
    ("Warfare_variables__Copper","EpistemicState",[],"Warfare variables||Copper",""),
    ("Warfare_variables__Crossbow","EpistemicState",[],"Warfare variables||Crossbow",""),
    ("Warfare_variables__Daggers","EpistemicState",[],"Warfare variables||Daggers",""),
    ("Warfare_variables__Dogs","EpistemicState",[],"Warfare variables||Dogs",""),
    ("Warfare_variables__Donkeys","EpistemicState",[],"Warfare variables||Donkeys",""),
    ("Warfare_variables__Elephants","EpistemicState",[],"Warfare variables||Elephants",""),
    ("Warfare_variables__Gunpowder_siege_artillery","EpistemicState",[],"Warfare variables||Gunpowder siege artillery",""),
    ("Warfare_variables__Handheld_firearms","EpistemicState",[],"Warfare variables||Handheld firearms",""),
    ("Warfare_variables__Helmets","EpistemicState",[],"Warfare variables||Helmets",""),
    ("Warfare_variables__Horses","EpistemicState",[],"Warfare variables||Horses",""),
    ("Warfare_variables__Iron","EpistemicState",[],"Warfare variables||Iron",""),
    ("Warfare_variables__Javelins","EpistemicState",[],"Warfare variables||Javelins",""),
    ("Warfare_variables__Laminar_armor","EpistemicState",[],"Warfare variables||Laminar armor",""),
    ("Warfare_variables__Leather_cloth","EpistemicState",[],"Warfare variables||Leather cloth",""),
    ("Warfare_variables__Limb_protection","EpistemicState",[],"Warfare variables||Limb protection",""),
    ("Warfare_variables__Long_walls","EpistemicState",[],"Warfare variables||Long walls",""),
    ("Warfare_variables__Merchant_ships_pressed_into_service","EpistemicState",[],"Warfare variables||Merchant ships pressed into service",""),
    ("Warfare_variables__Moat","EpistemicState",[],"Warfare variables||Moat",""),
    ("Warfare_variables__Modern_fortifications","EpistemicState",[],"Warfare variables||Modern fortifications",""),
    ("Warfare_variables__Plate_armor","EpistemicState",[],"Warfare variables||Plate armor",""),
    ("Warfare_variables__Polearms","EpistemicState",[],"Warfare variables||Polearms",""),
    ("Warfare_variables__RA","EpistemicState",[],"Warfare variables||RA",""),
    ("Warfare_variables__Scaled_armor","EpistemicState",[],"Warfare variables||Scaled armor",""),
    ("Warfare_variables__Self_bow","EpistemicState",[],"Warfare variables||Self bow",""),
    ("Warfare_variables__Settlements_in_a_defensive_position","EpistemicState",[],"Warfare variables||Settlements in a defensive position",""),
    ("Warfare_variables__Shields","EpistemicState",[],"Warfare variables||Shields",""),
    ("Warfare_variables__Sling_siege_engines","EpistemicState",[],"Warfare variables||Sling siege engines",""),
    ("Warfare_variables__Slings","EpistemicState",[],"Warfare variables||Slings",""),
    ("Warfare_variables__Small_vessels_(canoes_etc)","EpistemicState",[],"Warfare variables||Small vessels (canoes etc)",""),
    ("Warfare_variables__Spears","EpistemicState",[],"Warfare variables||Spears",""),
    ("Warfare_variables__Specialized_military_vessels","EpistemicState",[],"Warfare variables||Specialized military vessels",""),
    ("Warfare_variables__Steel","EpistemicState",[],"Warfare variables||Steel",""),
    ("Warfare_variables__Stone_walls_(mortared)","EpistemicState",[],"Warfare variables||Stone walls (mortared)",""),
    ("Warfare_variables__Stone_walls_(non-mortared)","EpistemicState",[],"Warfare variables||Stone walls (non-mortared)",""),
    ("Warfare_variables__Swords","EpistemicState",[],"Warfare variables||Swords",""),
    ("Warfare_variables__Tension_siege_engines","EpistemicState",[],"Warfare variables||Tension siege engines",""),
    ("Warfare_variables__War_clubs","EpistemicState",[],"Warfare variables||War clubs",""),
    ("Warfare_variables__Wood_bark_etc","EpistemicState",[],"Warfare variables||Wood bark etc",""),
    ]
