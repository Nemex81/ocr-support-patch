# ocr-support-patch
patch di compatibilità pe rocr support, mod dedicata a crusader king 3

## Modalità duale edifici (County View)
- **Normovedenti**: se la variabile `ocr` esiste (`GetVariableSystem.Exists('ocr')`) vengono mostrati i sottowindow grafici vanilla per costruzione/upgrade (`holding_tracks_view`, `holding_type_selection_view`).
- **Non vedenti**: se `ocr` non esiste (`Not(GetVariableSystem.Exists('ocr'))`) vengono mostrati i sottowindow OCR/testuali importati da OCR Support.

### Checklist rapida di test manuale
- Aprire la County View.
- Aprire la lista edifici costruibili (stato `Not(HoldingView.IsSelectingBuildingToConstruct)`).
- Aprire il dettaglio/upgrade building track (`HoldingView.IsSelectingBuildingToConstruct`).
- Usare i pulsanti back/close per uscire.
- Confermare che in modalità non vedenti non compaiano elementi grafici vanilla nei flow di build/upgrade.
