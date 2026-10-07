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

## Controlli

- Muovi un dito sul touchpad per muovere il puntatore.
- Tocca il touchpad o usa il pulsante sinistro per fare clic.
- Usa il pulsante destro per aprire il menu contestuale.
- Trascina due dita sul touchpad per scorrere.
- I pulsanti freccia eseguono piccoli scorrimenti.
- Tocca `Tastiera` in alto per aprire la tastiera virtuale e inviare i tasti al PC.

Premi `Ctrl+C` nel terminale per arrestare il server.
