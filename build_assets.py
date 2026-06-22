# -*- coding: utf-8 -*-
"""
Build pipeline per il portfolio di Chiara Buscemi.
- Conserva i master CMYK intatti in assets/originali-cmyk/
- Genera anteprime sRGB (gestione colore via profili ICC, intent percettivo)
- Converte HEIC/TIFF/PDF, copia le GIF senza alterarle
Nessuna correzione automatica di luminosita/contrasto/saturazione.
"""
import os, io, shutil, sys
from PIL import Image, ImageCms, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS = None
import pillow_heif; pillow_heif.register_heif_opener()
import fitz  # PyMuPDF

SRC = "Immagini"
LAV = "assets/lavori"
ORIG = "assets/originali-cmyk"
COVER = "assets/cover"
MAXSIDE = 2500
Q = 88

srgb = ImageCms.createProfile("sRGB")

def srgbify(im):
    """Converte in sRGB rispettando il profilo ICC incorporato, intent percettivo."""
    icc = im.info.get("icc_profile")
    mode = im.mode
    if mode == "RGBA":
        if icc:
            try:
                src = ImageCms.ImageCmsProfile(io.BytesIO(icc))
                rgb = ImageCms.profileToProfile(im.convert("RGB"), src, srgb,
                                                renderingIntent=0, outputMode="RGB")
                rgb.putalpha(im.getchannel("A"))
                return rgb
            except Exception:
                pass
        return im
    if icc and mode in ("CMYK", "RGB"):
        try:
            return ImageCms.profileToProfile(im, src=ImageCms.ImageCmsProfile(io.BytesIO(icc)),
                                             dst=srgb, renderingIntent=0, outputMode="RGB")
        except Exception:
            pass
    return im.convert("RGB")

def save_preview(im, dest):
    """Salva l'anteprima ridimensionando solo se piu grande di MAXSIDE (aspect ratio intatto)."""
    w, h = im.size
    if max(w, h) > MAXSIDE:
        im.thumbnail((MAXSIDE, MAXSIDE), Image.LANCZOS)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if dest.lower().endswith(".png"):
        im.save(dest, "PNG", optimize=True)
    else:
        im.convert("RGB").save(dest, "JPEG", quality=Q, progressive=True)

def conv(src_rel, dest_rel):
    src = os.path.join(SRC, src_rel)
    dest = os.path.join(LAV, dest_rel)
    if not os.path.exists(src):
        print("  !! MANCA:", src); return
    im = srgbify(Image.open(src))
    save_preview(im, dest)
    print("   ok", dest_rel, im.size)

def conv_pdf(src_rel, page, dest_rel, zoom=2.0):
    src = os.path.join(SRC, src_rel)
    dest = os.path.join(LAV, dest_rel)
    if not os.path.exists(src):
        print("  !! MANCA:", src); return
    doc = fitz.open(src)
    pix = doc[page].get_pixmap(matrix=fitz.Matrix(zoom, zoom))
    im = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
    save_preview(im, dest)
    print("   ok(pdf)", dest_rel, im.size)

def copy_raw(src_rel, dest_rel):
    src = os.path.join(SRC, src_rel)
    dest = os.path.join(LAV, dest_rel)
    if not os.path.exists(src):
        print("  !! MANCA:", src); return
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copy2(src, dest)
    print("   copy", dest_rel)

# ---------------------------------------------------------------- MANIFEST
JOBS = {
"01-beth-harmon": [
    ("01_BethHarmon/PitturaB&N_ChiaraBuscemi_01.jpg", "bn.jpg"),
    ("01_BethHarmon/PitturaColori_ChiaraBuscemi_01.jpg", "colore.jpg"),
    ("01_BethHarmon/BethHarmon_ bozza.jpg", "bozza-1.jpg"),
],
"02-cappellaio-matto": [
    ("02_TheMadHatter/PitturaB&N_ChiaraBuscemi_02.jpg", "bn.jpg"),
    ("02_TheMadHatter/PitturaColori_ChiaraBuscemi_02.jpg", "colore.jpg"),
    ("02_TheMadHatter/TheMadHatter_bozza.jpg", "bozza-1.jpg"),
],
"03-halloween": [
    ("03_Halloween/ChiaraBuscemi_06.jpg", "finale.jpg"),
],
"04-bambina-dombra": [
    ("04_Bambinad'ombra/Cover/ChiaraBuscemi_Cover_02.jpg", "cover.jpg"),
    ("04_Bambinad'ombra/Capurela/ChiaraBuscemi_Capurela_Colori_02.jpg", "interno-1-capulera.jpg"),
    ("04_Bambinad'ombra/Casa/ChiaraBuscemi_Casa_01.jpg", "interno-2-casa.jpg"),
    ("04_Bambinad'ombra/Rientro Osteria/ChiaraBuscemi_Rientroall'osteria_01.jpg", "interno-3-locanda.jpg"),
    ("04_Bambinad'ombra/Cover/Bozze/ChiaraBuscemi_Cover_R_v01.jpg", "bozza-1.jpg"),
    ("04_Bambinad'ombra/Capurela/Bozze/Capurela_R_v01.JPG", "bozza-2.jpg"),
    ("04_Bambinad'ombra/Altre Bozze Interni/03_ChiaraBuscemi_Paesaggio_R_v01.JPG", "bozza-3.jpg"),
    ("04_Bambinad'ombra/Altre Bozze Interni/04_ChiaraBuscemi_Osteria_R_v01.JPG", "bozza-4.jpg"),
],
"05-fuga-di-logan": [
    ("05_LaFugadiLogan/ChiaraBuscemi_v01.02.jpg", "versione-1.jpg"),
    ("05_LaFugadiLogan/ChiaraBuscemi_v02.02.jpg", "versione-2.jpg"),
    ("05_LaFugadiLogan/01-bozze-versione-1/01.jpg", "1-bozze-versione-1/1.jpg"),
    ("05_LaFugadiLogan/01-bozze-versione-1/ChiaraBuscemi_R_V03_3.JPG", "1-bozze-versione-1/2.jpg"),
    ("05_LaFugadiLogan/01-bozze-versione-1/ChiaraBuscemi_R_V03_1.jpg", "1-bozze-versione-1/3.jpg"),
    ("05_LaFugadiLogan/01-bozze-versione-1/ChiaraBuscemi_R_V03_2.jpg", "1-bozze-versione-1/4.jpg"),
    ("05_LaFugadiLogan/02-bozze-versione-2/ChiaraBuscemi_v02.01.jpg", "2-bozze-versione-2/bozza-1.jpg"),
    ("05_LaFugadiLogan/03-altre-Bozze/ChiaraBuscemi_R_v01.jpg", "3-altre-bozze/bozza-1.jpg"),
    ("05_LaFugadiLogan/03-altre-Bozze/ChiaraBuscemi_R_v02.jpg", "3-altre-bozze/bozza-2.jpg"),
    ("05_LaFugadiLogan/03-altre-Bozze/ChiaraBuscemi_R_v04.JPG", "3-altre-bozze/bozza-3.jpg"),
],
"06-simbiosi": [
    ("06_ Simbisi/ChiaraBuscemi_Simbiosi.jpg", "finale.jpg"),
    ("06_ Simbisi/ChiaraBuscemi_Simbiosi_R_v01.jpg", "bozza-1.jpg"),
],
"07-rise-caffe": [
    ("07_RISE — Packagingcaffè/ChiaraBuscemi_Rise_Mockup.jpg", "mockup.jpg"),
    ("07_RISE — Packagingcaffè/ChiaraBuscemi_Rise_01.jpg", "miscela-1.jpg"),
    ("07_RISE — Packagingcaffè/ChiaraBuscemi_Rise_02.jpg", "miscela-2.jpg"),
    ("07_RISE — Packagingcaffè/ChiaraBuscemi_Rise_03.jpg", "miscela-3.jpg"),
    ("07_RISE — Packagingcaffè/ChiaraBuscemi_Rise_R_v01.jpg", "bozza-1.jpg"),
],
"08-casa-in-fondo-alla-strada": [
    ("08_LaCasainFondoallaStrada/ChiaraBuscemi_V01.jpg", "finale.jpg"),
    ("08_LaCasainFondoallaStrada/Bozze/ChiaraBuscemi_R_v01.jpg", "bozza-1.jpg"),
],
"09-un-nuovo-inizio": [
    ("09_UnNuovoInizio/ChiaraBuscemi_v01.jpg", "finale.jpg"),
    ("09_UnNuovoInizio/Bozze/ChiaraBuscemi_R_v05.jpg", "1-bozze/1.jpg"),
    ("09_UnNuovoInizio/Bozze/ChiaraBuscemi_BiancoeNero_v01.jpg", "1-bozze/2.jpg"),
    ("09_UnNuovoInizio/Bozze/ChiaraBuscemi_v01.jpg", "1-bozze/3.jpg"),
    ("09_UnNuovoInizio/Bozze/ChiaraBuscemi_ProvaColore_v01.jpg", "1-bozze/4.jpg"),
    ("09_UnNuovoInizio/Bozze/ChiaraBuscemi_ProvaColore_v02.jpg", "1-bozze/5.jpg"),
    ("09_UnNuovoInizio/altre-bozze/ChiaraBuscemi_R_v02.jpg", "2-altre-bozze/1.jpg"),
    ("09_UnNuovoInizio/altre-bozze/ChiaraBuscemi_R_v03.jpg", "2-altre-bozze/2.jpg"),
],
"10-eclissi-al-sipario": [
    ("10_EclissiAlSipario/ClownSilente/03_ChiaraBuscemi_Personaggio_BN_v03.jpg", "clown-illustrazione.jpg"),
    ("10_EclissiAlSipario/ClownSilente/03_ChiaraBuscemi_Personaggio_Carta_v01.png", "clown-carta.png"),
    ("10_EclissiAlSipario/ClownSilente/03_ChiaraBuscemi_Personaggio_M3D_v02.png", "clown-3d.png"),
    ("10_EclissiAlSipario/ViolinoScordato/04_ChiaraBuscemi_Oggetto_BN_v02 .jpg", "violino-illustrazione.jpg"),
    ("10_EclissiAlSipario/ViolinoScordato/04_ChiaraBuscemi_Oggetto_Carta_v01.png", "violino-carta.png"),
    ("10_EclissiAlSipario/ViolinoScordato/04_ChiaraBuscemi_Oggetto_M3D_v01.png", "violino-3d.png"),
    ("10_EclissiAlSipario/SaladegliSpecchiIncrinati/05_ChiaraBuscemi_Ambiente_BN_v01.jpg", "specchi-illustrazione.jpg"),
    ("10_EclissiAlSipario/SaladegliSpecchiIncrinati/05_ChiaraBuscemi_Ambiente_Carta_v01.png", "specchi-carta.png"),
    ("10_EclissiAlSipario/ComposizioneGioco(generato tutti inAi)/ChiaraBuscemi_Composit_v01.png", "composizione.png"),
],
"11-journey-rove": [
    ("11_JOURNEY — Rove/ChiaraBuscemi_BoxMockup_v01_BN.jpg", "mockup-1.jpg"),
    ("11_JOURNEY — Rove/ChiaraBuscemi_BoxMockup_v02_BN.jpg", "mockup-2.jpg"),
    ("11_JOURNEY — Rove/ChiaraBuscemi_Coperchio_BN.jpg", "coperchio.jpg"),
    ("11_JOURNEY — Rove/ChiaraBuscemi_Corpo_BN.jpg", "corpo.jpg"),
    ("11_JOURNEY — Rove/ChiaraBuscemi_Sneakers_v01.jpg", "sneakers-1.jpg"),
    ("11_JOURNEY — Rove/ChiaraBuscemi_Sneakers_v02.jpg", "sneakers-2.jpg"),
],
"12-flaytraps": [
    ("12_Flytraps/Box/COVER.jpg", "box-cover.jpg"),
    ("12_Flytraps/Box/3/ChiaraBuscemi_R03_v01.jpg", "box-retro.jpg"),
    ("12_Flytraps/Box/mockup/MockUp_Box_V01.jpg", "mockup.jpg"),
    ("12_Flytraps/Composizione/Assemblaggio_V04 .png", "composizione.png"),
    ("12_Flytraps/Pedina/1.jpg", "tile-pianta-1.jpg"),
    ("12_Flytraps/Pedina/3.jpg", "tile-pianta-2.jpg"),
    ("12_Flytraps/Pedina/5.jpg", "tile-pianta-3.jpg"),
    ("12_Flytraps/Pedina/7.jpg", "tile-pianta-4.jpg"),
    ("12_Flytraps/Vasi/Vaso1psd copia 2.jpg", "tile-vaso-1.jpg"),
    ("12_Flytraps/Vasi/vaso3.jpg", "tile-vaso-2.jpg"),
    ("12_Flytraps/Fiore/IMG_3197 copia.png", "token-fiore.png"),
    ("12_Flytraps/Pedina/Bozze/ChiaraBuscemi_R_PlantTile_v02.jpg", "bozza-1.jpg"),
    ("12_Flytraps/Vasi/Bozze/IMG_3495.JPG", "bozza-2.jpg"),
],
"14-drago-nel-cortile": [
    ("14_UnDragonelCortile/Triangolo_V01.JPG", "finale.jpg"),
    ("14_UnDragonelCortile/Triangolo_R01_V01.JPG", "bozza-1.jpg"),
    ("14_UnDragonelCortile/Triangolo_R01_V02.JPG", "bozza-2.jpg"),
    ("14_UnDragonelCortile/Triangolo_RC_V01.JPG", "bozza-3.jpg"),
    ("14_UnDragonelCortile/Triangolo_RC_V02.JPG", "bozza-4.jpg"),
],
"15-eva-non-si-veste": [
    ("15_EvaNonSiVeste/EvaNonSiVeste_V01.2.heic", "finale-1.jpg"),
    ("15_EvaNonSiVeste/EvaNonSiVeste_V01.3.heic", "finale-2.jpg"),
    ("15_EvaNonSiVeste/EvaNonSiVeste_V01.4.heic", "finale-3.jpg"),
    ("15_EvaNonSiVeste/EvaNonSiVeste_V01.5.heic", "finale-4.jpg"),
    ("15_EvaNonSiVeste/EvaNonSiVeste_V01.1.heic", "finale-5.jpg"),
    ("15_EvaNonSiVeste/EvaNonSiVeste_V01.6.heic", "finale-6.jpg"),
    ("15_EvaNonSiVeste/EvaNonSiVeste_R01_V01.JPG", "bozza-1.jpg"),
    ("15_EvaNonSiVeste/EvaNonSiVeste_R01_V02.heic", "bozza-2.jpg"),
    ("15_EvaNonSiVeste/EvaNonSiVeste_R01_V04.heic", "bozza-3.jpg"),
],
"16-social-vs-bambini": [
    ("16_SocialvsBambini/B_01_V02 (1).JPG", "finale.jpg"),
    ("16_SocialvsBambini/B01_R02_v02.JPG", "bozza-1.jpg"),
],
"17-pesca-sostenibile": [
    ("17_Pescasostenibile/B02_v01.JPG", "finale.jpg"),
    ("17_Pescasostenibile/B03_v01.1.jpg", "finale-2.jpg"),
    ("17_Pescasostenibile/B02_R01_v01.jpg", "bozza-1.jpg"),
    ("17_Pescasostenibile/B02_R02_v01.JPG", "bozza-2.jpg"),
    ("17_Pescasostenibile/B02_R03_v01.JPG", "bozza-3.jpg"),
],
"19-spot-clio": [
    ("19_Spot/B04_v01.jpg", "spot-1.jpg"),
    ("19_Spot/B04_v02.jpg", "spot-2.jpg"),
    ("19_Spot/B04_v03.jpg", "spot-3.jpg"),
    ("19_Spot/B04_v04.jpg", "spot-4.jpg"),
    ("19_Spot/B04_v05.jpg", "spot-5.jpg"),
    ("19_Spot/B04_v06.jpg", "spot-6.jpg"),
    ("19_Spot/B04_v07.jpg", "spot-7.jpg"),
    ("19_Spot/B04_v08.jpg", "spot-8.jpg"),
],
}

PDF_JOBS = [
    # Journey bozze (scansioni a mano, ordine cronologico come in cartella)
    ("11_JOURNEY — Rove/Bozze/Scansione 18-03-26 (09.19.52).pdf", 0, "11-journey-rove/bozza-1.jpg"),
    ("11_JOURNEY — Rove/Bozze/Scansione 18-03-26 (09.21.48).pdf", 0, "11-journey-rove/bozza-2.jpg"),
    ("11_JOURNEY — Rove/Bozze/Scansione 18-03-26 (09.23.18).pdf", 0, "11-journey-rove/bozza-3.jpg"),
    ("11_JOURNEY — Rove/Bozze/Scansione 18-03-26 (09.25.44).pdf", 0, "11-journey-rove/bozza-4.jpg"),
    ("11_JOURNEY — Rove/Bozze/Scansione 18-03-26 (09.27.15).pdf", 0, "11-journey-rove/bozza-5.jpg"),
    ("11_JOURNEY — Rove/Bozze/Scansione 18-03-26 (09.31.22).pdf", 0, "11-journey-rove/bozza-6.jpg"),
    ("11_JOURNEY — Rove/Bozze/Scansione 18-03-26 (09.32.46).pdf", 0, "11-journey-rove/bozza-7.jpg"),
    ("11_JOURNEY — Rove/Bozze/Scansione 18-03-26 (09.34.01).pdf", 0, "11-journey-rove/bozza-8.jpg"),
    ("11_JOURNEY — Rove/Bozze/Scansione 18-03-26 (09.35.23).pdf", 0, "11-journey-rove/bozza-9.jpg"),
    ("11_JOURNEY — Rove/Bozze/Scansione 18-03-26 (09.36.30).pdf", 0, "11-journey-rove/bozza-10.jpg"),
    ("11_JOURNEY — Rove/Bozze/Scansione 18-03-26 (09.37.37).pdf", 0, "11-journey-rove/bozza-11.jpg"),
    ("11_JOURNEY — Rove/Bozze/Scansione 18-03-26 (09.38.34).pdf", 0, "11-journey-rove/bozza-12.jpg"),
    ("11_JOURNEY — Rove/Bozze/Scansione 18-03-26 (09.41.09).pdf", 0, "11-journey-rove/bozza-13.jpg"),
    ("11_JOURNEY — Rove/Bozze/Scansione 18-03-26 (09.42.11).pdf", 0, "11-journey-rove/bozza-14.jpg"),
    ("11_JOURNEY — Rove/Bozze/Scansione 18-03-26 (09.43.23).pdf", 0, "11-journey-rove/bozza-15.jpg"),
    ("11_JOURNEY — Rove/Bozze/Scansione 18-03-26 (09.44.28).pdf", 0, "11-journey-rove/bozza-16.jpg"),
    # Eva bozze (pdf)
    ("15_EvaNonSiVeste/EvaNonSiVeste_R01_V03.pdf", 0, "15-eva-non-si-veste/bozza-4.jpg"),
    ("15_EvaNonSiVeste/EvaNonSiVeste_RC_V01.pdf", 0, "15-eva-non-si-veste/bozza-5.jpg"),
    # Ansia: storyboard
    ("13_Ansia/ProvaStoryboard.pdf", 0, "13-ansia/storyboard.jpg"),
]

COPY_JOBS = [
    ("14_UnDragonelCortile/Triangolo_V02.GIF", "14-drago-nel-cortile/stop-motion.gif"),
    ("15_EvaNonSiVeste/EvaNonSiVeste_V01.gif", "15-eva-non-si-veste/stop-motion.gif"),
]

def main():
    # 1) anteprime sRGB
    for slug, items in JOBS.items():
        print("==", slug)
        for s, d in items:
            conv(s, os.path.join(slug, d))
    # 2) PDF -> immagine
    print("== PDF jobs")
    for s, p, d in PDF_JOBS:
        conv_pdf(s, p, d)
    # 3) Ansia: quaderno di progettazione (tutte le pagine)
    print("== Ansia quaderno")
    doc = fitz.open(os.path.join(SRC, "13_Ansia/Ansia.pdf"))
    for i in range(len(doc)):
        pix = doc[i].get_pixmap(matrix=fitz.Matrix(1.6, 1.6))
        im = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
        save_preview(im, os.path.join(LAV, "13-ansia", f"pagina-{i+1:02d}.jpg"))
    print("   ok ansia pagine:", len(doc))
    # 4) copie GIF intatte
    print("== GIF")
    for s, d in COPY_JOBS:
        copy_raw(s, d)
    # 5) cover placeholder
    make_cover_placeholder()
    print("\nFATTO.")

def make_cover_placeholder():
    os.makedirs(COVER, exist_ok=True)
    W, H = 1600, 2100
    img = Image.new("RGB", (W, H), (236, 232, 225))
    d = ImageDraw.Draw(img)
    d.rectangle([40, 40, W-40, H-40], outline=(120, 95, 120), width=6)
    def font(sz):
        for fn in ("seguisb.ttf", "segoeui.ttf", "arial.ttf"):
            try: return ImageFont.truetype(fn, sz)
            except Exception: pass
        return ImageFont.load_default()
    def center(txt, y, f, fill):
        bb = d.textbbox((0, 0), txt, font=f)
        d.text(((W-(bb[2]-bb[0]))//2, y), txt, font=f, fill=fill)
    center("COPERTINA", 760, font(120), (91, 58, 91))
    center("segnaposto", 920, font(70), (120, 95, 120))
    center("Sostituisci questo file con", 1120, font(48), (90, 84, 80))
    center("assets/cover/copertina.jpg", 1185, font(48), (90, 84, 80))
    img.save(os.path.join(COVER, "copertina.jpg"), "JPEG", quality=90)
    print("   ok cover placeholder")

def archive_masters():
    if os.path.exists(ORIG):
        print("originali-cmyk gia presente: salto la copia dei master.")
        return
    print("Copio i master intatti in", ORIG, "...")
    def ignore(d, names):
        return [n for n in names if n.lower().endswith(".pdf") and "Foglio1" in n]
    shutil.copytree(SRC, ORIG, ignore=ignore)
    print("   master archiviati.")

if __name__ == "__main__":
    if "--masters" in sys.argv:
        archive_masters()
    else:
        main()
