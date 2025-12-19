######################################################
############ PLACEHOLDER OCR COUNTY VIEW ############
############## (NON VEDENTI - OCR) ##################
######################################################
# Questo file contiene il CONTENUTO COMPLETO della
# County View in modalità OCR Support originale.
#
# Destinazione tipica di inclusione:
# - come base per ocr_county_view nel file:
#   ocr_support_compatibility_pach/gui/window_county_view.gui
#
# USO CONSIGLIATO:
# - Copia tutto il blocco window = { ... } qui sotto
# - Incollalo al posto del widget "ocr_county_view".
######################################################

window = {
	name = "holding_view"
	widgetid = "holding_view"
	parentanchor = bottom|left
	allow_outside = yes
	movable = no
	layer = windows_layer
	maximumsize = { 700 -1 }
	scissor = yes
	size = { 700 100% }
	datacontext = "[HoldingView.GetProvince]"
	datacontext = "[HoldingView.GetHolding]"
	datacontext = "[HoldingView.GetHolder]"
	datacontext = "[Province.GetCounty]"

	state = {
		name = pan_to_previous_county
		delay = 0.1
		on_start = "[HoldingView.PanToCountyCapital]"
		on_finish = "[PdxGuiTriggerAllAnimations('adjacent_counties')]"
		on_start = "[GetVariableSystem.Clear( 'window_ruins_confirm' )]"
	}

	state = {
		name = _show
		on_start = "[HoldingView.PanToCountyCapital]"
		on_start = "[GetVariableSystem.Set( 'county_view_open', 'true' )]"
		on_start = "[GetVariableSystem.Set( 'hide_bottom_left_HUD', 'true' )]"
		on_finish = "[PdxGuiTriggerAllAnimations('adjacent_counties')]"
		on_start = "[GetVariableSystem.Clear( 'window_ruins_confirm' )]"

		using = Animation_FadeIn_Standard
		using = Sound_WindowShow_Standard
		using = Animation_FadeIn_BottomLeft
	}

	state = {
		name = adjacent_counties
		trigger_on_create = yes
		on_finish = "[Click('reset_lootable_sort')]"
		on_finish = "[GetScriptedGui('province_adjacencies').Execute( GuiScope.SetRoot( Province.MakeScope ).AddScope( 'player', GetPlayer.MakeScope).End )]"
		on_finish = "[PdxGuiTriggerAllAnimations('adjacent_counties_land')]"
	}

	state = {
		name = _hide
		on_start = "[GetVariableSystem.Clear( 'county_view_open' )]"
		on_start = "[GetVariableSystem.Clear( 'hide_bottom_left_HUD' )]"
		on_finish = "[Clear('county_tabs')]"
		on_finish = "[Clear('holding_tabs')]"
		on_finish = "[ClickAdd('last_view', GetPlayer, Province)]"
		on_finish = "[Clear('hide_grant_titles')]"

		using = Animation_FadeOut_Standard
		using = Sound_WindowHide_Standard
		using = Animation_FadeOut_BottomLeft
	}

	widget = {
		size = { 0 0 }
		scissor = yes

		buttons_window_control = {
			blockoverride "button_go_to" {
				onclick = "[HoldingView.PanToCountyCapital]"
			}

			blockoverride "button_back" {
				visible = "[HasViewHistory]"
				onclick = "[OpenFromViewHistory]"
				onclick = "[PdxGuiTriggerAllAnimations('pan_to_previous_county')]"
			}
			blockoverride "button_close" {
				onclick = "[HoldingView.Close]"
			}
		}
	}

	vbox = {
		layoutpolicy_vertical = expanding
		name = "window_content"
		using = ocr_margins
		using = ocr
		background = { using = Background_Area_Border_Solid }

		error_button = {
			layoutpolicy_horizontal = expanding
		}

		vbox = {
			layoutpolicy_horizontal = expanding
			layoutpolicy_vertical = expanding
			visible = "[GetScriptedGui('is_land').IsShown( GuiScope.SetRoot( Province.MakeScope ).End )]"

			state = {
				name = "adjacent_counties_land"
				on_finish = "[GetScriptedGui('adjacent_counties').Execute( GuiScope.SetRoot( HoldingView.GetCountyTitle.MakeScope ).AddScope( 'player', GetPlayer.MakeScope).AddScope('target', HoldingView.GetProvince.MakeScope).End )]"
				on_finish = "[GetScriptedGui('county_holding_list').Execute( GuiScope.SetRoot( HoldingView.GetCountyTitle.MakeScope ).End )]"
				on_finish = "[GetScriptedGui('find_closest').Execute( GuiScope.SetRoot( GetPlayer.MakeScope ).AddScope('target', HoldingView.GetProvince.MakeScope).End )]"
			}

			scrollbox = {
				layoutpolicy_horizontal = expanding
				layoutpolicy_vertical = expanding

				blockoverride "scrollbox_margins" {
					margin_top = 20
				}
				blockoverride "scrollbox_content" {
					# CONTENUTO PRINCIPALE SCROLLBOX
					# Qui andrà tutto il contenuto della county view OCR
					# Vedere il file originale per la struttura completa
					
					vbox = {
						margin_left = 10
						layoutpolicy_horizontal = expanding
						visible = "[Not(GetVariableSystem.Exists('county_tabs'))]"
						
						# Placeholder per il contenuto completo
						# TODO: Inserire qui tutti i vbox/hbox dell'originale
					}
				}
			}

			state = {
				name = holdings_check
				trigger_when = "[IsDataModelEmpty(HoldingView.GetCountyTitle.MakeScope.GetList('county_holdings'))]"
				on_finish = "[GetScriptedGui('county_holding_list').Execute( GuiScope.SetRoot( HoldingView.GetCountyTitle.MakeScope ).End )]"
			}
		}
	}
}
