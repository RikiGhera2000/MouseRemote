# Mouse Remote

Controlla il puntatore del PC Windows dal browser di un iPhone collegato alla stessa rete Wi-Fi.

## Avvio su Windows

Apri PowerShell in questa cartella e installa le dipendenze:

```powershell
py -m pip install -r requirements.txt
```

Avvia il server:

```powershell
py server.py
```

Il terminale mostra l'indirizzo del PC e un QR code. Scansionalo con la fotocamera dell'iPhone e apri il collegamento in Safari. Il primo accesso potrebbe richiedere di consentire Python nella rete privata di Windows.

Se il server era già in esecuzione quando hai aggiornato il codice, fermalo con `Ctrl+C` e riavvialo con `py server.py`. Poi ricarica la pagina in Safari.

## Controlli

- Muovi un dito sul touchpad per muovere il puntatore.
- Tocca il touchpad o usa il pulsante sinistro per fare clic.
- Usa il pulsante destro per aprire il menu contestuale.
- Trascina due dita sul touchpad per scorrere.
- I pulsanti freccia eseguono piccoli scorrimenti.
- Tocca `Tastiera` in alto per aprire la tastiera virtuale: la fila numerica è sempre visibile e `?123` apre i simboli.

Il fail-safe di PyAutoGUI sugli angoli è disattivato, così puoi continuare a controllare il puntatore dal telefono anche quando raggiunge un angolo dello schermo.

Premi `Ctrl+C` nel terminale per arrestare il server.
