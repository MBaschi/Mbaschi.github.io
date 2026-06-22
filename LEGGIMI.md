# Portfolio — Chiara Buscemi (3° anno · 2025/2026)

Portfolio in un unico file **`index.html`**. Apri il file con un doppio clic (o con un
browser: Chrome, Edge, Firefox, Safari). Funziona offline; serve la rete solo per i
font tipografici, che comunque degradano con eleganza se non disponibili.

## Struttura delle cartelle

```
index.html                     ← il portfolio (apri questo)
assets/
  cover/
    copertina.jpg              ← SEGNAPOSTO della copertina (da sostituire)
  lavori/                      ← anteprime sRGB mostrate nel sito (web)
    01-beth-harmon/
    02-cappellaio-matto/
    ...
    19-spot-clio/
  originali-cmyk/              ← MASTER originali per la stampa (NON modificare)
build_assets.py                ← script che rigenera le anteprime dai master
```

- **`assets/lavori/`** contiene le **anteprime di sola visualizzazione**, convertite da
  CMYK a **sRGB** con gestione del colore basata su profili ICC (intent percettivo),
  così che a schermo i colori siano il più fedeli possibile all'intento di stampa.
  Nessuna correzione automatica di luminosità/contrasto/saturazione è stata applicata.
- **`assets/originali-cmyk/`** conserva i **file sorgente intatti** (i master per la
  stampa editoriale). Non vengono mai modificati, ricompressi o sovrascritti. Tienili
  separati dalle anteprime web.

## Come sostituire la copertina

Metti la tua immagine di copertina in `assets/cover/` con il nome **`copertina.jpg`**
(sovrascrivendo il segnaposto). Se il file manca o ha un altro nome, al suo posto
compare un riquadro segnaposto ben visibile.

## Come aggiungere o sostituire le immagini di un lavoro

Le immagini di ogni progetto stanno in `assets/lavori/NN-titolo/`. Per sostituirne una,
salva il nuovo file con **lo stesso nome** già usato nella cartella (es.
`finale.jpg`, `bozza-1.jpg`, `cover.jpg`): il sito la mostrerà automaticamente.

### Lavoro 18 — "Gelateria di Libri"
Le immagini di questo progetto **non erano presenti** nel materiale fornito. Quando le
hai, crea la cartella `assets/lavori/18-gelateria-di-libri/`, inserisci i file e nel
blocco `id="work-18"` di `index.html` sostituisci il riquadro "Immagini da inserire"
con i tag `<img>` (puoi copiare la struttura di un altro lavoro Magazine).

## Rigenerare le anteprime dai master (opzionale)

Se aggiorni i master in `originali-cmyk` (o nella cartella `Immagini/` di origine) puoi
rigenerare le anteprime sRGB con:

```
python -m pip install Pillow pillow-heif PyMuPDF
python build_assets.py            # rigenera anteprime + segnaposto copertina
python build_assets.py --masters  # (ri)crea l'archivio originali-cmyk
```

Lo script: converte CMYK→sRGB via ICC, gestisce HEIC/TIFF, estrae le pagine dai PDF
(es. il quaderno di "Ansia") e copia le GIF stop-motion senza alterarle. Il lato lungo
delle anteprime è limitato a 2500 px mantenendo sempre il rapporto d'aspetto originale.

## Stampa / esportazione in PDF (A4)

Dal browser: **Stampa → Salva come PDF**, formato **A4**. Il foglio di stile include un
`@media print` dedicato: nasconde la navigazione, imposta i margini A4 ed evita che i
blocchi-lavoro vengano spezzati a metà (`break-inside: avoid`). Nello slider B&N→colore,
in stampa le due versioni vengono mostrate una sotto l'altra per intero.

> Suggerimento: nelle opzioni di stampa attiva **"Grafica di sfondo"** per mantenere le
> tinte delle sezioni.

## Funzioni interattive

- **Slider B&N → colore** (Beth Harmon, Cappellaio Matto): trascina il cursore.
- **Mockup**: copertine su mockup di libro, interni su doppia pagina, poster incorniciati.
- **GIF stop-motion** (Un Drago nel Cortile, Eva non si veste): riproduzione automatica in loop.
- **Click su un'immagine**: ingrandimento a schermo intero (lightbox); `Esc` o click per chiudere.
