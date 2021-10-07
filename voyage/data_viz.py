#formerly graphs.py

scatter_plot_x_vars=[
	'voyage_dates__imp_arrival_at_port_of_dis_year',
	'voyage_dates__length_middle_passage_days',
	'voyage_dates__imp_length_home_to_disembark',
	'voyage_crew__crew_voyage_outset',
	'voyage_crew__crew_first_landing',
	'voyage_slaves_numbers__imp_total_num_slaves_embarked',
	'voyage_slaves_numbers__imp_total_num_slaves_disembarked'
]

scatter_plot_y_vars=[
	'voyage_dates__imp_length_home_to_disembark',
	'voyage_dates__length_middle_passage_days',
	'voyage_ship__tonnage_mod',
	'voyage_crew__crew_voyage_outset',
	'voyage_crew__crew_first_landing',
	'voyage_slaves_numbers__imp_total_num_slaves_embarked',
	'voyage_slaves_numbers__imp_total_num_slaves_disembarked',
	'voyage_slaves_numbers__percentage_men',
	'voyage_slaves_numbers__percentage_women',
	'voyage_slaves_numbers__percentage_boy',
	'voyage_slaves_numbers__percentage_girl',
	'voyage_slaves_numbers__percentage_male',
	'voyage_slaves_numbers__percentage_child',
	'voyage_slaves_numbers__percentage_adult',
	'voyage_slaves_numbers__percentage_female',
	'voyage_slaves_numbers__imp_mortality_ratio',
	'voyage_slaves_numbers__imp_jamaican_cash_price'
]

scatter_plot_factors = [
	'voyage_ship__imputed_nationality',
	'voyage_itinerary__imp_port_voyage_begin',
	'voyage_ship__imputed_nationality'
]

# or should it be something like
#geo_sunburst_keys = [
#'voyage_broadregion__broad_region',
#'voyage_region__region',
#'voyage_place__place'
#]


geo_sunburst_broadregion_vars=[
'voyage_itinerary__imp_broad_region_of_slave_purchase',
'voyage_itinerary__imp_broad_region_slave_dis',
'voyage_itinerary__imp_broad_region_voyage_begin'

]

##SOMETHING IS WRONG WITH voyage_itinerary__broad_region_of_return

geo_sunburst_region_vars = [
'voyage_itinerary__first_landing_region',
'voyage_itinerary__first_region_slave_emb',
'voyage_itinerary__imp_principal_region_of_slave_purchase',
'voyage_itinerary__imp_principal_region_slave_dis',
'voyage_itinerary__imp_region_voyage_begin',
'voyage_itinerary__int_first_region_purchase_slaves',
'voyage_itinerary__int_first_region_slave_landing',
'voyage_itinerary__int_second_place_region_slave_landing',
'voyage_itinerary__int_second_region_purchase_slaves',
'voyage_itinerary__second_landing_region',
'voyage_itinerary__second_region_slave_emb',
'voyage_itinerary__third_landing_region',
'voyage_itinerary__third_region_slave_emb'
]

geo_sunburst_place_vars = [
'voyage_itinerary__first_landing_place',
'voyage_itinerary__first_place_slave_purchase',
'voyage_itinerary__imp_principal_place_of_slave_purchase',
'voyage_itinerary__int_second_place_region_slave_landing',
'voyage_itinerary__principal_place_of_slave_purchase',
'voyage_itinerary__second_landing_place',
'voyage_itinerary__second_place_slave_purchase',
'voyage_itinerary__third_landing_place',
'voyage_itinerary__third_place_slave_purchase'
]


sunburst_plot_values = [
'voyage_dates__length_middle_passage_days',
'voyage_dates__imp_length_home_to_disembark',
'voyage_crew__crew_voyage_outset',
'voyage_crew__crew_first_landing',
'voyage_slaves_numbers__imp_total_num_slaves_embarked',
'voyage_slaves_numbers__imp_total_num_slaves_disembarked',
'voyage_ship__tonnage_mod',
'voyage_slaves_numbers__percentage_men',
'voyage_slaves_numbers__percentage_women',
'voyage_slaves_numbers__percentage_boy',
'voyage_slaves_numbers__percentage_girl',
'voyage_slaves_numbers__percentage_male',
'voyage_slaves_numbers__percentage_child',
'voyage_slaves_numbers__percentage_adult',
'voyage_slaves_numbers__percentage_female',
'voyage_slaves_numbers__imp_mortality_ratio',
'voyage_slaves_numbers__imp_jamaican_cash_price'
]



